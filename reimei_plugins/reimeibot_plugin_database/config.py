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
    # 权限设置
    allow_group = "global_config.maintainers"  # 允许字符串被引用的set集合以及SUPERUSER权限的人员使用此插件
    docs = """【ReimeiBot数据库管理系统】
/db.list：列出目录下全部数据库
/db.connect <file>：连接数据库
/db.run <SQL command>：执行命令
/db.dc：断开与数据库的连接
/db.help：获取数据库帮助"""
