from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    # 权限设置
    allow_group = "global_config.maintainers"  # 允许字符串被引用的set集合以及SUPERUSER权限的人员使用此插件
    docs = """【ReimeiBot数据库管理系统】
/db.connect <file>：连接数据库
/db.run <SQL command>：执行命令
/db.dc：断开与数据库的连接
/db.help：获取数据库帮助"""
