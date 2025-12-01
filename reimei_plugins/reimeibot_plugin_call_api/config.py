# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    docs = """【ReimeiBot GoCQAPI快捷调用】
    /call_api [api名] [json数据]"""
