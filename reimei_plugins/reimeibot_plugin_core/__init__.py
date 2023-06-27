import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from .config import Config

from reimei_api.rule import globalWhitelisted
from reimei_api.permission import isMaintainer
from reimei_api.metadata import PluginMetadata

driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)

# 注册插件
PluginMetadata("黎明核心", "reimeibot_plugin_core", config.docs, "Advanced_Killer", True).register()

# 事件合集
debug = on_command("/debug", rule=globalWhitelisted,
                   permission=SUPERUSER, aliases={"/调试"}, priority=10, block=True)
plugin_list = on_command(("/plugin", "list"), rule=globalWhitelisted,
                         aliases={"/插件列表"}, priority=10, block=True)
plugin_help = on_command(("/plugin", "help"), rule=globalWhitelisted,
                         aliases={"/帮助", "/help"}, priority=10, block=True)
plugin_inspect = on_command(("/plugin", "inspect"), rule=globalWhitelisted,
                            permission=isMaintainer, aliases={"/开关插件"}, priority=10, block=True)


@debug.handle()
async def debugHandle(args: Message = CommandArg()):
    if message := args.extract_plain_text():
        await debug.finish(Message(message))
    else:
        await debug.finish("一切正常！")


@plugin_list.handle()
async def pluginList():
    metadata: PluginMetadata
    string_list = "====ReimeiBot插件列表====\n"
    for index, metadata in enumerate(global_config.plugins_metadata.values()):
        string_list += (f"{index}. {metadata.plugin_name}（{metadata.package_name}）"
                        f"[{'启用' if metadata else '禁用'}]\n\n")
    await plugin_list.finish(string_list)


@plugin_help.handle()
async def pluginHelp(args: Message = CommandArg()):
    if package := args.extract_plain_text():
        if package in global_config.plugins_metadata:
            await plugin_help.finish(global_config.plugins_metadata[package].getHelp())
        else:
            await plugin_help.finish(f"插件包 {package} 不存在哦~")
    else:
        await plugin_help.finish(config.docs)


@plugin_inspect.handle()
async def pluginInspect(args: Message = CommandArg()):
    if package := args.extract_plain_text():
        if package in config.system_plugins:
            await plugin_inspect.finish(f"插件包 {package} 为黎明系统插件，不可禁用哦！")
        if package in global_config.plugins_metadata:
            global_config.plugins_metadata[package].enabled = not global_config.plugins_metadata[package]
            await plugin_inspect.finish(f"插件包 {package} 的开关已成功"
                                        f"{'启用' if global_config.plugins_metadata[package] else '禁用'}"
                                        f"了哦！")
        else:
            await plugin_help.finish(f"插件包 {package} 不存在哦~")
    else:
        await plugin_help.finish("请指定插件包呐~")
