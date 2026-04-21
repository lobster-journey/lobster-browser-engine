"""
Lobster Browser Engine - 示例代码
演示如何使用浏览器引擎完成常见任务
"""

import asyncio
from pathlib import Path
import sys

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from browser_engine import BrowserEngine


async def example_basic_navigation():
    """示例1：基础导航操作"""
    print("\n=== 示例1：基础导航 ===")
    
    async with BrowserEngine() as engine:
        # 导航到网页
        await engine.navigate("https://example.com")
        
        # 截图
        await engine.screenshot("example_com.png")
        
        print("✅ 导航和截图完成")


async def example_fill_form():
    """示例2：表单填充"""
    print("\n=== 示例2：表单填充 ===")
    
    async with BrowserEngine() as engine:
        # 导航到登录页面
        await engine.navigate("https://example.com/login")
        
        # 填充表单
        await engine.fill('input[name="username"]', "test_user")
        await engine.fill('input[name="password"]', "test_pass")
        
        # 点击登录
        await engine.click('button[type="submit"]')
        
        # 等待跳转
        await engine.wait_for_url("**/dashboard")
        
        print("✅ 表单填充和登录完成")


async def example_take_screenshots():
    """示例3：批量截图"""
    print("\n=== 示例3：批量截图 ===")
    
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    async with BrowserEngine() as engine:
        for i, url in enumerate(urls, 1):
            await engine.navigate(url)
            await engine.screenshot(f"screenshot_{i}.png")
            print(f"✅ 截图 {i}/{len(urls)}: {url}")
    
    print("✅ 所有截图完成")


async def example_execute_flow():
    """示例4：执行预定义流程"""
    print("\n=== 示例4：执行流程 ===")
    
    async with BrowserEngine() as engine:
        # 执行登录流程
        result = await engine.execute_flow("jimeng_login")
        
        # 查看结果
        print(result.get_summary())
        
        print("✅ 流程执行完成")


async def main():
    """运行所有示例"""
    print("🦞 Lobster Browser Engine 示例")
    print("=" * 50)
    
    # 运行示例
    await example_basic_navigation()
    await example_fill_form()
    await example_take_screenshots()
    await example_execute_flow()
    
    print("\n" + "=" * 50)
    print("✅ 所有示例运行完成")


if __name__ == "__main__":
    asyncio.run(main())
