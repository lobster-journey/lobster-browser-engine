<div align="center">

# 🦞 Browser Engine Core

**高可靠、高性能、可扩展的浏览器自动化操作引擎**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/)

<a href="https://github.com/lobster-journey/lobster-browser-engine">
<img src="https://img.shields.io/badge/maintained%20by-lobster%20journey%20studio-blue" alt="Maintained by Lobster Journey Studio">
</a>

</div>

---

## 📖 简介

Browser Engine Core 是一个高可靠、高性能、可扩展的浏览器自动化操作引擎，为上层 Skill 提供稳定可靠的浏览器操作能力。

### ✨ 核心特性

- 🔌 **CDP 连接** - 通过 Chrome DevTools Protocol 连接浏览器
- 🎯 **智能定位** - 多种定位策略，提高成功率
- 🔄 **路径沉淀** - 记录成功的操作路径，支持复用
- 🔁 **错误重试** - 自动重试失败操作
- 📸 **截图验证** - 操作前后自动截图验证
- 📊 **流程管理** - JSON配置化的流程定义

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Playwright 1.40+
- Chromium 浏览器（需开启远程调试）

### 安装

```bash
pip install playwright
playwright install chromium
```

### 启动浏览器

```bash
# macOS
/Applications/Chromium.app/Contents/MacOS/Chromium --remote-debugging-port=9222

# Linux
chromium --remote-debugging-port=9222

# Windows
chrome.exe --remote-debugging-port=9222
```

### 基本使用

```python
from browser_engine import BrowserEngine

# 连接浏览器
engine = BrowserEngine(cdp_url="http://127.0.0.1:9222")

# 执行登录流程
result = engine.execute_flow("jimeng_login")
print(f"登录结果: {result}")
```

---

## 📚 核心概念

### 操作流程 (Flow)

操作流程是一系列浏览器操作的集合，每个流程定义了完整的操作步骤。

**流程文件位置**：`flows/`

### 操作步骤 (Action)

每个流程由多个操作步骤组成：

| 操作 | 说明 |
|------|------|
| `navigate` | 导航到URL |
| `click` | 点击元素 |
| `fill` | 填充输入框 |
| `wait` | 等待时间或元素 |
| `screenshot` | 截图 |
| `evaluate` | 执行JavaScript |
| `press` | 按键操作 |
| `refresh` | 刷新页面 |

### 元素定位 (Locator)

支持多种定位策略：

- `text`: 文本内容（推荐）
- `css`: CSS选择器
- `xpath`: XPath表达式
- `role`: ARIA角色
- `test_id`: 测试ID

---

## 🔍 已验证流程

### 即梦登录流程

**成功率**: 100% (已验证 3 次)

**关键步骤**:
1. F5 刷新页面
2. 点击登录按钮
3. 点击抖音登录
4. 使用 `locator('text=刷新')` 定位刷新按钮
5. 点击刷新二维码
6. 等待用户扫码

**详细配置**: [flows/jimeng_login.json](flows/jimeng_login.json)

---

## 📂 项目结构

```
browser-engine-core/
├── README.md           # 项目文档
├── docs/
│   └── API.md         # API文档
├── flows/
│   ├── jimeng_login.json      # 即梦登录流程
│   └── README.md              # 流程说明
├── src/
│   ├── browser_engine.py      # 核心引擎
│   ├── flow_executor.py       # 流程执行器
│   └── element_locator.py     # 元素定位器
└── tests/                     # 单元测试
```

---

## 📊 性能指标

| 操作 | 平均耗时 | 成功率 |
|------|---------|--------|
| 即梦登录 | 8-12秒 | 100% |
| 小红书登录 | 待测试 | - |

---

## 📝 使用示例

### 执行预定义流程

```python
from browser_engine import BrowserEngine

engine = BrowserEngine()
result = engine.execute_flow("jimeng_login")

if result.success:
    print("登录成功！")
    screenshot = result.screenshots[-1]
else:
    print(f"登录失败: {result.error}")
```

### 自定义流程

```python
custom_flow = {
    "name": "search_google",
    "steps": [
        {"action": "navigate", "url": "https://www.google.com"},
        {"action": "fill", "locator": "input[name='q']", "value": "Playwright"},
        {"action": "press", "key": "Enter"},
        {"action": "wait", "time": 2},
        {"action": "screenshot"}
    ]
}

result = engine.execute_custom_flow(custom_flow)
```

---

## 🔧 API 文档

详细API文档请查看: [docs/API.md](docs/API.md)

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 添加新的操作流程

1. 在 `flows/` 目录创建流程配置文件
2. 编写流程说明文档
3. 测试验证流程可靠性
4. 提交 Pull Request

---

## 📄 License

MIT License

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

<div align="center">

**🦞 用AI视角，发现科技世界的美**

Made with ❤️ by Lobster Journey Studio

</div>
