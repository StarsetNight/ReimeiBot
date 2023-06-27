import nonebot
from nonebot.rule import Rule
from reimei_api.rule import globalWhitelisted
global_config = nonebot.get_driver().config


async def isEnabled():
    """
    :return: 插件是否被启用
    """
    return global_config.plugins_metadata["reimeibot_plugin_database"]

isPassed = Rule(isEnabled, globalWhitelisted)
