# ReimeiBot文档

## 如何将自己的插件注册为支持ReimeiBot协议的插件，即适配ReimeiBot协议？
这是简单的，使用我们提供的`reimeiapi.metadata.PluginMetadata`类即可完成接入，现在我们尝试一下接入。

## 创建NoneBot插件

### 插件核心

万事得有一个开头，请在`reimei_plugins`目录下创建一个Python包，即一个包含`__init__.py`文件的文件夹。我们将暂时命名它为`reimeibot_plugin_test`。

接下来，在`__init__.py`文件中，你可以编写任何符合**NoneBot协议**的代码。但是请务必记住添加以下代码行，以将插件注册到ReimeiBot核心：

```python
from reimei_api.metadata import PluginMetadata
from .config import Config
config = Config.parse_obj()  # 参数可以写入nonebot.get_driver().config
PluginMetadata("ReimeiBot插件测试", "reimeibot_plugin_test", config.docs, "Advanced_Killer", True).register()
```

这一行代码将使用`PluginMetadata`类创建一个插件元数据对象，并注册插件到ReimeiBot的全局元数据列表。这样，ReimeiBot核心就能够正确识别和加载你的插件。

稍后我们将详细介绍`PluginMetadata`类的工作原理，并说明如何使用它来自定义和扩展你的插件。

请确保在编写插件代码之前，已正确安装和配置了NoneBot环境。以上是创建NoneBot插件的一个简单示例，通过这种方式，你可以轻松将你的插件注册到ReimeiBot，并利用NoneBot协议的功能进行开发和交互。

敬请期待后续我们将详细讲解`PluginMetadata`类的使用方法以及更多有关插件开发的内容。祝你插件开发顺利！

### 插件设定

接着创建 `config.py` 用于插件设定，将以下代码写入其中：

```python
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    docs = "【ReimeiBot测试】"
```

这段代码定义了一个名为 `Config` 的类，它继承自 `BaseModel`，用于配置插件的设定。在示例中，我们为 `docs` 设定了一个默认值 `"【ReimeiBot测试】"`，你可以根据实际需求修改和扩展这个类。

接下来，创建 `_rule.py` 文件，用于插件内部判断插件是否启用，将以下代码写入其中：

```python
import nonebot
global_config = nonebot.get_driver().config

async def isEnabled():
    return global_config.plugins_metadata["reimeibot_plugin_test"]
```

这段代码导入了 `nonebot` 模块，并使用 `nonebot.get_driver().config` 获取全局配置信息。`isEnabled()` 函数用于判断插件是否启用，它通过访问全局元数据列表中的插件信息来确定插件的启用状态。

请注意，你需要将代码中的 `"reimeibot_plugin_test"` 修改为你实际的插件包名，以确保正确获取插件的启用状态。

通过以上步骤，你已经创建了一个配置文件和一个用于判断插件启用状态的模块。你可以根据需求修改这些文件，添加更多的设定和功能来满足你的插件开发需求。记得确保文件名和包名与你的插件实际情况相匹配。

### 插件的文件结构

现在，`reimei_plugins` 文件夹的架构如下所示：

```
reimei_plugins
├── （其他的ReimeiBot默认插件）
└── reimeibot_plugin_test
    ├── __init__.py
    ├── config.py
    └── _rule.py
```

在 `reimei_plugins` 文件夹中，除了 `reimeibot_plugin_test` 文件夹外，可能还包含其他的ReimeiBot默认插件。

在 `reimeibot_plugin_test` 文件夹中，有以下文件：

- `__init__.py`：这是插件的入口文件，你可以在其中编写符合NoneBot协议的代码，并注册插件元数据到ReimeiBot核心。
- `config.py`：这是用于插件设定的文件，你可以在其中定义和配置插件的设定。
- `_rule.py`：这是用于判断插件是否启用的模块文件，你可以在其中编写逻辑以确定插件是否处于启用状态。

请确保文件夹和文件的名称、位置和结构与上述描述一致，以确保插件能够正确加载和运行。

现在，你已经创建了插件的基本架构和配置文件，可以继续开发插件的功能和交互逻辑。祝你在插件开发过程中取得好成果！

## 我们做了什么？

首先，我们创建了一个支持NoneBot协议的插件包，其中包含了`__init__.py`和`config.py`两个文件，用于插件的基本运作。

在`__init__.py`中，我们编写了一些符合NoneBot协议的函数代码段，并创建了`PluginMetadata`类的一个实例，将其注册到ReimeiBot核心。

接着，我们在`config.py`和`_rule.py`中添加了一些附加内容，使插件成功接入ReimeiBot并支持ReimeiBot协议。

现在，让我们来详细讲解一下`PluginMetadata`类的使用方法。

## PluginMetadata类
### 成员变量
- `plugin_name`：插件的名称，类型为字符串（`str`）。
- `package_name`：插件所属的包名，类型为字符串（`str`）。
- `enabled`：插件的启用开关，类型为布尔值（`bool`）。
- `plugin_docs`：插件的帮助文档，类型为字符串（`str`）。
- `developer`：插件的开发者，类型为字符串（`str`）。

### 方法
- `__init__(self, name: str, package: str, docs: str = "", developer: str = "佚名", enabled: bool = True)`：初始化方法，用于设置插件的名称、包名、帮助文档、开发者和启用状态。
- `register(self)`：注册方法，将插件的元数据注册到全局元数据列表。
- `getHelp(self) -> str`：获取完整插件帮助文档的方法，返回包括插件名称、包名、开发者和帮助文档内容的字符串（`str`）。

通过使用`PluginMetadata`类，我们可以轻松地定义插件的元数据，并将其注册到ReimeiBot的全局元数据列表中。这样，ReimeiBot就能正确识别和加载我们的插件。

请确保在使用`PluginMetadata`类之前，已正确安装和配置了NoneBot环境，并按照文档和示例代码的指导进行操作。

通过以上步骤，我们成功创建了一个插件，并将其注册到了ReimeiBot核心。接下来，我们可以继续开发和扩展插件的功能，与ReimeiBot进行交互，并为用户提供更丰富的体验。祝你在插件开发的过程中取得成功！