"""
Lobster Browser Engine - Smart Finder
智能元素查找器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import List, Dict, Any, Optional
from playwright.async_api import Page, Locator
from ..enums import LocatorStrategy
from ..exceptions import ElementNotFoundException
from .strategies import LocatorStrategies


class SmartFinder:
    """
    智能元素查找器
    
    尝试多种策略查找元素
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.strategies = LocatorStrategies(page)
    
    async def find(
        self,
        strategies: List[Dict[str, str]],
        timeout: int = 10000
    ) -> Optional[Locator]:
        """
        智能查找元素
        
        Args:
            strategies: 策略列表 [{"strategy": "text", "value": "登录"}, ...]
            timeout: 超时时间
            
        Returns:
            Locator: 找到的元素，如果都未找到则返回None
        """
        for strategy_config in strategies:
            try:
                strategy = LocatorStrategy(strategy_config["strategy"])
                value = strategy_config["value"]
                
                element = await self.strategies.create_locator(value, strategy)
                count = await element.count()
                
                if count > 0:
                    return element
                    
            except Exception:
                continue
        
        return None
    
    async def find_with_fallback(
        self,
        primary: Dict[str, str],
        fallbacks: List[Dict[str, str]],
        timeout: int = 10000
    ) -> Locator:
        """
        带降级的查找
        
        Args:
            primary: 主要策略
            fallbacks: 降级策略列表
            timeout: 超时时间
            
        Returns:
            Locator: 找到的元素
            
        Raises:
            ElementNotFoundException: 所有策略都失败
        """
        all_strategies = [primary] + fallbacks
        element = await self.find(all_strategies, timeout)
        
        if element:
            return element
        
        raise ElementNotFoundException(
            f"Element not found with {len(all_strategies)} strategies"
        )
