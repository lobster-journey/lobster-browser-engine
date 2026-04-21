"""
Lobster Browser Engine - 测试代码
"""

import pytest
import asyncio
from pathlib import Path
import sys

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from browser_engine import BrowserEngine


@pytest.mark.asyncio
async def test_basic_navigation():
    """测试基础导航"""
    async with BrowserEngine() as engine:
        await engine.navigate("https://example.com")
        assert engine.page is not None


@pytest.mark.asyncio
async def test_screenshot():
    """测试截图功能"""
    async with BrowserEngine() as engine:
        await engine.navigate("https://example.com")
        await engine.screenshot("test_screenshot.png")
        assert Path("test_screenshot.png").exists()
        Path("test_screenshot.png").unlink()


@pytest.mark.asyncio
async def test_fill_and_click():
    """测试填充和点击"""
    async with BrowserEngine() as engine:
        await engine.navigate("https://example.com")
        # 这里只是测试API是否可用
        # 实际测试需要真实的表单页面
        assert hasattr(engine, 'fill')
        assert hasattr(engine, 'click')


@pytest.mark.asyncio
async def test_wait_for_selector():
    """测试等待元素"""
    async with BrowserEngine() as engine:
        await engine.navigate("https://example.com")
        await engine.wait_for_selector("h1")
        assert await engine.page.query_selector("h1") is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
