import nonebot

global_config = nonebot.get_driver().config


async def globalWhitelisted(event: nonebot.adapters.Event):
    """
    无论白名单怎么改，failsafe群聊永远不会被阻挡。
    :return: 是否在白名单内
    """
    session = event.get_session_id()
    return session.startswith(f"group_{global_config.global_whitelist}") or \
           session.startswith(f"group_{global_config.failsafe_group}")
