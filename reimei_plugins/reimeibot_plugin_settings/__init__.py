import nonebot
import sqlite3
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from .config import Config
from reimei_api.rule import globalWhitelisted
from reimei_api.permission import isMaintainer

driver = nonebot.get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

global_config.superusers = {}  # 最高管理者
global_config.maintainers = {}  # 维护员
global_config.nickname = config.bot_nickname  # 昵称
global_config.global_whitelist = {}  # 全局白名单，一些通用插件可以使用这个

connection: sqlite3.Connection
cursor: sqlite3.Cursor

# 命令合集
set_failsafe = on_command("/failsafe", permission=SUPERUSER, aliases={"/紧急备用设置"}, priority=10, block=True)

add_whitelist = on_command(("/whitelist", "add"), rule=globalWhitelisted,
                           permission=isMaintainer, aliases={"/添加白名单"}, priority=10, block=True)
get_whitelist = on_command(("/whitelist", "list"), rule=globalWhitelisted,
                           permission=isMaintainer, aliases={"/列出白名单"}, priority=10, block=True)
del_whitelist = on_command(("/whitelist", "remove"), rule=globalWhitelisted,
                           permission=isMaintainer, aliases={"/移除白名单"}, priority=10, block=True)

set_permission = on_command(("/permission", "set"), rule=globalWhitelisted,
                            permission=SUPERUSER, aliases={"/设置权限"}, priority=10, block=True)
get_permission = on_command(("/permission", "get"), rule=globalWhitelisted,
                            permission=SUPERUSER, aliases={"/获取权限"}, priority=10, block=True)
del_permission = on_command(("/permission", "remove"), rule=globalWhitelisted,
                            permission=SUPERUSER, aliases={"/移除权限"}, priority=10, block=True)


@driver.on_startup
async def startup():
    global connection, cursor
    connection = sqlite3.connect("reimei_databases/ReimeiBotPluginSettings.db")
    cursor = connection.cursor()

    # 如果表不存在，初始化表
    cursor.execute(config.initialize_permission)
    cursor.execute(config.initialize_whitelist)
    cursor.execute(config.initialize_settings)
    connection.commit()

    # 如果表早已存在，从表里面获取信息并写入到Nonebot全局配置池
    superusers = cursor.execute(config.list_permission, ("Superuser",)).fetchall()
    global_config.superusers = {superuser[0] for superuser in superusers}
    maintainers = cursor.execute(config.list_permission, ("Maintainer",)).fetchall()
    global_config.maintainers = {maintainer[0] for maintainer in maintainers}
    whitelist_groups = cursor.execute(config.get_whitelist).fetchall()
    global_config.global_whitelist = {whitelist_group[0] for whitelist_group in whitelist_groups}

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
        await add_whitelist.finish(f"群聊{group_id}已经从全局白名单移除了哦！")
    else:
        await add_whitelist.finish(f"{group_id}不是纯数字形式哦！不可以从全局白名单移除呐~")


@set_permission.handle()
async def setPermission(args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split(" ")
    if len(args) >= 2:
        if args[0].isdigit():
            match args[1]:
                case "Superuser":
                    global_config.superusers.add(args[0])
                case "Maintainer":
                    global_config.maintainers.add(args[0])
            cursor.execute(config.set_permission, args)
            connection.commit()
            await add_whitelist.finish(f"用户{args[0]}的权限已经被设置为了{args[1]}哦！")
        else:
            await add_whitelist.finish(f"{args[0]}不是纯数字形式哦！不可以添加权限呐~")
    else:
        await add_whitelist.finish("不对，不对！正确的命令形式应当为“/permission.set <QQ号> <权限>”才对！")


@get_permission.handle()
async def getPermission(args: Message = CommandArg()):
    if (qq := args.extract_plain_text()).strip().isdigit():
        try:
            cursor.execute(config.get_permission, (qq,))
            connection.commit()
        except sqlite3.OperationalError:
            await add_whitelist.finish(f"用户{qq}没有权限呐~")
        else:
            await add_whitelist.finish(f"用户{qq}的权限是{cursor.fetchone()[0]}哦！")
    else:
        await add_whitelist.finish(f"{args[0]}不是纯数字形式哦！不可以获取权限呐~")


@del_permission.handle()
async def delPermission(args: Message = CommandArg()):
    if (qq := args.extract_plain_text()).strip().isdigit():
        try:
            cursor.execute(config.del_permission, (qq,))
            connection.commit()
        except sqlite3.OperationalError:
            await add_whitelist.finish(f"用户{qq}没有权限呐~")
        else:
            await add_whitelist.finish(f"用户{qq}的权限成功被移除了哦！")
        finally:
            global_config.superusers.remove(qq) if qq in global_config.superusers else None
            global_config.maintainers.remove(qq) if qq in global_config.maintainers else None
    else:
        await add_whitelist.finish(f"{args[0]}不是纯数字形式哦！不可以删除权限呐~")
