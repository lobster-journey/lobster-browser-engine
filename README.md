# Browser Engine Core

> 🦞 由 **龙虾巡游记工作室** (Lobster Journey Studio) 开源
>
> 高可靠、高性能、可扩展的浏览器自动化操作引擎
>
> 版本：v0.2.0 | 状态：架构设计中

---

## 📖 项目简介

浏览器操作引擎是一个底层自动化引擎，提供可靠、稳定的浏览器操作能力。通过封装 Playwright 的强大功能，为上层 Skill 提供简单易用的 API。

### 核心特性

- ✅ **CDP 连接**：通过 Chrome DevTools Protocol 连接浏览器
- ✅ **智能元素定位**：多种定位策略，提高成功率
- ✅ **操作路径沉淀**：记录成功的操作路径，支持复用
- ✅ **错误重试机制**：自动重试失败操作
- ✅ **截图验证**：操作前后自动截图验证

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Playwright 1.40+
- Chromium 浏览器（需开启远程调试）

### 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 启动浏览器（开启远程调试）

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

### 1. 操作流程（Flow）

操作流程是一系列浏览器操作的集合，例如登录、发帖等。每个流程定义了完整的操作步骤。

**流程文件位置**：`flows/`

### 2. 操作步骤（Action）

每个流程由多个操作步骤组成：

- `navigate`: 导航到URL
- `click`: 点击元素
- `fill`: 填充输入框
- `wait`: 等待时间或元素
- `screenshot`: 截图
- `evaluate`: 执行JavaScript

### 3. 元素定位（Locator）

支持多种定位策略：

- `css`: CSS选择器
- `text`: 文本内容
- `xpath`: XPath表达式
- `role`: ARIA角色
- `test_id`: 测试ID

---

## 🔧 API 文档

详细API文档请查看：[API.md](./docs/API.md)

---

## 📂 目录结构

```
browser-engine-core/
├── README.md           # 项目文档（本文件）
├── docs/
│   ├── API.md         # 详细API文档
│   └── EXAMPLES.md    # 使用示例
├── flows/
│   ├── jimeng_login.json      # 即梦登录流程
│   ├── xiaohongshu_login.json # 小红书登录流程
│   └── README.md              # 流程说明
├── src/
│   ├── browser_engine.py      # 核心引擎
│   ├── flow_executor.py       # 流程执行器
│   ├── element_locator.py     # 元素定位器
│   └── utils.py               # 工具函数
└── examples/
    ├── basic_usage.py         # 基本使用示例
    └── custom_flow.py         # 自定义流程示例
```

---

## 🎯 设计原则

### 1. 可靠性优先

- 所有操作都有重试机制
- 操作前后自动验证
- 详细的错误日志

### 2. 可扩展性

- 流程配置化，易于添加新流程
- 支持自定义操作步骤
- 插件化架构

### 3. 简单易用

- 上层 Skill 只需调用 `execute_flow`
- 自动处理复杂细节
- 清晰的返回结果

---

## 🔍 已验证的操作路径

### 即梦登录流程

**成功率**：100%（已验证 3 次）

**关键步骤**：
1. F5 刷新页面
2. 点击登录按钮
3. 点击抖音登录
4. 使用 `locator('text=刷新')` 定位刷新按钮
5. 点击刷新二维码
6. 等待用户扫码

**注意事项**：
- 二维码弹窗需要等待加载（2-3秒）
- Playwright locator API 比 DOM 搜索更可靠
- 截图发送需保存到本地文件再发送

**详细路径**：[flows/jimeng_login.json](./flows/jimeng_login.json)

---

## 📝 使用示例

### 示例1：即梦登录

```python
from browser_engine import BrowserEngine

engine = BrowserEngine()
result = engine.execute_flow("jimeng_login")

if result.success:
    print("登录成功！")
    # 获取截图
    screenshot_path = result.screenshots[-1]
else:
    print(f"登录失败: {result.error}")
```

---

## ⚠️ 重要规则

### 截图发送规则

**✅ 正确流程**：
1. Python脚本截图保存到本地文件
2. 确认文件存在
3. 使用 `infoflow_send` 的 `imageUrl` 参数发送本地文件

**❌ 错误做法**：
- 直接使用 `browser screenshot`（不会发送给用户）
- 不保存文件直接发送

---

## 📊 性能指标

| 操作 | 平均耗时 | 成功率 |
|------|---------|--------|
| 即梦登录 | 8-12秒 | 100% |

---

## 🔄 更新日志

### v0.1.0 (2026-04-19)
- ✅ 完成即梦登录流程验证
- ✅ 沉淀截图发送规则
- ✅ 创建项目结构

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

**🦞 用AI视角，发现科技世界的美**
