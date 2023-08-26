"""
项目名称：ReimeiBot
项目作者：StarsetNight（化名：何星夕，网名：星夕Starset）
许可协议：MIT许可证

版权所有 (c) 2023 星夕Starset
依据MIT许可证效力，衍生项目需保证本版权声明原封不动，可以增添“原”前缀以免与您的衍生项目混淆
"""

import nonebot

global_config = nonebot.get_driver().config


async def globalWhitelisted(event: nonebot.adapters.Event):
    """
    无论白名单怎么改，failsafe群聊永远不会被阻挡。
    :return: 是否不在白名单内
    """
    if (session := event.get_session_id()).startswith("group_"):
        group_id = session.split("_")[1]
        return not (group_id in global_config.global_whitelist or
                    group_id == global_config.failsafe_group)
    return True

