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
