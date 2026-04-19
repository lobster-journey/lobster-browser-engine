# 浏览器操作引擎 API 文档

> 版本：v0.1.0  
> 更新时间：2026-04-19

---

## 目录

- [核心类](#核心类)
  - [BrowserEngine](#browserengine)
  - [FlowExecutor](#flowexecutor)
  - [ElementLocator](#elementlocator)
- [操作类型](#操作类型)
- [元素定位](#元素定位)
- [流程配置](#流程配置)
- [返回结果](#返回结果)
- [错误处理](#错误处理)

---

## 核心类

### BrowserEngine

主引擎类，提供完整的浏览器操作能力。

#### 初始化

```python
from browser_engine import BrowserEngine

engine = BrowserEngine(
    cdp_url="http://127.0.0.1:9222",  # CDP连接地址
    headless=False,                    # 是否无头模式
    timeout=30000,                     # 默认超时时间（毫秒）
    retry_times=3,                     # 失败重试次数
    screenshot_dir="/tmp/screenshots"  # 截图保存目录
)
```

#### 主要方法

##### execute_flow()

执行预定义的流程。

```python
result = engine.execute_flow(
    flow_name="jimeng_login",  # 流程名称
    params={                    # 可选参数
        "username": "user@example.com",
        "password": "password"
    }
)
```

**参数**：
- `flow_name` (str): 流程名称，对应 `flows/` 目录下的配置文件
- `params` (dict, 可选): 流程参数，用于动态配置

**返回**：
- `FlowResult`: 流程执行结果对象

**示例**：

```python
# 即梦登录
result = engine.execute_flow("jimeng_login")

# 检查结果
if result.success:
    print("登录成功")
    # 获取最后一张截图
    screenshot = result.screenshots[-1]
else:
    print(f"登录失败: {result.error}")
```

##### execute_custom_flow()

执行自定义流程。

```python
custom_flow = {
    "name": "my_custom_flow",
    "steps": [
        {"action": "navigate", "url": "https://example.com"},
        {"action": "screenshot"}
    ]
}

result = engine.execute_custom_flow(custom_flow)
```

**参数**：
- `flow` (dict): 流程配置对象

**返回**：
- `FlowResult`: 流程执行结果对象

##### connect()

连接到浏览器。

```python
engine.connect()
```

##### disconnect()

断开浏览器连接。

```python
engine.disconnect()
```

##### get_page()

获取当前页面对象。

```python
page = engine.get_page()
```

**返回**：
- `Page`: Playwright Page 对象

---

### FlowExecutor

流程执行器，负责执行具体的操作步骤。

#### 主要方法

##### execute_step()

执行单个操作步骤。

```python
executor = FlowExecutor(page)
result = executor.execute_step({
    "action": "click",
    "locator": "text=登录",
    "wait_after": 2
})
```

**参数**：
- `step` (dict): 步骤配置

**返回**：
- `StepResult`: 步骤执行结果

---

### ElementLocator

元素定位器，提供多种定位策略。

#### 定位方法

##### by_css()

CSS选择器定位。

```python
locator = ElementLocator(page)
element = locator.by_css("#login-button")
```

##### by_text()

文本内容定位。

```python
element = locator.by_text("登录")
```

##### by_xpath()

XPath定位。

```python
element = locator.by_xpath("//button[contains(text(), '登录')]")
```

##### by_role()

ARIA角色定位。

```python
element = locator.by_role("button", name="登录")
```

---

## 操作类型

### navigate

导航到指定URL。

```json
{
  "action": "navigate",
  "url": "https://example.com",
  "wait_until": "networkidle"
}
```

**参数**：
- `url` (str): 目标URL
- `wait_until` (str, 可选): 等待条件，可选值：
  - `load`: 等待 load 事件
  - `domcontentloaded`: 等待 DOMContentLoaded 事件
  - `networkidle`: 等待网络空闲（默认）

---

### click

点击元素。

```json
{
  "action": "click",
  "locator": "text=登录",
  "timeout": 5000,
  "wait_after": 2
}
```

**参数**：
- `locator` (str): 元素定位器
- `timeout` (int, 可选): 超时时间（毫秒），默认5000
- `wait_after` (int, 可选): 点击后等待时间（秒）

**定位器格式**：
- `text=登录`: 文本定位（推荐）
- `css=#btn`: CSS选择器
- `xpath=//button`: XPath表达式
- `role=button`: ARIA角色

---

### fill

填充输入框。

```json
{
  "action": "fill",
  "locator": "css=input[name='username']",
  "value": "user@example.com",
  "clear_first": true,
  "wait_after": 1
}
```

**参数**：
- `locator` (str): 元素定位器
- `value` (str): 要填充的值
- `clear_first` (bool, 可选): 是否先清空，默认true
- `wait_after` (int, 可选): 填充后等待时间（秒）

---

### wait

等待时间或元素。

#### 等待时间

```json
{
  "action": "wait",
  "time": 3
}
```

#### 等待元素出现

```json
{
  "action": "wait",
  "locator": "text=登录",
  "timeout": 10000
}
```

#### 等待URL变化

```json
{
  "action": "wait",
  "url": "https://example.com/dashboard",
  "timeout": 10000
}
```

**参数**：
- `time` (int): 等待时间（秒）
- `locator` (str): 等待的元素
- `url` (str): 等待的URL
- `timeout` (int, 可选): 超时时间（毫秒）

---

### screenshot

截图。

```json
{
  "action": "screenshot",
  "path": "/tmp/screenshot.png",
  "full_page": false
}
```

**参数**：
- `path` (str, 可选): 保存路径，不指定则自动生成
- `full_page` (bool, 可选): 是否全页截图，默认false

---

### evaluate

执行JavaScript。

```json
{
  "action": "evaluate",
  "script": "document.querySelector('#login-btn').click()",
  "wait_after": 2
}
```

**参数**：
- `script` (str): JavaScript代码
- `wait_after` (int, 可选): 执行后等待时间（秒）

---

### press

按键操作。

```json
{
  "action": "press",
  "key": "Enter",
  "wait_after": 1
}
```

**参数**：
- `key` (str): 按键名称，如 `Enter`, `Escape`, `F5` 等
- `wait_after` (int, 可选): 按键后等待时间（秒）

---

### refresh

刷新页面。

```json
{
  "action": "refresh",
  "wait_until": "networkidle"
}
```

**参数**：
- `wait_until` (str, 可选): 等待条件，默认 `networkidle`

---

## 元素定位

### 定位器格式

定位器使用统一格式：`策略=值`

#### 文本定位（推荐）

```
text=登录
text=刷新
```

**优点**：
- 最可靠
- 不受页面结构变化影响
- 适合包含特定文本的元素

#### CSS选择器

```
css=#login-button
css=.btn-primary
css=div.container > button
```

**优点**：
- 精确定位
- 性能好
- 适合固定结构的元素

#### XPath

```
xpath=//button[contains(text(), '登录')]
xpath=//div[@class='container']//button[1]
```

**优点**：
- 灵活强大
- 适合复杂结构

#### ARIA角色

```
role=button
role=link[name='登录']
```

**优点**：
- 语义化
- 可访问性好

---

### 定位器优先级

推荐使用顺序：

1. **text=...** - 最可靠，优先使用
2. **role=...** - 语义化，适合交互元素
3. **css=...** - 精确定位，适合固定结构
4. **xpath=...** - 最后选择，灵活性最高

---

### 元素等待策略

所有定位操作都会自动等待元素出现，默认超时5秒。

可配置：

```json
{
  "action": "click",
  "locator": "text=登录",
  "timeout": 10000,
  "wait_for": "visible"
}
```

**wait_for 选项**：
- `visible`: 等待元素可见（默认）
- `hidden`: 等待元素隐藏
- `attached`: 等待元素附加到DOM
- `detached`: 等待元素从DOM分离

---

## 流程配置

### 流程文件格式

流程配置使用JSON格式，存放在 `flows/` 目录。

#### 完整示例

```json
{
  "name": "jimeng_login",
  "version": "1.0.0",
  "description": "即梦AI登录流程",
  "success_rate": "100%",
  "author": "龙虾智能体",
  "created_at": "2026-04-19",
  "tags": ["login", "jimeng", "douyin"],
  
  "params": {
    "wait_qr_code": {
      "type": "number",
      "default": 30,
      "description": "等待扫码时间（秒）"
    }
  },
  
  "steps": [
    {
      "action": "press",
      "key": "F5",
      "wait_after": 3,
      "description": "刷新页面"
    },
    {
      "action": "click",
      "locator": "css=#SiderMenuLogin > div > div",
      "wait_after": 2,
      "description": "点击登录按钮",
      "retry": 3
    },
    {
      "action": "click",
      "locator": "css=.lv-menu-item.lv-menu-item-size-default.login-menu-item-Yoy61o",
      "wait_after": 2,
      "description": "点击抖音登录"
    },
    {
      "action": "wait",
      "time": 3,
      "description": "等待二维码弹窗加载"
    },
    {
      "action": "click",
      "locator": "text=刷新",
      "wait_after": 2,
      "description": "点击刷新二维码",
      "optional": false
    },
    {
      "action": "screenshot",
      "description": "截取二维码"
    },
    {
      "action": "wait",
      "time": "{{params.wait_qr_code}}",
      "description": "等待用户扫码"
    },
    {
      "action": "evaluate",
      "script": "const loginBtns = Array.from(document.querySelectorAll('*')).filter(el => el.textContent.trim() === '登录'); return loginBtns.length === 0;",
      "description": "验证登录成功（登录按钮消失）"
    }
  ],
  
  "on_success": {
    "action": "screenshot",
    "description": "登录成功截图"
  },
  
  "on_failure": {
    "action": "screenshot",
    "description": "失败状态截图"
  },
  
  "notes": [
    "二维码弹窗需要等待加载（2-3秒）",
    "Playwright locator API 比 DOM 搜索更可靠",
    "截图需保存到本地文件再发送"
  ]
}
```

### 流程字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 流程名称，唯一标识 |
| version | string | ✅ | 流程版本 |
| description | string | ✅ | 流程描述 |
| success_rate | string | ❌ | 成功率 |
| author | string | ❌ | 作者 |
| created_at | string | ❌ | 创建时间 |
| tags | array | ❌ | 标签列表 |
| params | object | ❌ | 流程参数定义 |
| steps | array | ✅ | 操作步骤列表 |
| on_success | object | ❌ | 成功后的操作 |
| on_failure | object | ❌ | 失败后的操作 |
| notes | array | ❌ | 注意事项 |

---

### 步骤配置说明

每个步骤支持以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | ✅ | 操作类型 |
| * | * | - | 操作参数（根据action类型） |
| wait_after | number | ❌ | 操作后等待时间（秒） |
| description | string | ❌ | 步骤描述 |
| retry | number | ❌ | 失败重试次数 |
| optional | boolean | ❌ | 是否可选步骤，默认false |

---

## 返回结果

### FlowResult

流程执行结果对象。

```python
class FlowResult:
    success: bool              # 是否成功
    flow_name: str             # 流程名称
    steps_executed: int        # 执行的步骤数
    steps_total: int           # 总步骤数
    screenshots: List[str]     # 截图文件路径列表
    data: dict                 # 返回数据
    error: str                 # 错误信息（失败时）
    duration: float            # 执行时长（秒）
    timestamp: str             # 时间戳
```

#### 使用示例

```python
result = engine.execute_flow("jimeng_login")

print(f"成功: {result.success}")
print(f"执行步骤: {result.steps_executed}/{result.steps_total}")
print(f"截图数量: {len(result.screenshots)}")
print(f"耗时: {result.duration}秒")

if result.success:
    # 获取最后一张截图
    last_screenshot = result.screenshots[-1]
    
    # 发送截图给用户
    send_message(to="user", image_url=last_screenshot)
else:
    print(f"错误: {result.error}")
```

---

### StepResult

单个步骤执行结果。

```python
class StepResult:
    success: bool              # 是否成功
    action: str                # 操作类型
    data: any                  # 返回数据
    screenshot: str            # 截图路径（如果有）
    error: str                 # 错误信息
    duration: float            # 执行时长（秒）
```

---

## 错误处理

### 异常类型

#### BrowserEngineException

基础异常类。

```python
from browser_engine.exceptions import BrowserEngineException

try:
    result = engine.execute_flow("jimeng_login")
except BrowserEngineException as e:
    print(f"引擎错误: {e}")
```

#### ConnectionException

连接异常。

```python
from browser_engine.exceptions import ConnectionException

try:
    engine.connect()
except ConnectionException as e:
    print(f"连接失败: {e}")
```

#### ElementNotFoundException

元素未找到异常。

```python
from browser_engine.exceptions import ElementNotFoundException

try:
    element = locator.by_text("登录")
except ElementNotFoundException as e:
    print(f"元素未找到: {e}")
```

#### TimeoutException

超时异常。

```python
from browser_engine.exceptions import TimeoutException

try:
    element = locator.by_text("登录", timeout=5000)
except TimeoutException as e:
    print(f"超时: {e}")
```

---

### 错误处理最佳实践

#### 1. 使用重试机制

```python
result = engine.execute_flow(
    "jimeng_login",
    retry_times=3
)
```

#### 2. 检查返回结果

```python
result = engine.execute_flow("jimeng_login")

if not result.success:
    # 查看错误信息
    print(f"错误: {result.error}")
    
    # 查看失败截图
    if result.screenshots:
        last_screenshot = result.screenshots[-1]
```

#### 3. 自定义错误处理

```python
try:
    result = engine.execute_flow("jimeng_login")
    
    if not result.success:
        # 通知用户
        send_message(
            to="admin",
            message=f"登录失败: {result.error}",
            image_url=result.screenshots[-1]
        )
except Exception as e:
    # 记录日志
    log_error(f"流程执行异常: {e}")
```

---

## 高级功能

### 条件执行

根据条件执行不同步骤。

```json
{
  "action": "click",
  "locator": "text=登录",
  "condition": {
    "type": "element_exists",
    "locator": "text=登录"
  }
}
```

### 循环执行

重复执行步骤。

```json
{
  "action": "click",
  "locator": "text=加载更多",
  "loop": {
    "max_times": 10,
    "until": {
      "type": "element_not_exists",
      "locator": "text=加载更多"
    }
  }
}
```

### 并行执行

并行执行多个步骤。

```json
{
  "action": "parallel",
  "steps": [
    {"action": "screenshot"},
    {"action": "evaluate", "script": "..."}
  ]
}
```

---

## 性能优化

### 1. 元素等待优化

```json
{
  "action": "click",
  "locator": "text=登录",
  "timeout": 5000,
  "wait_for": "visible"
}
```

### 2. 减少不必要的等待

只等待必要的时间：

```json
{
  "action": "wait",
  "time": 2  # 而不是5或10秒
}
```

### 3. 使用高效的定位器

优先级：`text` > `role` > `css` > `xpath`

### 4. 批量操作

合并多个操作减少页面刷新。

---

## 调试技巧

### 1. 启用详细日志

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### 2. 保留截图

```python
engine = BrowserEngine(
    screenshot_dir="/tmp/debug_screenshots",
    keep_all_screenshots=True
)
```

### 3. 单步执行

```python
executor = FlowExecutor(page)

for step in flow['steps']:
    result = executor.execute_step(step)
    print(f"步骤: {step['action']}, 结果: {result.success}")
    input("按回车继续...")
```

---

**🦞 文档持续更新中...**
