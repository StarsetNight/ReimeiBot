import nonebot
global_config = nonebot.get_driver().config


async def globalWhitelisted(event: nonebot.adapters.Event):
    """
    无论白名单怎么改，failsafe群聊永远不会被阻挡。
    :return: 是否在白名单内
    """
    session = event.get_session_id().split("_")
    return ((session[1] in global_config.global_whitelist or session[1] == global_config.failsafe_group)
            and session[0] == "group")