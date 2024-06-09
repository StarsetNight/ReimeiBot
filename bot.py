"""
项目名称：ReimeiBot
项目作者：StarsetNight（化名：何星夕，网名：星夕Starset）
许可协议：MIT许可证

版权所有 (c) 2023 星夕Starset
依据MIT许可证效力，衍生项目需保证本版权声明原封不动，可以增添“原”前缀以免与您的衍生项目混淆
"""

import nonebot, os
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# 确认数据文件夹存在
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
    nonebot.run()