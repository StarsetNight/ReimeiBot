# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

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

