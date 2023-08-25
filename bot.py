import nonebot
import os
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot import logger
from nonebot.log import logger_id, default_filter
import sys

# 移除 NoneBot 默认的日志处理器
logger.remove(logger_id)
# 添加新的日志处理器
logger.add(
    sys.stdout,
    level=0,
    diagnose=True,
    format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> | {message}",
    filter=default_filter
)

if not os.path.exists("reimei_databases/"):
    os.mkdir("reimei_databases/")

nonebot.init()

driver = nonebot.get_driver()
config = driver.config
driver.register_adapter(ONEBOT_V11Adapter)

# SETTINGS
config.command_start = {""}
config.command_sep = {"."}


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(host="127.0.0.1", port=8080)