"""
Lobster Browser Engine - Base Action Executor
操作执行器基类

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from playwright.async_api import Page
from ...config import EngineConfig
from ...result import ActionResult
from ...enums import ActionType
from ...exceptions import ActionFailedException


class BaseActionExecutor(ABC):
    """
    操作执行器基类
    
    所有操作执行器的抽象基类
    """
    
    def __init__(self, page: Page, config: EngineConfig):
        """
        初始化操作执行器
        
        Args:
            page: Playwright页面对象
            config: 引擎配置
        """
        self.page = page
        self.config = config
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行操作
        
        Args:
            params: 操作参数
            
        Returns:
            ActionResult: 操作结果
        """
        pass
    
    @property
    @abstractmethod
    def action_type(self) -> ActionType:
        """操作类型"""
        pass
    
    def _validate_params(self, params: Dict[str, Any], required: list) -> None:
        """
        验证参数
        
        Args:
            params: 参数字典
            required: 必需参数列表
            
        Raises:
            ActionFailedException: 参数验证失败
        """
        missing = [p for p in required if p not in params]
        if missing:
            raise ActionFailedException(
                self.action_type.value,
                f"Missing required parameters: {', '.join(missing)}"
            )
    
    async def _take_screenshot(self, params: Dict[str, Any]) -> Optional[str]:
        """
        截图
        
        Args:
            params: 参数
            
        Returns:
            截图路径
        """
        if not self.config.screenshot.enabled:
            return None
        
        import time
        timestamp = int(time.time() * 1000)
        filename = f"{timestamp}_{self.action_type.value}.png"
        filepath = Path(self.config.screenshot.save_dir) / filename
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        await self.page.screenshot(path=str(filepath))
        
        return str(filepath)
