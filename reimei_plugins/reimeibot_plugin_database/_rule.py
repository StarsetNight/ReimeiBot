import nonebot
global_config = nonebot.get_driver().config


async def isEnabled():
    """
    :return: 插件是否被启用
    """
    return nonebot.get_plugin("reimeibot_plugin_database").metadata.extra["Enabled"]
