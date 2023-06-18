from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    # 权限设置
    allow_group = "global_config.maintainers"  # 允许字符串被引用的set集合以及SUPERUSER权限的人员使用此插件
