# Lobster Browser Engine - 示例场景

---

## 示例1：小红书自动登录

### 场景描述

自动打开小红书网站，点击登录按钮，等待用户扫码登录。

### Skill实现

```python
"""
小红书自动登录Skill

触发词：小红书登录、打开小红书
"""

from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig
import asyncio

async def xiaohongshu_login():
    """自动登录小红书"""
    
    # 配置浏览器（保存登录状态）
    config = EngineConfig()
    config.connection.user_data_dir = "/tmp/xiaohongshu_profile"
    config.connection.headless = False
    config.screenshot.enabled = True
    
    # 创建引擎
    async with BrowserEngine(config) as engine:
        # 获取页面
        page = engine.get_page()
        
        # 访问小红书
        await page.goto("https://www.xiaohongshu.com")
        
        # 点击登录
        login_button = page.locator("text=登录")
        await login_button.click()
        
        # 等待登录成功（最多5分钟）
        try:
            await page.wait_for_selector(".user-info", timeout=300000)
            print("✅ 登录成功！")
            
            # 保存截图
            await page.screenshot(path="/tmp/xiaohongshu_logged_in.png")
            
            return True
        except Exception as e:
            print(f"❌ 登录失败：{str(e)}")
            return False

# 执行
if __name__ == "__main__":
    asyncio.run(xiaohongshu_login())
```

### 流程配置方式

**流程文件** (`flows/xiaohongshu_login.json`):

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
      "name": "点击登录",
      "action": "click",
      "params": {
        "locator": "text=登录",
        "strategy": "text"
      }
    },
    {
      "step_id": 3,
      "name": "等待登录成功",
      "action": "wait",
      "params": {
        "locator": ".user-info",
        "state": "visible",
        "timeout": 300000
      }
    },
    {
      "step_id": 4,
      "name": "截图保存",
      "action": "screenshot",
      "params": {
        "path": "/tmp/xiaohongshu_logged_in.png"
      }
    }
  ]
}
```

**使用流程**:

```python
from lobster_browser_engine import BrowserEngine
import asyncio

async def main():
    async with BrowserEngine() as engine:
        result = await engine.execute_flow("xiaohongshu_login")
        print(result.get_summary())

asyncio.run(main())
```

---

## 示例2：即梦每日积分获取

### 场景描述

每天自动打开即梦网站，获取60积分奖励。

### 完整实现

```python
"""
即梦每日积分获取Skill

触发词：即梦积分、每日登录、jimeng credit
"""

from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.config import EngineConfig
import asyncio
from pathlib import Path

class JimengDailyCredit:
    """即梦每日积分管理"""
    
    def __init__(self):
        self.profile_dir = Path.home() / ".openclaw/browser_profiles/jimeng"
        self.profile_dir.mkdir(parents=True, exist_ok=True)
    
    async def get_daily_credit(self):
        """获取每日积分"""
        
        # 配置持久化浏览器
        config = EngineConfig()
        config.connection.user_data_dir = str(self.profile_dir)
        config.connection.headless = False
        config.timeout.navigation_timeout = 60000
        
        async with BrowserEngine(config) as engine:
            page = engine.get_page()
            
            # 访问即梦
            print("🌐 正在访问即梦网站...")
            await page.goto("https://jimeng.jianying.com/")
            
            # 等待页面加载
            await asyncio.sleep(3)
            
            # 检查登录状态
            login_button = page.locator("text=登录").first
            if await login_button.is_visible():
                print("⚠️ 未检测到登录状态")
                print("请在浏览器中扫码登录...")
                
                # 等待用户扫码
                await page.wait_for_selector("text=我的", timeout=300000)
                print("✅ 登录成功！")
            else:
                print("✅ 已保持登录状态")
            
            # 提取Session ID
            cookies = await page.context.cookies()
            session_id = next((c["value"] for c in cookies if c["name"] == "sessionid"), None)
            
            if session_id:
                # 保存Session ID
                session_file = Path.home() / ".openclaw/config/jimeng/session_id.txt"
                session_file.parent.mkdir(parents=True, exist_ok=True)
                session_file.write_text(session_id)
                print(f"✅ Session ID已保存")
            
            print("✅ 每日积分获取完成！")
            print("💰 预计获得60积分奖励")
            
            return True

