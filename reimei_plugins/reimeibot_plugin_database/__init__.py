import nonebot
import os
import sqlite3
from nonebot import CommandGroup
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

from reimei_api.help import getHelp
from .config import Config
from ._permission import isAllowed
from ._rule import isPassed
from nonebot.plugin import PluginMetadata

driver = nonebot.get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

connection: sqlite3.Connection
cursor: sqlite3.Cursor

# 注册插件
__plugin_meta__ = PluginMetadata(
    name="Reimei数据库",
    description="ReimeiBot数据库管理系统",
    usage=config.docs,
    config=Config,
    extra={
        "Enabled": True
    },
)

# 事件合集
db_command_group = CommandGroup("/db", rule=isPassed, permission=isAllowed, priority=6, block=True)
new_connection = db_command_group.command("connect ", aliases={"/连接数据库 "})
list_databases = db_command_group.command("list ", aliases={"/列出数据库 "})
execute_command = db_command_group.command("run ", aliases={"/执行SQL命令 ", "/执行数据库命令 "})
drop_connection = db_command_group.command("dc ", aliases={"/断开连接 ", ("/db", "disconnect ")})
get_help = db_command_group.command("help ", aliases={"数据库帮助 "})


@new_connection.handle()
async def newConnection(args: Message = CommandArg()):
    global connection, cursor
    if path := args.extract_plain_text().strip():
        connection = sqlite3.connect(os.path.join("./reimei_databases/", path))
        cursor = connection.cursor()
        await new_connection.finish(f"哒！成功连接到数据库“{os.path.join('./reimei_databases/', path)}”！")
    else:
        await new_connection.finish("咱连接数据库得加上数据库文件名嗷！")


@list_databases.handle()
async def listDatabases():
    show_databases = "ReimeiBot下使用的数据库文件有如下这些哦："
    for database in os.listdir("./reimei_databases/"):
        show_databases += f"\n{database}"
    await list_databases.finish(show_databases)


@execute_command.handle()
async def executeCommand(args: Message = CommandArg()):
    if command := args.extract_plain_text().strip():
        cursor.execute(command)
        connection.commit()
        if response := cursor.fetchall():
            await execute_command.finish(str(response))
        else:
            await execute_command.finish("SQL命令成功执行！")
    else:
        await execute_command.finish("呜哇！没有命令怎么执行命令的啦？")


@drop_connection.handle()
async def dropConnection():
    connection.close()
    await drop_connection.finish("已成功与数据库断开连接！")


@get_help.handle()
async def getDatabaseHelp():
    await get_help.finish(await getHelp("reimeibot_plugin_database"))
