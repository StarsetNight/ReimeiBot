"""
项目名称：ReimeiBot
项目作者：StarsetNight（化名：何星夕，网名：星夕Starset）
许可协议：MIT许可证

版权所有 (c) 2023 星夕Starset
依据MIT许可证效力，衍生项目需保证本版权声明原封不动，可以增添“原”前缀以免与您的衍生项目混淆
"""

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
