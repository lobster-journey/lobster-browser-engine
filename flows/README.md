# 操作流程说明

本目录存放所有已验证的操作流程配置文件。

---

## 流程列表

### 即梦登录流程 ✅

**文件**：`jimeng_login.json`

**状态**：已验证，成功率100%

**用途**：
- 即梦AI账号登录
- 支持抖音扫码登录
- 自动刷新二维码

**使用**：
```python
from browser_engine import BrowserEngine

engine = BrowserEngine()
result = engine.execute_flow("jimeng_login")
```

**关键发现**：
- Playwright `locator('text=刷新')` 最可靠
- 二维码弹窗需等待2-3秒
- 截图必须保存到本地再发送

---

### 小红书登录流程 🔄

**文件**：待创建

**状态**：待验证

**用途**：
- 小红书账号登录
- 支持多种登录方式

**计划**：
1. 收集登录流程信息
2. 编写流程配置
3. 测试验证
4. 记录成功率

---

## 流程规范

### 文件命名

- 格式：`{平台}_{操作}.json`
- 示例：`jimeng_login.json`, `xiaohongshu_post.json`

### 必填字段

```json
{
  "name": "流程名称",
  "version": "1.0.0",
  "description": "流程描述",
  "steps": []
}
```

### 验证要求

每个流程至少验证3次成功后，才能标记为"已验证"。

---

**🦞 持续添加更多流程...**
