"""
项目名称：ReimeiBot
项目作者：StarsetNight（化名：何星夕，网名：星夕Starset）
许可协议：MIT许可证

版权所有 (c) 2023 星夕Starset
依据MIT许可证效力，衍生项目需保证本版权声明原封不动，可以增添“原”前缀以免与您的衍生项目混淆
"""
from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot import logger

from reimei_api.permission import isMaintainer

from config import Config

from json import loads
from json.decoder import JSONDecodeError

driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

__plugin_meta__ = PluginMetadata(
    name="Reimei GoCQAPI",
    description="ReimeiBot GoCQAPI快捷调用",
    usage="【ReimeiBot GoCQAPI快捷调用】\n/call_api [api名] [json数据]",
    config=Config,
    extra={
        "Enabled": True
    },
)

call_api = on_command("/call_api", aliases={"/调用API"}, permission=isMaintainer)


@call_api.handle()  # 写的非常屎
async def call_api_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    user_id = event.user_id
    user_info = await bot.get_stranger_info(user_id=user_id)
    text_list = text.split(" ")
    if len(text_list) != 2 and len(text_list) == 1:
        return_data = await bot.call_api(api=text_list[0])
        logger.info(f"管理员{user_info.get('nickname')}({user_id})调用了API：{text_list[0]}")
        logger.info(f"API返回值：{return_data}")
        await call_api.finish(f"API返回值：{return_data}")
    if len(text_list) != 2:
        await call_api.finish("参数有误")
    try:
        json_data = loads(text_list[1])
    except JSONDecodeError as error:
        await call_api.finish(f"json数据错误:{error}")
    return_data = await bot.call_api(api=text_list[0], **json_data)
    logger.info(f"管理员{user_info.get('nickname')}({user_id})调用了API：{text_list[0]},参数：{json_data}")
    logger.info(f"API返回值：{return_data}")
    await call_api.finish(f"API返回值：{return_data}")
