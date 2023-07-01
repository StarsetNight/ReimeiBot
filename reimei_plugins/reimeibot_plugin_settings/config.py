from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""

    # 机器人核心设置
    bot_nickname = {"星酱", "星桑"}  # 机器人昵称，自然语言处理会用到
    failsafe_group = ""  # 紧急备用群聊，不设置入数据库的原因是这是个很重要的设置

    # 文档
    docs = """【ReimeiBot设定系统】
/failsafe <group>：将紧急安全后备群聊号设置为group
/whitelist.add <group>：添加白名单
/whitelist.list：列出白名单
/whitelist.remove <group>：移除白名单
/permission.set <qq> <permission>：设置权限
/permission.get <qq>：获取权限
/permission.remove <qq>：移除权限
/settings.help：获取设定帮助"""

    # SQL命令
    # # 初始化表
    initialize_permission = """CREATE TABLE IF NOT EXISTS PERMISSIONS(
    QQ TEXT UNIQUE NOT NULL,
    PERMISSION TEXT NOT NULL,
    REMARK TEXT
    );"""
    initialize_whitelist = """CREATE TABLE IF NOT EXISTS WHITELIST(
    SESSION TEXT UNIQUE NOT NULL,
    REMARK TEXT
    );"""
    initialize_settings = """CREATE TABLE IF NOT EXISTS SETTINGS(
    KEY TEXT UNIQUE NOT NULL,
    VALUE TEXT NOT NULL,
    REMARK TEXT
    );"""

    # # 白名单操作
    add_whitelist = "INSERT INTO WHITELIST (SESSION) VALUES (?)"
    get_whitelist = "SELECT SESSION FROM WHITELIST"
    del_whitelist = "DELETE FROM WHITELIST WHERE SESSION = ?"

    # 权限操作
    set_permission = "REPLACE INTO PERMISSIONS (QQ, PERMISSION) VALUES (?, ?)"
    list_permission = "SELECT QQ FROM PERMISSIONS WHERE PERMISSION = ?"
    get_permission = "SELECT PERMISSION FROM PERMISSIONS WHERE QQ = ?"
    del_permission = "DELETE FROM PERMISSIONS WHERE QQ = ?"

    # # 数据库操作修改设置
    get_all_settings = "SELECT KEY, VALUE FROM SETTINGS"
    add_option = "INSERT INTO SETTINGS (KEY, VALUE, REMARK) VALUES (?, ?, ?)"
    get_option = "SELECT VALUE FROM SETTINGS WHERE KEY = ?"
    set_option = "UPDATE SETTINGS SET VALUE = ? WHERE KEY = ?"
    del_option = "DELETE FROM SETTINGS WHERE KEY = ?"
