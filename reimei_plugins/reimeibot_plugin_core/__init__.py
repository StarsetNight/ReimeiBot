import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from .config import Config

nonebot.require("reimeibot_plugin_settings")

from reimei_api.rule import globalWhitelisted

# from nonebot_plugin_apscheduler import scheduler

driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

# 事件合集
debug = on_command("/debug", rule=globalWhitelisted,
                   permission=SUPERUSER, aliases={"/调试"}, priority=10, block=True)


@debug.handle()
async def debugHandle(args: Message = CommandArg()):
    if message := args.extract_plain_text():
        await debug.finish(Message(message))
    else:
        await debug.finish("欸？怎么不说话啊？")
