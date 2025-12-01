# Copyright (c) 2023 StarsetNight, XuanRikka
# SPDX-License-Identifier: MIT

from pydantic import BaseModel

from typing import ClassVar


class Config(BaseModel):
    """Plugin Config Here"""

    # 机器人核心设置
    bot_nickname = {"宵宫", "夕"}  # 机器人昵称，自然语言处理会用到
    failsafe_group = ""  # 紧急备用群聊，不设置入数据库的原因是这是个很重要的设置

    # 文档
    docs: ClassVar[str] = """【ReimeiBot设定系统】
/failsafe <group>：将紧急安全后备群聊号设置为group
/whitelist.add <group>：添加白名单
/whitelist.list：列出白名单
/whitelist.remove <group>：移除白名单
/blacklist.add <qq>：添加黑名单
/blacklist.del <qq>：移除黑名单
/blacklist.lookup：列出黑名单
/permission.set <qq> <permission>：设置权限
/permission.get <qq>：获取权限
/permission.remove <qq>：移除权限
/settings.help：获取设定帮助"""

    # SQL命令
    # # 初始化表
    initialize_permission: ClassVar[str] = """CREATE TABLE IF NOT EXISTS PERMISSIONS(
    QQ TEXT UNIQUE NOT NULL,
    PERMISSION TEXT NOT NULL,
    REMARK TEXT
    );"""
    initialize_whitelist: ClassVar[str] = """CREATE TABLE IF NOT EXISTS WHITELIST(
    SESSION TEXT UNIQUE NOT NULL,
    REMARK TEXT
    );"""
    initialize_settings: ClassVar[str] = """CREATE TABLE IF NOT EXISTS SETTINGS(
    KEY TEXT UNIQUE NOT NULL,
    VALUE TEXT NOT NULL,
    REMARK TEXT
    );"""
    initialize_blacklist: ClassVar[str] = """CREATE TABLE IF NOT EXISTS BLACKLIST(
    QQ TEXT UNIQUE NOT NULL,
    REMARK TEXT
    );"""

    # # 白名单操作
    add_whitelist: ClassVar[str] = "INSERT INTO WHITELIST (SESSION) VALUES (?)"
    get_whitelist: ClassVar[str] = "SELECT SESSION FROM WHITELIST"
    del_whitelist: ClassVar[str] = "DELETE FROM WHITELIST WHERE SESSION = ?"

    # 权限操作
    set_permission: ClassVar[str] = "REPLACE INTO PERMISSIONS (QQ, PERMISSION) VALUES (?, ?)"
    list_permission: ClassVar[str] = "SELECT QQ FROM PERMISSIONS WHERE PERMISSION = ?"
    get_permission: ClassVar[str] = "SELECT PERMISSION FROM PERMISSIONS WHERE QQ = ?"
    del_permission: ClassVar[str] = "DELETE FROM PERMISSIONS WHERE QQ = ?"

    # # 数据库操作修改设置
    get_all_settings: ClassVar[str] = "SELECT KEY, VALUE FROM SETTINGS"
    add_option: ClassVar[str] = "INSERT INTO SETTINGS (KEY, VALUE, REMARK) VALUES (?, ?, ?)"
    get_option: ClassVar[str] = "SELECT VALUE FROM SETTINGS WHERE KEY = ?"
    set_option: ClassVar[str] = "UPDATE SETTINGS SET VALUE = ? WHERE KEY = ?"
    del_option: ClassVar[str] = "DELETE FROM SETTINGS WHERE KEY = ?"

    # 黑名单操作
    blacklist_add: ClassVar[str] = "INSERT INTO BLACKLIST (QQ) VALUES (?);"
    blacklist_del: ClassVar[str] = "DELETE FROM BLACKLIST WHERE QQ = ?;"
    blacklist_get: ClassVar[str] = "SELECT QQ FROM BLACKLIST"
