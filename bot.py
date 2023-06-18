import nonebot
import os
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

if not os.path.exists("ReimeiBotDatabases/"):
    os.mkdir("ReimeiBotDatabases/")

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