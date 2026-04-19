"""
Lobster Browser Engine - Action Factory
操作工厂

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from playwright.async_api import Page
from ...config import EngineConfig
from ...enums import ActionType
from ...exceptions import ActionNotSupportedException
from .base import BaseActionExecutor
from .navigate import NavigateAction
from .click import ClickAction
from .fill import FillAction
from .wait import WaitAction
from .screenshot import ScreenshotAction
from .evaluate import EvaluateAction
from .press import PressAction


class ActionFactory:
    """操作工厂类"""
    
    # 操作执行器映射
    _executors = {
        ActionType.NAVIGATE: NavigateAction,
        ActionType.CLICK: ClickAction,
        ActionType.FILL: FillAction,
        ActionType.WAIT: WaitAction,
        ActionType.SCREENSHOT: ScreenshotAction,
        ActionType.EVALUATE: EvaluateAction,
        ActionType.PRESS: PressAction,
    }
    
    @classmethod
    def create(
        cls,
        action_type: str,
        page: Page,
        config: EngineConfig
    ) -> BaseActionExecutor:
        """
        创建操作执行器
        
        Args:
            action_type: 操作类型
            page: Playwright页面对象
            config: 引擎配置
            
        Returns:
            BaseActionExecutor: 操作执行器实例
            
        Raises:
            ActionNotSupportedException: 操作不支持
        """
        # 转换为枚举
        if isinstance(action_type, str):
            try:
                action_type = ActionType(action_type)
            except ValueError:
                raise ActionNotSupportedException(action_type)
        
        # 获取执行器类
        executor_class = cls._executors.get(action_type)
        
        if not executor_class:
            raise ActionNotSupportedException(action_type.value)
        
        return executor_class(page, config)
    
    @classmethod
    def register(cls, action_type: ActionType, executor_class: type) -> None:
        """
        注册自定义操作执行器
        
        Args:
            action_type: 操作类型
            executor_class: 执行器类
        """
        cls._executors[action_type] = executor_class
    
    @classmethod
    def get_supported_actions(cls) -> list:
        """获取支持的操作列表"""
        return [action.value for action in cls._executors.keys()]
