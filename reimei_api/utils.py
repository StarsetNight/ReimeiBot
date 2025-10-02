from nonebot.adapters.onebot.v11 import Message, Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent

import hashlib
import asyncio
import zlib
import re

from aiofile import async_open
import httpx


async def getIdentityFromQQ(qq_list: list[int | str], bot: Bot, group_id: int | str | None = None, *,
                            card: bool = True,
                            do_cache: bool = False) -> list[str]:
    """
    使用多个qq号构建形如多个{昵称}({qq})的文本

    参数:
      qq_list (list[int|str]): qq号列表
      group_id (int|str): 群号，不填则使用get_stranger_info获取昵称
      bot (Bot): bot对象
      card (bool): 为True且群号不为空时使用群昵称，默认为True
      do_cache (bool): 是否使用缓存，使用速度更快但是相对没有那么新，默认为False

    返回:
      list[str]: 形如"{昵称}({qq})"的字符串的列表
    """
    if group_id is None or not card:  # 当群号为空或不使用群昵称时
        tasks = [bot.get_stranger_info(user_id=qq, no_cache=not do_cache) for qq in qq_list]
        results = await asyncio.gather(*tasks)
        return [f'{result["nickname"]}({qq})' for qq, result in zip(qq_list, results)]

    elif group_id is not None and card:  # 当群号不为空且使用群昵称时
        tasks = [bot.get_group_member_info(user_id=qq, group_id=group_id, no_cache=not do_cache) for qq in qq_list]
        results = await asyncio.gather(*tasks)
        return [f'{result["card"]}({qq})' for qq, result in zip(qq_list, results)]

    return []


async def getNicknameFromQQ(qq: int | str, bot: Bot, group_id: int | str | None = None, *, card: bool = True,
                            do_cache: bool = False) -> str | None:
    """
    使用qq号构建形如{昵称}({qq})的文本

    参数:
      qq (int|str): qq号
      group_id (int|str): 群号，不填则使用get_stranger_info获取昵称
      bot (Bot): bot对象
      card (bool): 为True且群号不为空时使用群昵称，默认为True
      do_cache (bool): 是否使用缓存，使用速度更快但是相对没有那么新，默认为False

    返回:
      str: 形如"{昵称}({qq})"的字符串
    """
    try:
        if group_id is None or not card:  # 当群号为空且或不使用群昵称时
            res = f"{(await bot.get_stranger_info(user_id=qq, no_cache=not do_cache))['nickname']}({qq})"
        elif group_id is not None and card:  # 当群号不为空且使用群昵称时
            res = f'{(await bot.get_group_member_info(user_id=qq, group_id=group_id, no_cache=not do_cache))["card"]}({qq})'
        else:
            res = str(qq)
    except TypeError:
        res = str(qq)
    return res


async def sendForwardMsg(content: Message | str, event: GroupMessageEvent, bot: Bot) -> dict:
    """
    构建并发送群转发消息

    参数:
      content (Message): 消息段
      content (str): 消息文本
      event (GroupMessageEvent): 消息事件
      bot (Bot): bot对象

    返回:
      dict: call_api返回数据
    """
    return_data = await bot.call_api("send_group_forward_msg", data={
        "group_id": event.group_id,
        "message": [
            {
                "uin": str(event.self_id),
                "name": (await bot.get_login_info())["nickname"],
                "content": content
            }
        ]
    })
    return return_data


async def key_value2dict(text: str) -> dict | str:
    """
    把传入的形如"aaa=bbb ccc=ddd"的字符串转换为形如{'aaa':'bbb','ccc','ddd'}的dict

    参数:
        text (str): 需要处理的字符串

    返回:
        dict: 处理完成的dict
        str: 错误信息
    """
    try:
        text = text.strip()
        return_value = dict([i.split("=") for i in text.split(" ")])
        print(return_value)
        return return_value
    except BaseException as error:
        return str(error)



async def CQ2dict(string: str) -> dict:
    """
    把单个CQ码转换为onebot的消息段格式的dict
    :return: dict
    """
    CQ_code = re.findall(r"\[CQ:.+?]", string)[0]
    CQ_type = re.findall(r"\[CQ:(.+?),.+]", CQ_code)[0]
    CQ_code_value = re.findall(r"\[CQ:.+?,(.+=.+)+]", CQ_code)[0].split(",")
    CQ_json = {"type": CQ_type}
    data = {}
    for i in CQ_code_value:
        value = i.split("=")
        data[value[0]] = value[1]
    CQ_json["data"] = data
    return CQ_json


async def msg2list(msg: Message | str) -> list:
    """
    把Message转换为onebot的消息段数组格式的list
    :return: list
    """
    if type(msg) == Message:
        args = list(msg)
    else:
        args = list(Message(msg))
    args = [str(i) for i in args]
    msg_list = []
    for i in args:
        temp_dict = {}
        if not re.findall(r"[CQ:.+?]", i):
            temp_dict["type"] = "text"
            temp_dict["data"] = {"text": i}
        else:
            temp_dict = CQ2dict(i)
        msg_list.append(temp_dict)
    return msg_list


async def get_at(msg: Message) -> int:
    """
    获取at消息中的QQ号
    返回-1则为消息中不存在at信息或at信息格式错误
    :return: int
    """
    at = msg["at"]
    if not msg:
        return at[0].data["qq"]
    else:
        return -1


async def in_type(args: Message, type_: str) -> bool:
    """
    检测传入Message中是否有at消息

    参数:
        args (Message): 需要检测的消息段

    返回:
        bool: 是否存在at消息
    """
    if not args[type_]:
        return True
    else:
        return False


async def args_qq(args: Message) -> str | None:
    """
    从消息里提取纯文本的qq号或者at消息的qq号

    参数:
        args (Message): 要提取的消息段

    返回:
        str: 提取出来的qq号
        None: 这个消息既没有qq号也没有at
    """
    if args.extract_plain_text().isdigit():
        return args.extract_plain_text()
    if in_type(args, "at"):
        return str(await get_at(args))
    else:
        return None


async def _async_download_content(url: str) -> bytes:
    """
    异步获取url的content

    参数:
        url (str): 地址

    返回:
        bytes: 下载下来的content

    可能出现的错误:
        和使用httpx.AsyncClient().get()一样
    """
    async with httpx.AsyncClient() as client:
        data = (await client.get(url)).content
    return data


async def calculate_sha256(file_path: str) -> str:
    """
    读取文件内容并计算SHA256哈希值。

    参数:
        file_path (str): 要读取的文件的路径。

    返回:
        str: 文件的SHA256哈希值。
    """
    sha256_hash = hashlib.sha256()
    async with async_open(file_path, "rb") as f:
        while True:
            byte_block = await f.read(4096)
            if not byte_block:
                break
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


async def calculate_crc32(file_path: str) -> str:
    """
    读取文件内容并计算CRC32哈希值，并以16进制表示。

    参数:
        file_path (str): 要读取的文件的路径。

    返回:
        str: CRC32的十六进制表示
    """
    crc32_hash = 0
    async with async_open(file_path, 'rb') as file:
        while True:
            chunk = await file.read(4096)
            if not chunk:
                break
            crc32_hash = zlib.crc32(chunk, crc32_hash)
    return f"{crc32_hash & 0xffffffff:08x}"
