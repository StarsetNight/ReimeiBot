# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

from pydantic import BaseModel

from typing import ClassVar


class Config(BaseModel):
    """Plugin Config Here"""
    system_plugins: ClassVar[set[str]] = {"reimeibot_plugin_core", "reimeibot_plugin_settings"}  # 这些插件不能被禁用（其实禁用了也没用）
    docs: ClassVar[str] = """【ReimeiBot调试与插件管理系统】
/debug [string]：回复任意字符串string的内容，如无则回复“一切正常！”
/plugin.list：列出支持ReimeiBot协议的插件
/plugin.turn <package>：开关支持ReimeiBot协议的包名为package插件
/plugin.help <package>：获取支持ReimeiBot协议的包名为package插件的帮助文档
注意：不支持ReimeiBot协议的插件（例如Nonebot原生插件）不可以使用这个插件管理器哦！"""
