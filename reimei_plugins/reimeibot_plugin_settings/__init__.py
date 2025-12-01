# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

import nonebot
import sqlite3
from nonebot import on_command, CommandGroup
from nonebot.adapters.onebot.v11 import Message
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot import on_message
from nonebot import logger

from .config import Config
from reimei_api.rule import globalWhitelisted
from reimei_api.permission import isMaintainer, isBaka
from reimei_api.help import getHelp
from nonebot.plugin import PluginMetadata

driver = nonebot.get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

global_config.superusers = {}  # 最高管理者
global_config.maintainers = {}  # 维护员
global_config.blacklist = {}  # 黑名单
global_config.nickname = config.bot_nickname  # 昵称
global_config.global_whitelist = {}  # 全局白名单，一些通用插件可以使用这个

connection: sqlite3.Connection
cursor: sqlite3.Cursor

# 注册插件
__plugin_meta__ = PluginMetadata(
    name="Reimei设定",
    description="ReimeiBot设定系统",
    usage=config.docs,
    config=Config,
    extra={
        "Enabled": True
    },
)

# 命令合集
on_message(block=True, priority=0, rule=isBaka)

set_failsafe = on_command("/failsafe", permission=SUPERUSER, aliases={"/紧急备用设置"}, priority=-1, block=True)

whitelist_command_group = CommandGroup("/whitelist", priority=10, permission=isMaintainer, block=True)
add_whitelist = whitelist_command_group.command("add", aliases={"/添加白名单"})
get_whitelist = whitelist_command_group.command("get", aliases={"/获取白名单"})
del_whitelist = whitelist_command_group.command("del", aliases={"/移除白名单"})

blacklist_command_group = CommandGroup("/blacklist", permission=isMaintainer, priority=1, block=True)
blacklist_add = blacklist_command_group.command("add", aliases={"/黑名单添加"})
blacklist_del = blacklist_command_group.command("del", aliases={"/黑名单移除"})
blacklist_lookup = blacklist_command_group.command("lookup", aliases={"/列出黑名单"})

permission_command_group = CommandGroup("/permission", permission=SUPERUSER, priority=10, block=True)
set_permission = permission_command_group.command("set", aliases={"/设置权限"})
get_permission = permission_command_group.command("get", aliases={"/获取权限"})
del_permission = permission_command_group.command("remove", aliases={"/移除权限"})

get_help = on_command(("/settings", "help"), aliases={"/设定帮助"}, priority=10, block=True)


@driver.on_startup
async def startup():
    global connection, cursor
    connection = sqlite3.connect("reimei_databases/ReimeiBotPluginSettings.db")
    cursor = connection.cursor()

    # 如果表不存在，初始化表
    cursor.execute(config.initialize_permission)
    cursor.execute(config.initialize_whitelist)
    cursor.execute(config.initialize_settings)
    cursor.execute(config.initialize_blacklist)
    connection.commit()

    # 如果表早已存在，从表里面获取信息并写入到Nonebot全局配置池
    superusers = cursor.execute(config.list_permission, ("Superuser",)).fetchall()
    global_config.superusers = {superuser[0] for superuser in superusers}
    maintainers = cursor.execute(config.list_permission, ("Maintainer",)).fetchall()
    global_config.maintainers = {maintainer[0] for maintainer in maintainers}
    whitelist_groups = cursor.execute(config.get_whitelist).fetchall()
    global_config.global_whitelist = {whitelist_group[0] for whitelist_group in whitelist_groups}
    blacklists = cursor.execute(config.blacklist_get)
    global_config.blacklist = {blacklist[0] for blacklist in blacklists}
    logger.info(f"Superuser:{global_config.superusers}")
    logger.info(f"Maintainers:{global_config.maintainers}")
    logger.info(f"Whitelist:{global_config.global_whitelist}")
    logger.info(f"Blacklist:{global_config.blacklist}")
    # 设置一些东西
    global_config.failsafe_group = config.failsafe_group  # 紧急备用群聊


@driver.on_shutdown
async def shutdown():
    connection.close()


@set_failsafe.handle()
async def setFailsafe(args: Message = CommandArg()):
    if (group_id := args.extract_plain_text()).isdigit():
        global_config.failsafe_group = group_id
        await set_failsafe.finish(f"紧急备用群聊已被设置为{group_id}了！如果你有急事，赶快去做，不要耽误了哦！")
    else:
        await set_failsafe.finish(f"{group_id}不是一个纯数字的群聊ID形式！！！")


@add_whitelist.handle()
async def addWhitelist(args: Message = CommandArg()):
    if (group_id := args.extract_plain_text()).strip().isdigit():
        if group_id in global_config.global_whitelist:
            await add_whitelist.finish(f"群聊{group_id}早就在全局白名单了哦，不可以重复添加呐！")
        global_config.global_whitelist.add(group_id)
        cursor.execute(config.add_whitelist, (group_id,))
        connection.commit()
        await add_whitelist.finish(f"群聊{group_id}已被添加进全局白名单了哦！快让你的小伙伴也来使用吧！")
    else:
        await add_whitelist.finish(f"{group_id}不是纯数字形式哦！不可以添加进白名单呐~")


