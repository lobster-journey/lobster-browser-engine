# Lobster Browser Engine - API文档

> 本文档为Agent友好格式，包含所有可执行的接口说明

---

## 核心类

### BrowserEngine

主引擎类，管理浏览器连接和操作执行。

#### 初始化

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig

# 方式1：默认配置
engine = BrowserEngine()

# 方式2：自定义配置
config = EngineConfig()
config.connection.cdp_url = "http://127.0.0.1:9222"
config.screenshot.enabled = True
engine = BrowserEngine(config)
```

#### 方法

##### `connect() -> None`

连接到浏览器。

```python
await engine.connect()
```

**异常**：
- `ConnectionException` - 连接失败

---

##### `disconnect() -> None`

断开浏览器连接。

```python
await engine.disconnect()
```

---

##### `execute_flow(flow_name: str, params: Optional[Dict] = None) -> FlowResult`

执行预定义流程。

**参数**：
- `flow_name` (str) - 流程名称（不含.json扩展名）
- `params` (Optional[Dict]) - 流程参数，默认为None

**返回**：
- `FlowResult` - 流程执行结果

**示例**：

```python
# 无参数执行
result = await engine.execute_flow("login_flow")

# 带参数执行
result = await engine.execute_flow("form_fill", {
    "username": "user@example.com",
    "password": "password123"
})

# 查看结果
if result.success:
    print(f"✅ 执行成功，耗时：{result.get_duration_human()}")
    print(f"步骤数：{result.steps_executed}")
else:
    print(f"❌ 执行失败：{result.error}")
    print(f"失败步骤：{result.error_step}")
```

---

##### `get_page() -> Page`

获取当前页面对象。

**返回**：
- `playwright.async_api.Page` - Playwright页面对象

**异常**：
- `ConnectionException` - 浏览器未连接

**示例**：

```python
page = engine.get_page()
await page.goto("https://example.com")
await page.screenshot(path="screenshot.png")
```

---

#### 上下文管理器

支持 `async with` 语法。

```python
async with BrowserEngine() as engine:
    page = engine.get_page()
    await page.goto("https://example.com")
# 自动断开连接
```

---

## 操作执行器

### ActionFactory

操作工厂类，创建操作执行器。

#### `create(action_type: str, page: Page, config: EngineConfig) -> BaseActionExecutor`

创建操作执行器。

**参数**：
- `action_type` (str) - 操作类型
- `page` (Page) - Playwright页面对象
- `config` (EngineConfig) - 引擎配置

**返回**：
- `BaseActionExecutor` - 操作执行器实例

**支持的操作类型**：
- `navigate` - 导航
- `click` - 点击
- `fill` - 填充
- `wait` - 等待
- `screenshot` - 截图
- `evaluate` - 执行JavaScript
- `press` - 按键
- `scroll` - 滚动
- `select` - 选择
- `upload` - 上传
- `download` - 下载
- `hover` - 悬停
- `drag` - 拖拽
- `keyboard` - 键盘操作
- `mouse` - 鼠标操作
- `dialog` - 对话框
- `cookie` - Cookie操作

**示例**：

```python
from lobster_browser_engine.actions import ActionFactory

# 创建点击执行器
click_executor = ActionFactory.create("click", page, config)

# 执行点击
result = await click_executor.execute({
    "locator": "text=登录",
    "strategy": "text",
    "timeout": 5000
})

if result.success:
    print(f"✅ 点击成功，耗时：{result.duration}ms")
else:
    print(f"❌ 点击失败：{result.error}")
```

---

## 操作执行器详解

### NavigateAction

导航操作。

**参数**：
```python
{
    "url": "https://example.com",  # 必需
    "wait_until": "networkidle",   # 可选：load/domcontentloaded/networkidle
    "timeout": 60000,              # 可选，毫秒
    "screenshot": true             # 可选，是否截图
}
```

**示例**：
```python
executor = ActionFactory.create("navigate", page, config)
result = await executor.execute({
    "url": "https://example.com",
    "wait_until": "networkidle"
})
```

---

### ClickAction

点击操作。

**参数**：
```python
{
    "locator": "text=登录",  # 必需
    "strategy": "text",      # 可选：text/css/xpath，默认auto
    "timeout": 5000,         # 可选，毫秒
    "click_count": 1,        # 可选，点击次数
    "button": "left",        # 可选：left/right/middle
    "modifiers": []          # 可选：Alt/Control/Meta/Shift
}
```

**示例**：
```python
executor = ActionFactory.create("click", page, config)
result = await executor.execute({
    "locator": "button.submit",
    "strategy": "css",
    "click_count": 1
})
```

---

### FillAction

填充操作。

**参数**：
```python
{
    "locator": "input[name='username']",  # 必需
    "value": "user@example.com",          # 必需
    "clear_first": true,                  # 可选，是否先清空
    "timeout": 5000                       # 可选，毫秒
}
```

**示例**：
```python
executor = ActionFactory.create("fill", page, config)
result = await executor.execute({
    "locator": "input[name='username']",
    "value": "user@example.com",
    "clear_first": true
})
```

---

### WaitAction

等待操作。

**参数**：
```python
{
    # 方式1：等待时间
    "time": 3,  # 秒
    
    # 方式2：等待元素
    "locator": ".loading",
    "state": "hidden",  # visible/hidden/attached/detached
    "timeout": 10000,
    
    # 方式3：等待URL
    "url": "https://example.com/success"
}
```

**示例**：
```python
# 等待3秒
await executor.execute({"time": 3})

