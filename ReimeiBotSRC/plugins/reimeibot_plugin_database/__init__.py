import nonebot
import os
import sqlite3
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

from .config import Config
from ReimeiBotSRC.plugins.reimeibot_plugin_core.rule import globalWhitelisted
from ._permission import isAllowed

driver = nonebot.get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

connection: sqlite3.Connection
cursor: sqlite3.Cursor

new_connection = on_command(("/db", "connect"), rule=globalWhitelisted,
                            permission=isAllowed, aliases={"/连接数据库"}, priority=6, block=True)
execute_command = on_command(("/db", "run"), rule=globalWhitelisted,
                             permission=isAllowed, aliases={"/执行SQL命令", "/执行数据库命令"}, priority=6, block=True)
drop_connection = on_command(("/db", "dc"), rule=globalWhitelisted,
                             permission=isAllowed, aliases={"/断开连接", ("/db", "disconnect")}, priority=6, block=True)


@new_connection.handle()
async def newConnection(args: Message = CommandArg()):
    global connection, cursor
    if path := args.extract_plain_text().strip():
        connection = sqlite3.connect(os.path.join("./ReimeiBotDatabases/", path))
        cursor = connection.cursor()
        await new_connection.finish(f"哒！成功连接到数据库“{os.path.join('./ReimeiBotDatabases/', path)}”！")
    else:
        await new_connection.finish("咱连接数据库得加上数据库文件名嗷！")


@execute_command.handle()
async def executeCommand(args: Message = CommandArg()):
    if command := args.extract_plain_text().strip():
        cursor.execute(command)
        if response := cursor.fetchall():
            await new_connection.finish(str(response))
        else:
            await new_connection.finish("SQL命令成功执行！")
    else:
        await new_connection.finish("呜哇！没有命令怎么执行命令的啦？")


@drop_connection.handle()
async def dropConnection():
    connection.close()
    await drop_connection.finish("已成功与数据库断开连接！")
