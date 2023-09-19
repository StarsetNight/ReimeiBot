import re


async def get_at(string: str) -> int:
    """
    获取at消息中的QQ号
    返回-1则为消息中不存在at信息或at信息格式错误
    :return: int
    """
    try:
        return int(re.findall(r"\[CQ:at,qq=([0-9]+)\]", string)[0])
    except:
        return -1


def CQ2dict(string: str) -> dict:
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


def msg2list(args: Message) -> list:
    """
    把Message转换为onebot的消息段数组格式的list
    :return: list
    """
    args = list(args)
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
