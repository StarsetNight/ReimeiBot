import nonebot
global_config = nonebot.get_driver().config


class PluginMetadata(object):
    plugin_name: str  # 插件名
    package_name: str  # 包名
    enabled: bool  # 启用开关
    plugin_docs: str  # 插件帮助文档
    developer: str  # 插件开发者

    def __init__(self, name: str, package: str, docs: str = "", developer: str = "佚名", enabled: bool = True):
        self.plugin_name = name
        self.package_name = package
        self.plugin_docs = docs
        self.developer = developer
        self.enabled = enabled

    def register(self):
        global_config.plugins_metadata[self.package_name] = self  # 注册此插件元数据至全局元数据列表

    def getHelp(self) -> str:
        """
        获取完整插件帮助
        """
        return f"""{self.plugin_name}
（{self.package_name}）
开发者：{self.developer}
文档：
{self.plugin_docs}"""
