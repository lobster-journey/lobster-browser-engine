<div align="center">

# 🦞 Lobster Browser Engine

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

Lobster Browser Engine 是一个生产级的浏览器自动化操作引擎，基于 Playwright 构建，提供了完整、可靠、易用的浏览器操作能力。

### 🎯 设计理念

- **简单易用** - 几行代码即可完成复杂操作
- **功能完整** - 覆盖所有常见浏览器自动化场景
- **生产可用** - 完善的错误处理、重试机制、日志系统
- **可扩展** - 插件系统和流程配置，轻松扩展

---

## ✨ 核心特性

### 🚀 18种操作类型

| 类别 | 操作 |
|------|------|
| **导航** | navigate, go_back, go_forward, refresh |
| **交互** | click, fill, select, hover, drag |
| **输入** | press, keyboard, type |
| **等待** | wait, wait_for_selector, wait_for_url |
| **截图** | screenshot, video, pdf |
| **高级** | evaluate, upload, download, cookie, dialog |

### 🎯 智能元素定位

- **多种策略**：text, css, xpath, role, label, placeholder
- **自动降级**：定位失败时自动尝试其他策略
- **错误恢复**：完善的异常处理和重试机制

### 🔄 流程管理

- **流程定义**：JSON配置文件定义复杂流程
- **流程执行**：自动执行、变量替换、条件判断
- **流程监控**：执行历史、性能统计、错误追踪

### 🔌 插件系统

- **可扩展架构**：插件管理器、注册表、钩子系统
- **自定义扩展**：轻松添加新功能和操作类型

---

## 💡 使用场景

### 适合什么场景？

✅ **Web应用自动化测试**  
✅ **数据抓取和采集**  
✅ **表单自动填充**  
✅ **定时任务自动化**  
✅ **浏览器操作封装**  
✅ **RPA流程自动化**  

### 不适合什么场景？

❌ 简单的HTTP请求（用 requests）  
❌ 静态页面解析（用 BeautifulSoup）  
❌ 反爬虫严格的网站（需要特殊处理）  

---

## 🚀 快速开始

### 5分钟上手

```python
from lobster_browser_engine import BrowserEngine
import asyncio

async def main():
    # 创建引擎
    async with BrowserEngine() as engine:
        page = engine.get_page()
        
        # 打开网页
        await page.goto("https://example.com")
        
        # 截图
        await page.screenshot(path="screenshot.png")

asyncio.run(main())
```

### 执行预定义流程

```python
async with BrowserEngine() as engine:
    # 执行登录流程
    result = await engine.execute_flow("xiaohongshu_login")
    
    # 查看结果
    print(result.get_summary())
```

---

## 📚 文档

- **[安装指南](docs/INSTALLATION.md)** - 环境配置和安装步骤
- **[API文档](docs/API.md)** - 详细的接口说明
- **[示例场景](docs/EXAMPLES.md)** - 真实场景的实现案例

---

## 🎯 项目亮点

### 1. 生产级可靠性

- 完善的异常处理体系
- 自动重试和错误恢复
- 详细的日志和监控

### 2. 开发者友好

- 清晰的API设计
- 完整的类型注解
- 详细的代码注释

### 3. Agent友好

- 代码结构清晰
- 配置文件驱动
- 易于理解和执行

---

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/lobster-journey/lobster-browser-engine.git

# 安装依赖
pip install -r requirements.txt

# 安装浏览器
playwright install chromium
```

---

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议！

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🦞 关于作者

**Lobster Journey Studio**  
用AI视角，发现科技世界的美

- GitHub: [@lobster-journey](https://github.com/lobster-journey)
- 品牌：🦞 龙虾巡游记

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

Made with 🦞 by Lobster Journey Studio

</div>