# 执行
if __name__ == "__main__":
    jimeng = JimengDailyCredit()
    asyncio.run(jimeng.get_daily_credit())
```

---

## 示例3：自动化表单填充

### 场景描述

自动填充网页表单并提交。

### 实现代码

```python
from lobster_browser_engine import BrowserEngine
from lobster_browser_engine.actions import ActionFactory
import asyncio

async def fill_form():
    """自动填充表单"""
    
    async with BrowserEngine() as engine:
        page = engine.get_page()
        
        # 打开表单页面
        await page.goto("https://example.com/form")
        
        # 填充用户名
        fill_executor = ActionFactory.create("fill", page, engine.config)
        await fill_executor.execute({
            "locator": "input[name='username']",
            "value": "user@example.com"
        })
        
        # 填充密码
        await fill_executor.execute({
            "locator": "input[name='password']",
            "value": "password123"
        })
        
        # 选择下拉框
        select_executor = ActionFactory.create("select", page, engine.config)
        await select_executor.execute({
            "selector": "select#country",
            "value": "china"
        })
        
        # 上传文件
        upload_executor = ActionFactory.create("upload", page, engine.config)
        await upload_executor.execute({
            "selector": "input[type='file']",
            "files": ["/path/to/file.jpg"]
        })
        
        # 点击提交
        click_executor = ActionFactory.create("click", page, engine.config)
        await click_executor.execute({
            "locator": "button[type='submit']"
        })
        
        print("✅ 表单提交完成！")

asyncio.run(fill_form())
```

---

## 示例4：批量操作

### 场景描述

批量处理多个URL，自动截图并保存。

### 实现代码

```python
from lobster_browser_engine import BrowserEngine
import asyncio
from pathlib import Path

async def batch_process():
    """批量处理URL"""
    
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    output_dir = Path("/tmp/screenshots")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with BrowserEngine() as engine:
        page = engine.get_page()
        
        for i, url in enumerate(urls):
            try:
                print(f"处理 {i+1}/{len(urls)}: {url}")
                
                # 访问URL
                await page.goto(url, wait_until="networkidle")
                
                # 截图
                screenshot_path = output_dir / f"screenshot_{i+1}.png"
                await page.screenshot(path=str(screenshot_path))
                
                print(f"  ✅ 完成：{screenshot_path}")
                
            except Exception as e:
                print(f"  ❌ 失败：{str(e)}")
        
        print(f"\n✅ 批量处理完成！共处理 {len(urls)} 个URL")

asyncio.run(batch_process())
```

---

## 示例5：数据抓取

### 场景描述

自动抓取网页数据并保存。

### 实现代码

```python
from lobster_browser_engine import BrowserEngine
import asyncio
import json

async def scrape_data():
    """抓取网页数据"""
    
    async with BrowserEngine() as engine:
        page = engine.get_page()
        
        # 访问目标网站
        await page.goto("https://example.com/products")
        
        # 等待数据加载
        await page.wait_for_selector(".product-item")
        
        # 提取数据
        products = await page.evaluate("""() => {
            const items = document.querySelectorAll('.product-item');
            return Array.from(items).map(item => ({
                title: item.querySelector('.title')?.textContent || '',
                price: item.querySelector('.price')?.textContent || '',
                link: item.querySelector('a')?.href || ''
            }));
        }""")
        
        # 保存数据
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 抓取完成！共 {len(products)} 条数据")
        print(f"📄 数据已保存到 products.json")

asyncio.run(scrape_data())
```

---

## 🦞 龙虾巡游记工作室

**持续更新更多示例...**
