"""
Lobster Browser Engine - Element Locator
元素定位器主模块

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Optional, List, Dict, Any
from playwright.async_api import Page, Locator
from ..enums import LocatorStrategy
from ..exceptions import ElementNotFoundException
from .strategies import LocatorStrategies


class ElementLocator:
    """
    元素定位器
    
    提供多种元素定位策略
    """
    
    def __init__(self, page: Page):
        """
        初始化元素定位器
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.strategies = LocatorStrategies(page)
    
    async def find(
        self,
        locator: str,
        strategy: LocatorStrategy = LocatorStrategy.AUTO,
        timeout: int = 10000
    ) -> Locator:
        """
        查找元素
        
        Args:
            locator: 定位器字符串
            strategy: 定位策略
            timeout: 超时时间
            
        Returns:
            Locator: Playwright定位器
            
        Raises:
            ElementNotFoundException: 元素未找到
        """
        try:
            if strategy == LocatorStrategy.AUTO:
                return await self._auto_find(locator, timeout)
            
            return await self.strategies.create_locator(locator, strategy)
            
        except Exception as e:
            raise ElementNotFoundException(locator, str(e))
    
    async def _auto_find(self, locator: str, timeout: int) -> Locator:
        """自动查找（尝试多种策略）"""
        strategies = [
            LocatorStrategy.TEXT,
            LocatorStrategy.CSS,
            LocatorStrategy.XPATH,
        ]
        
        for strategy in strategies:
            try:
                element = await self.strategies.create_locator(locator, strategy)
                if await element.count() > 0:
                    return element
            except:
                continue
        
        raise ElementNotFoundException(locator, "Element not found with any strategy")
    
    async def find_all(
        self,
        locator: str,
        strategy: LocatorStrategy = LocatorStrategy.CSS
    ) -> List[Locator]:
        """查找所有匹配元素"""
        element = await self.strategies.create_locator(locator, strategy)
        count = await element.count()
        return [element.nth(i) for i in range(count)]
    
    async def wait_for(
        self,
        locator: str,
        state: str = "visible",
        timeout: int = 10000
    ) -> Locator:
        """等待元素"""
        element = await self.find(locator)
        await element.wait_for(state=state, timeout=timeout)
        return element
