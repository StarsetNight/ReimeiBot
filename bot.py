# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

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