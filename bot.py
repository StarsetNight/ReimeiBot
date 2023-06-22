import nonebot
import os
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

if not os.path.exists("reimei_databases/"):
    os.mkdir("reimei_databases/")

nonebot.init()

driver = nonebot.get_driver()
config = driver.config
driver.register_adapter(ONEBOT_V11Adapter)

# SETTINGS
config.command_start = {""}
config.command_sep = {"."}
config.plugins_metadata = {}  # 插件元数据合集，类型为dict[str, PluginMetadata]


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(host="127.0.0.1", port=8080)