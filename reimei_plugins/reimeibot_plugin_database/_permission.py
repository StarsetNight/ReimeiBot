"""
项目名称：ReimeiBot
项目作者：StarsetNight（化名：何星夕，网名：星夕Starset）
许可协议：MIT许可证

版权所有 (c) 2023 星夕Starset
依据MIT许可证效力，衍生项目需保证本版权声明原封不动，可以增添“原”前缀以免与您的衍生项目混淆
"""

import nonebot
from .config import Config

driver = nonebot.get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)


async def isAllowed(event: nonebot.adapters.Event):
    """
    表面上权限检查只检查维护者，但是超级用户也可通过此权限检查器。
    :return: 是否符合本插件权限
    """
    return event.get_user_id() in eval(config.allow_group) or event.get_user_id() in global_config.superusers
