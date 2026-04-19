"""
Lobster Browser Engine - Locator Strategies
定位策略实现

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Type
from playwright.async_api import Page, Locator
from ..enums import LocatorStrategy


class LocatorStrategies:
    """定位策略集合"""
    
    def __init__(self, page: Page):
        self.page = page
        self._strategies: Dict[LocatorStrategy, Type] = {}
        self._register_default_strategies()
    
    def _register_default_strategies(self) -> None:
        """注册默认策略"""
        self._strategies = {
            LocatorStrategy.TEXT: self._text_strategy,
            LocatorStrategy.CSS: self._css_strategy,
            LocatorStrategy.XPATH: self._xpath_strategy,
            LocatorStrategy.ROLE: self._role_strategy,
            LocatorStrategy.LABEL: self._label_strategy,
            LocatorStrategy.PLACEHOLDER: self._placeholder_strategy,
            LocatorStrategy.TEST_ID: self._test_id_strategy,
        }
    
    async def create_locator(
        self,
        value: str,
        strategy: LocatorStrategy
    ) -> Locator:
        """创建定位器"""
        strategy_func = self._strategies.get(strategy)
        
        if not strategy_func:
            raise ValueError(f"Unsupported strategy: {strategy}")
        
        return await strategy_func(value)
    
    async def _text_strategy(self, value: str) -> Locator:
        """文本定位策略"""
        return self.page.locator(f"text={value}")
    
    async def _css_strategy(self, value: str) -> Locator:
        """CSS定位策略"""
        return self.page.locator(value)
    
    async def _xpath_strategy(self, value: str) -> Locator:
        """XPath定位策略"""
        return self.page.locator(f"xpath={value}")
    
    async def _role_strategy(self, value: str) -> Locator:
        """角色定位策略"""
        return self.page.get_by_role(value)
    
    async def _label_strategy(self, value: str) -> Locator:
        """标签定位策略"""
        return self.page.get_by_label(value)
    
    async def _placeholder_strategy(self, value: str) -> Locator:
        """占位符定位策略"""
        return self.page.get_by_placeholder(value)
    
    async def _test_id_strategy(self, value: str) -> Locator:
        """测试ID定位策略"""
        return self.page.get_by_test_id(value)
    
    def register(self, strategy: LocatorStrategy, func: Type) -> None:
        """注册自定义策略"""
        self._strategies[strategy] = func
    
    def get_supported_strategies(self) -> list:
        """获取支持的策略列表"""
        return [s.value for s in self._strategies.keys()]
