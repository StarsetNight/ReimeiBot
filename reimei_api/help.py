import nonebot


async def getHelp(package: str) -> str:
    if plugin := nonebot.get_plugin(package):
        if plugin.metadata:
            return f"""{plugin.metadata.name}
（{plugin.name}）
文档：
{plugin.metadata.usage}"""
        else:
            return f"""{plugin.name}
文档：
插件作者并未编写文档……"""
    else:
        return "插件不存在……"
