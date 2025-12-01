# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

from pydantic import BaseModel

from typing import ClassVar


class Config(BaseModel):
    """Plugin Config Here"""
    docs: ClassVar[str] = """【ReimeiBot GoCQAPI快捷调用】
    /call_api [api名] [json数据]"""