# 等待元素出现
await executor.execute({
    "locator": ".user-info",
    "state": "visible",
    "timeout": 10000
})

# 等待URL变化
await executor.execute({
    "url": "https://example.com/dashboard"
})
```

---

### ScreenshotAction

截图操作。

**参数**：
```python
{
    "path": "/tmp/screenshot.png",  # 可选，默认自动生成
    "full_page": false,             # 可选，是否全页截图
    "clip": {                       # 可选，裁剪区域
        "x": 0,
        "y": 0,
        "width": 800,
        "height": 600
    }
}
```

**示例**：
```python
executor = ActionFactory.create("screenshot", page, config)
result = await executor.execute({
    "path": "/tmp/screenshot.png",
    "full_page": true
})
print(f"截图保存到：{result.data['path']}")
```

---

### EvaluateAction

执行JavaScript。

**参数**：
```python
{
    "script": "document.querySelector('#btn').click()",  # 必需
    "arg": null  # 可选，传递给脚本的参数
}
```

**示例**：
```python
executor = ActionFactory.create("evaluate", page, config)
result = await executor.execute({
    "script": "() => document.title"
})
print(f"页面标题：{result.data['result']}")
```

---

### ScrollAction

滚动操作。

**参数**：
```python
{
    "direction": "down",  # up/down/top/bottom
    "distance": 300,      # 像素
    "selector": "#content",  # 可选，指定滚动元素
    "smooth": true
}
```

**示例**：
```python
# 向下滚动300像素
await executor.execute({
    "direction": "down",
    "distance": 300
})

# 滚动到页面底部
await executor.execute({
    "direction": "bottom"
})
```

---

### SelectAction

选择操作。

**参数**：
```python
{
    "selector": "select#country",  # 必需
    "value": "china",              # 方式1：按值选择
    "label": "中国",                # 方式2：按标签选择
    "index": 0                     # 方式3：按索引选择
}
```

**示例**：
```python
executor = ActionFactory.create("select", page, config)
result = await executor.execute({
    "selector": "select#country",
    "value": "china"
})
```

---

### UploadAction

上传操作。

**参数**：
```python
{
    "selector": "input[type='file']",        # 必需
    "files": ["/path/to/file1.jpg", ...],   # 必需，文件路径列表
    "timeout": 30000
}
```

**示例**：
```python
executor = ActionFactory.create("upload", page, config)
result = await executor.execute({
    "selector": "input[type='file']",
    "files": ["/tmp/image.jpg"]
})
```

---

### CookieAction

Cookie操作。

**参数**：
```python
{
    "action": "get/set/delete/clear",  # 必需
    "name": "sessionid",               # get/delete时使用
    "value": "xxx",                    # set时使用
    "domain": ".example.com",          # 可选
    "cookies": [...]                   # set批量时使用
}
```

**示例**：
```python
# 获取所有Cookie
result = await executor.execute({"action": "get"})

# 设置Cookie
await executor.execute({
    "action": "set",
    "name": "token",
    "value": "abc123",
    "domain": ".example.com"
})

# 清除所有Cookie
await executor.execute({"action": "clear"})
```

---

## 流程管理

### FlowManager

流程管理器，负责流程的CRUD操作。

```python
from lobster_browser_engine.flows import FlowManager

manager = FlowManager()

# 创建流程
manager.create({
    "name": "login_flow",
    "version": "1.0.0",
    "steps": [...]
})

# 读取流程
flow = manager.read("login_flow")

# 更新流程
manager.update("login_flow", {"version": "1.1.0"})

# 删除流程
manager.delete("login_flow")

