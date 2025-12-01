# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    # 权限设置
    docs = """【ReimeiBot数据库管理系统】
/db.list：列出目录下全部数据库
/db.connect <file>：连接数据库
/db.run <SQL command>：执行命令
/db.dc：断开与数据库的连接
/db.help：获取数据库帮助"""