@get_whitelist.handle()
async def listWhitelist():
    white_str = ""
    for count, whitegroup in enumerate(global_config.global_whitelist, start=1):
        white_str += f"{count}: {whitegroup}\n"
    await get_whitelist.finish(f"呐，这些是全局白名单的列表哦，你过目一下：\n{white_str}\n"
                               f"还有最重要的紧急备用群聊！群号是这个：{global_config.failsafe_group}")


@del_whitelist.handle()
async def removeWhitelist(args: Message = CommandArg()):
    if (group_id := args.extract_plain_text()).strip().isdigit():
        if group_id not in global_config.global_whitelist:
            await add_whitelist.finish(f"喂！群聊{group_id}根本不在全局白名单里！")
        global_config.global_whitelist.remove(group_id)
        cursor.execute(config.del_whitelist, (group_id,))
        connection.commit()
        await del_whitelist.finish(f"群聊{group_id}已经从全局白名单移除了哦！")
    else:
        await del_whitelist.finish(f"{group_id}不是纯数字形式哦！不可以从全局白名单移除呐~")


@set_permission.handle()
async def setPermission(args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split(" ")
    if len(args) >= 2:
        if args[0].isdigit():
            global_config.superusers.remove(args[0]) if args[0] in global_config.superusers else None
            global_config.maintainers.remove(args[0]) if args[0] in global_config.maintainers else None
            match args[1]:
                case "Superuser":
                    global_config.superusers.add(args[0])
                case "Maintainer":
                    global_config.maintainers.add(args[0])
            cursor.execute(config.set_permission, args)
            connection.commit()
            await set_permission.finish(f"用户{args[0]}的权限已经被设置为了{args[1]}哦！")
        else:
            await set_permission.finish(f"{args[0]}不是纯数字形式哦！不可以添加权限呐~")
    else:
        await set_permission.finish("不对，不对！正确的命令形式应当为“/permission.set <QQ号> <权限>”才对！")


@get_permission.handle()
async def getPermission(args: Message = CommandArg()):
    if (qq := args.extract_plain_text()).strip().isdigit():
        try:
            cursor.execute(config.get_permission, (qq,))
            connection.commit()
        except sqlite3.OperationalError:
            await get_permission.finish(f"用户{qq}没有权限呐~")
        else:
            await get_permission.finish(f"用户{qq}的权限是{cursor.fetchone()[0]}哦！")
    else:
        await get_permission.finish(f"{args[0]}不是纯数字形式哦！不可以获取权限呐~")


@del_permission.handle()
async def delPermission(args: Message = CommandArg()):
    if (qq := args.extract_plain_text()).strip().isdigit():
        try:
            cursor.execute(config.del_permission, (qq,))
            connection.commit()
        except sqlite3.OperationalError:
            await del_permission.finish(f"用户{qq}没有权限呐~")
        else:
            await del_permission.finish(f"用户{qq}的权限成功被移除了哦！")
        finally:
            global_config.superusers.remove(qq) if qq in global_config.superusers else None
            global_config.maintainers.remove(qq) if qq in global_config.maintainers else None
    else:
        await del_permission.finish(f"{args[0]}不是纯数字形式哦！不可以删除权限呐~")


@blacklist_add.handle()
async def blacklist_add_handle(args: Message = CommandArg()):
    if not (qq := args.extract_plain_text()).strip().isdigit():
        await blacklist_add.finish(f"{args[0]}不是纯数字形式哦！不可以拉黑呐~")
    if qq in global_config.blacklist:
        await blacklist_add.finish(f"{qq}已经在黎明系统黑名单了，不可重复添加！")
    cursor.execute(config.blacklist_add, (qq,))
    connection.commit()
    global_config.blacklist.add(qq)
    await blacklist_add.finish(f"成功将{qq}添加到黎明系统黑名单！")


@blacklist_del.handle()
async def blacklist_del_handle(args: Message = CommandArg()):
    if not (qq := args.extract_plain_text()).strip().strip():
        await blacklist_del.finish(f"{args[0]}不是纯数字形式哦！不可以解除拉黑呐~")
    if not qq in global_config.blacklist:
        await blacklist_del.finish(f"{qq}不在黎明系统黑名单，不可移除！")
    cursor.execute(config.blacklist_del, (qq,))
    connection.commit()
    global_config.blacklist.remove(qq)
    await blacklist_del.finish(f"成功将{qq}从黎明系统黑名单移除！")


@blacklist_lookup.handle()
async def blacklist_lookup_handle():
    msg = ""
    for i in global_config.blacklist:
        msg = f"{msg}{i}\n"
    await blacklist_lookup.finish(f"黎明系统黑名单列表：\n{msg}")


@get_help.handle()
async def getDatabaseHelp():
    await get_help.finish(await getHelp("reimeibot_plugin_settings"))
