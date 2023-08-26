"""
项目名称：ReimeiBot
项目作者：StarsetNight（化名：何星夕，网名：星夕Starset）
许可协议：MIT许可证

版权所有 (c) 2023 星夕Starset
依据MIT许可证效力，衍生项目需保证本版权声明原封不动，可以增添“原”前缀以免与您的衍生项目混淆
"""

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    system_plugins = {"reimeibot_plugin_core", "reimeibot_plugin_settings"}  # 这些插件不能被禁用（其实禁用了也没用）
    docs = """【ReimeiBot调试与插件管理系统】
/debug [string]：回复任意字符串string的内容，如无则回复“一切正常！”
/plugin.list：列出支持ReimeiBot协议的插件
/plugin.turn <package>：开关支持ReimeiBot协议的包名为package插件
/plugin.help <package>：获取支持ReimeiBot协议的包名为package插件的帮助文档
注意：不支持ReimeiBot协议的插件（例如Nonebot原生插件）不可以使用这个插件管理器哦！"""
