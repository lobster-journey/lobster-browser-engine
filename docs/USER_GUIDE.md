# Lobster Browser Engine - 用户指南

> 🦞 高可靠、高性能、可扩展的浏览器自动化操作引擎

---

## 📖 目录

- [简介](#简介)
- [安装](#安装)
- [快速开始](#快速开始)
- [核心概念](#核心概念)
- [API文档](#api文档)
- [示例场景](#示例场景)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 简介

Lobster Browser Engine 是一个基于 Playwright 的浏览器自动化操作引擎，提供了完整的浏览器操作能力，支持复杂的自动化流程。

### 核心特性

- ✅ **完整的操作支持**：18种操作类型，覆盖所有常见场景
- ✅ **智能元素定位**：多种定位策略，自动降级查找
- ✅ **流程管理**：流程录制、执行、验证、监控
- ✅ **插件系统**：可扩展的插件架构
- ✅ **异步支持**：完整的异步API
- ✅ **错误处理**：完善的异常体系和重试机制

---

## 安装

### 环境要求

- Python 3.8+
- Playwright 1.40+

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/lobster-journey/lobster-browser-engine.git
cd lobster-browser-engine

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium
```

### 验证安装

```python
from lobster_browser_engine import BrowserEngine

async def main():
    async with BrowserEngine() as engine:
        print("✅ 安装成功！")

import asyncio
asyncio.run(main())
```

---

## 快速开始

### 示例1：打开网页并截图

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig
import asyncio

async def main():
    # 创建引擎
    config = EngineConfig()
    
    async with BrowserEngine(config) as engine:
        # 获取页面
        page = engine.get_page()
        
        # 访问网页
        await page.goto("https://example.com")
        
        # 截图
        await page.screenshot(path="screenshot.png")
        
        print("✅ 截图完成！")

asyncio.run(main())
```

### 示例2：执行预定义流程

```python
from lobster_browser_engine import BrowserEngine
import asyncio

async def main():
    async with BrowserEngine() as engine:
        # 执行流程
        result = await engine.execute_flow("jimeng_login")
        
        # 查看结果
        print(result.get_summary())

asyncio.run(main())
```

---

## 核心概念

### 1. 引擎（Engine）

引擎是核心类，负责管理浏览器连接和执行操作。

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig

# 创建配置
config = EngineConfig()
config.connection.cdp_url = "http://127.0.0.1:9222"
config.screenshot.enabled = True
config.log.level = LogLevel.DEBUG

# 创建引擎
engine = BrowserEngine(config)

# 连接
await engine.connect()

# 使用...

# 断开
await engine.disconnect()
```

### 2. 操作（Action）

操作是执行的最小单元，包括导航、点击、填充、截图等。

```python
from lobster_browser_engine.actions import ActionFactory

# 创建操作执行器
executor = ActionFactory.create("click", page, config)

# 执行操作
result = await executor.execute({
    "locator": "text=登录",
    "strategy": "text"
})

# 查看结果
if result.success:
    print(f"✅ 点击成功，耗时：{result.duration}ms")
else:
    print(f"❌ 点击失败：{result.error}")
```

### 3. 流程（Flow）

流程是多个操作的组合，定义在JSON配置文件中。

```json
{
  "name": "login_flow",
  "version": "1.0.0",
  "description": "登录流程",
  "steps": [
    {
      "step_id": 1,
      "name": "打开登录页",
      "action": "navigate",
      "params": {
        "url": "https://example.com/login"
      }
    },
    {
      "step_id": 2,
      "name": "填充用户名",
      "action": "fill",
      "params": {
        "locator": "input[name='username']",
        "value": "user@example.com"
      }
    },
    {
      "step_id": 3,
      "name": "点击登录",
      "action": "click",
      "params": {
        "locator": "button[type='submit']"
      }
    }
  ]
}
```

---

## API文档

### BrowserEngine

#### 初始化

```python
engine = BrowserEngine(config: Optional[EngineConfig] = None)
```

#### 方法

- `connect()` - 连接到浏览器
- `disconnect()` - 断开浏览器连接
- `execute_flow(flow_name: str, params: Optional[Dict] = None)` - 执行流程
- `get_page()` - 获取页面对象

### ActionFactory

#### 创建操作

```python
executor = ActionFactory.create(action_type: str, page: Page, config: EngineConfig)
```

#### 支持的操作类型

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

### FlowManager

#### 管理流程

```python
from lobster_browser_engine.flows import FlowManager

manager = FlowManager()

# 创建流程
manager.create(flow_config)

# 读取流程
flow = manager.read("login_flow")

# 更新流程
manager.update("login_flow", updates)

# 删除流程
manager.delete("login_flow")

# 列出所有流程
flows = manager.list_flows()
```

---

## 示例场景

### 场景1：自动登录小红书

```python
from lobster_browser_engine import BrowserEngine
import asyncio

async def xiaohongshu_login():
    """自动登录小红书"""
    async with BrowserEngine() as engine:
        # 执行登录流程
        result = await engine.execute_flow("xiaohongshu_login")
        
        if result.success:
            print("✅ 登录成功！")
            print(f"步骤数：{result.steps_executed}")
            print(f"耗时：{result.get_duration_human()}")
        else:
            print(f"❌ 登录失败：{result.error}")

asyncio.run(xiaohongshu_login())
```

**流程配置** (`flows/xiaohongshu_login.json`):

```json
{
  "name": "xiaohongshu_login",
  "version": "1.0.0",
  "description": "小红书自动登录流程",
  "steps": [
    {
      "step_id": 1,
      "name": "打开小红书",
      "action": "navigate",
      "params": {
        "url": "https://www.xiaohongshu.com"
      }
    },
    {
      "step_id": 2,
      "name": "点击登录按钮",
      "action": "click",
      "params": {
        "locator": "text=登录",
        "strategy": "text"
      }
    },
    {
      "step_id": 3,
      "name": "等待扫码",
      "action": "wait",
      "params": {
        "locator": ".user-info",
        "state": "visible",
        "timeout": 60000
      }
    }
  ]
}
```

### 场景2：即梦每日积分获取

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig
import asyncio

async def jimeng_daily_credit():
    """即梦每日积分获取"""
    # 配置持久化浏览器
    config = EngineConfig()
    config.connection.user_data_dir = "/tmp/jimeng_browser_profile"
    config.connection.headless = False
    
    async with BrowserEngine(config) as engine:
        # 访问即梦
        page = engine.get_page()
        await page.goto("https://jimeng.jianying.com/")
        
        # 等待登录（首次需要扫码）
        await asyncio.sleep(3)
        
        print("✅ 每日积分已获取！")

asyncio.run(jimeng_daily_credit())
```

### 场景3：批量截图

```python
from lobster_browser_engine import BrowserEngine
import asyncio

async def batch_screenshot():
    """批量截图"""
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    async with BrowserEngine() as engine:
        page = engine.get_page()
        
        for i, url in enumerate(urls):
            await page.goto(url)
            await page.screenshot(path=f"screenshot_{i}.png")
            print(f"✅ 截图 {i+1}/{len(urls)} 完成")

asyncio.run(batch_screenshot())
```

---

## 最佳实践

### 1. 使用持久化浏览器配置

```python
config = EngineConfig()
config.connection.user_data_dir = "/tmp/browser_profile"
```

这样可以保存登录状态，避免重复登录。

### 2. 合理设置超时时间

```python
config = EngineConfig()
config.timeout.navigation_timeout = 60000  # 导航超时60秒
config.timeout.action_timeout = 10000  # 操作超时10秒
```

### 3. 启用日志和截图

```python
config = EngineConfig()
config.log.enabled = True
config.log.level = LogLevel.DEBUG
config.screenshot.enabled = True
config.screenshot.auto_screenshot_on_error = True
```

### 4. 使用流程配置文件

将复杂的操作流程定义为JSON文件，便于维护和复用。

### 5. 错误处理

```python
from lobster_browser_engine.exceptions import BrowserEngineException

try:
    result = await engine.execute_flow("login_flow")
    if not result.success:
        print(f"流程失败：{result.error}")
except BrowserEngineException as e:
    print(f"引擎错误：{str(e)}")
```

---

## 常见问题

### Q1：如何连接到已运行的浏览器？

```python
config = EngineConfig()
config.connection.cdp_url = "http://127.0.0.1:9222"
engine = BrowserEngine(config)
await engine.connect()
```

### Q2：如何处理动态加载的元素？

```python
# 使用wait操作等待元素
executor = ActionFactory.create("wait", page, config)
await executor.execute({
    "locator": ".dynamic-element",
    "state": "visible",
    "timeout": 10000
})
```

### Q3：如何保存登录状态？

```python
# 使用持久化浏览器配置
config.connection.user_data_dir = "/tmp/profile"
```

### Q4：如何处理弹窗？

```python
# 使用dialog操作
executor = ActionFactory.create("dialog", page, config)
await executor.execute({
    "action": "accept"
})
```

---

## 🦞 Lobster Journey Studio

**版本**：v0.2.0  
**日期**：2026-04-19  
**作者**：龙虾巡游记工作室  
**开源协议**：MIT

---

**文档持续更新中...**
