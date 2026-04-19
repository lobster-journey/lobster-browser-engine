# Lobster Browser Engine - 安装和配置指南

---

## 📋 环境要求

### 必需环境

- **操作系统**：Linux / macOS / Windows
- **Python版本**：3.8 或更高
- **浏览器**：Chromium / Firefox / WebKit

### 推荐环境

- Python 3.10+
- Ubuntu 20.04+ / macOS 12+ / Windows 10+
- 至少 4GB 内存
- 至少 10GB 磁盘空间

---

## 🚀 安装步骤

### 步骤1：安装Python

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

**macOS**:
```bash
brew install python@3.10
```

**Windows**:
从 [python.org](https://www.python.org/downloads/) 下载安装

### 步骤2：克隆仓库

```bash
git clone https://github.com/lobster-journey/lobster-browser-engine.git
cd lobster-browser-engine
```

### 步骤3：创建虚拟环境（推荐）

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

### 步骤4：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤5：安装浏览器

```bash
playwright install chromium
# 或安装所有浏览器
playwright install
```

### 步骤6：验证安装

```bash
python -c "from lobster_browser_engine import BrowserEngine; print('✅ 安装成功！')"
```

---

## ⚙️ 配置

### 基础配置

创建配置文件 `config/engine.json`：

```json
{
  "connection": {
    "connection_type": "cdp",
    "cdp_url": "http://127.0.0.1:9222",
    "headless": false
  },
  "timeout": {
    "default_timeout": 30000,
    "navigation_timeout": 60000
  },
  "screenshot": {
    "enabled": true,
    "save_dir": "/tmp/screenshots"
  },
  "log": {
    "enabled": true,
    "level": "INFO"
  }
}
```

### 高级配置

```json
{
  "connection": {
    "connection_type": "persistent",
    "user_data_dir": "/tmp/browser_profile",
    "browser_type": "chromium",
    "args": [
      "--disable-blink-features=AutomationControlled",
      "--disable-dev-shm-usage"
    ]
  },
  "timeout": {
    "default_timeout": 30000,
    "navigation_timeout": 60000,
    "element_wait_timeout": 10000
  },
  "retry": {
    "enabled": true,
    "default_retry_times": 3,
    "strategy": "exponential_backoff"
  },
  "screenshot": {
    "enabled": true,
    "format": "png",
    "auto_screenshot_on_error": true
  },
  "performance": {
    "slow_mo": 0,
    "default_wait_after": 1.0
  }
}
```

---

## 🌐 浏览器配置

### CDP连接模式

连接到已运行的浏览器：

```bash
# 启动Chrome（CDP模式）
chromium-browser --remote-debugging-port=9222
```

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig

config = EngineConfig()
config.connection.cdp_url = "http://127.0.0.1:9222"

engine = BrowserEngine(config)
await engine.connect()
```

### 持久化模式

保存浏览器状态：

```python
config = EngineConfig()
config.connection.user_data_dir = "/tmp/browser_profile"
config.connection.headless = false

engine = BrowserEngine(config)
```

---

## 📂 项目结构

```
lobster-browser-engine/
├── src/
│   └── lobster_browser_engine/
│       ├── __init__.py
│       ├── engine.py           # 核心引擎
│       ├── config.py           # 配置管理
│       ├── enums.py            # 枚举定义
│       ├── exceptions.py       # 异常类
│       ├── result.py           # 结果对象
│       ├── actions/            # 操作执行器
│       ├── locators/           # 元素定位器
│       ├── flows/              # 流程管理
│       ├── utils/              # 工具函数
│       └── plugins/            # 插件系统
├── flows/                      # 流程配置文件
│   └── jimeng_login.json
├── tests/                      # 测试用例
├── docs/                       # 文档
├── requirements.txt
└── README.md
```

---

## 🔧 开发环境设置

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

### 运行测试

```bash
pytest tests/
```

### 代码格式化

```bash
black src/
isort src/
```

---

## 🐛 故障排除

### 问题1：浏览器启动失败

**解决方案**：
```bash
# 安装浏览器依赖
playwright install-deps chromium
```

### 问题2：权限错误

**解决方案**：
```bash
chmod +x scripts/*.sh
```

### 问题3：内存不足

**解决方案**：
- 减少并发数
- 使用无头模式
- 增加系统内存

---

## 📚 下一步

- 阅读 [用户指南](USER_GUIDE.md)
- 查看 [API文档](API.md)
- 尝试 [示例场景](EXAMPLES.md)

---

**🦞 龙虾巡游记工作室**