# 列出所有流程
flows = manager.list_flows()
```

---

### 流程配置格式

```json
{
  "name": "flow_name",
  "version": "1.0.0",
  "description": "流程描述",
  "params": {
    "username": {
      "type": "string",
      "required": true,
      "default": ""
    }
  },
  "steps": [
    {
      "step_id": 1,
      "name": "步骤名称",
      "description": "步骤描述",
      "action": "navigate",
      "params": {
        "url": "https://example.com"
      },
      "optional": false,
      "wait_after": 1.0,
      "condition": {
        "type": "element_exists",
        "selector": ".element"
      }
    }
  ],
  "before_hooks": [],
  "after_hooks": []
}
```

---

## 结果对象

### ActionResult

操作执行结果。

```python
result = await executor.execute(params)

# 属性
result.success       # bool - 是否成功
result.action_type   # ActionType - 操作类型
result.data          # Optional[Any] - 返回数据
result.screenshot    # Optional[str] - 截图路径
result.error         # Optional[str] - 错误信息
result.duration      # float - 执行时长（毫秒）
result.retry_count   # int - 重试次数

# 方法
result.is_successful()          # 判断是否成功
result.has_screenshot()         # 判断是否有截图
result.get_duration_seconds()   # 获取执行时长（秒）
result.get_duration_human()     # 获取人类可读的执行时长
```

---

### FlowResult

流程执行结果。

```python
result = await engine.execute_flow("login_flow")

# 属性
result.success           # bool - 是否成功
result.flow_name         # str - 流程名称
result.status            # FlowStatus - 流程状态
result.steps_total       # int - 总步骤数
result.steps_executed    # int - 执行步骤数
result.steps_success     # int - 成功步骤数
result.steps_failed      # int - 失败步骤数
result.error             # Optional[str] - 错误信息
result.error_step        # Optional[int] - 失败步骤ID
result.duration          # float - 执行时长（毫秒）
result.step_results      # List[StepResult] - 步骤结果列表

# 方法
result.is_successful()          # 判断是否成功
result.get_duration_human()     # 获取人类可读的执行时长
result.get_success_rate()       # 获取成功率
result.get_failed_steps()       # 获取失败的步骤
result.get_summary()            # 获取摘要信息
result.to_json()                # 转换为JSON字符串
result.save_to_file(path)       # 保存到文件
```

---

## 配置

### EngineConfig

主配置类。

```python
from lobster_browser_engine.config import EngineConfig

config = EngineConfig()

# 连接配置
config.connection.cdp_url = "http://127.0.0.1:9222"
config.connection.headless = False
config.connection.user_data_dir = "/tmp/browser_profile"

# 超时配置
config.timeout.default_timeout = 30000
config.timeout.navigation_timeout = 60000

# 重试配置
config.retry.enabled = True
config.retry.default_retry_times = 3

# 截图配置
config.screenshot.enabled = True
config.screenshot.auto_screenshot_on_error = True

# 日志配置
config.log.enabled = True
config.log.level = LogLevel.DEBUG

# 性能配置
config.performance.slow_mo = 0
config.performance.default_wait_after = 1.0
```

---

## 异常

### 异常层次

```
BrowserEngineException (基类)
├── ConnectionException
├── ActionException
│   ├── ActionNotSupportedException
│   ├── ActionFailedException
│   └── ...
├── FlowException
│   ├── FlowNotFoundException
│   ├── FlowExecutionException
│   └── FlowValidationException
└── ...
```

### 异常处理

```python
from lobster_browser_engine.exceptions import (
    BrowserEngineException,
    ConnectionException,
    FlowNotFoundException
)

try:
    result = await engine.execute_flow("login_flow")
except ConnectionException as e:
    print(f"连接错误：{str(e)}")
except FlowNotFoundException as e:
    print(f"流程未找到：{str(e)}")
except BrowserEngineException as e:
    print(f"引擎错误：{str(e)}")
```

---

## 完整示例

### 示例：自动登录流程

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig
import asyncio

async def auto_login():
    # 配置
    config = EngineConfig()
    config.connection.user_data_dir = "/tmp/login_profile"
    config.screenshot.enabled = True
    
    # 创建引擎
    async with BrowserEngine(config) as engine:
        page = engine.get_page()
        
        # 1. 导航
        await page.goto("https://example.com/login")
        
        # 2. 填充用户名
        await page.fill("input[name='username']", "user@example.com")
        
        # 3. 填充密码
        await page.fill("input[name='password']", "password123")
        
        # 4. 点击登录
        await page.click("button[type='submit']")
        
        # 5. 等待登录成功
        await page.wait_for_selector(".user-dashboard", timeout=10000)
        
        # 6. 截图
        await page.screenshot(path="/tmp/login_success.png")
        
        print("✅ 登录成功！")

asyncio.run(auto_login())
```

---

**API文档持续更新中...**
