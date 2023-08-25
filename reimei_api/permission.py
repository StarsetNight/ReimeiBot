import nonebot
global_config = nonebot.get_driver().config


async def isMaintainer(event: nonebot.adapters.Event):
    """
    表面上权限检查只检查维护者，但是超级用户也可通过此权限检查器。
    :return: 是否符合权限
    """
    return event.get_user_id() in global_config.maintainers or event.get_user_id() in global_config.superusers


async def isBaka(event: nonebot.adapters.Event):
    """
    判断是否在黑名单中
    :return: bool
    """
    return event.get_user_id() in global_config.blacklist
