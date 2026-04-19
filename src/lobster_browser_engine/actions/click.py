"""
Lobster Browser Engine - Click Action
点击操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...config import EngineConfig
from ...result import ActionResult
from ...enums import ActionType
from ...exceptions import ClickException
from .base import BaseActionExecutor


class ClickAction(BaseActionExecutor):
    """点击操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.CLICK
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行点击操作
        
        Args:
            params: {
                "locator": "text=登录",
                "strategy": "text",
                "timeout": 5000,
                "click_count": 1,
                "button": "left",
                "modifiers": []
            }
            
        Returns:
            ActionResult: 操作结果
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["locator"])
            
            locator = params["locator"]
            strategy = params.get("strategy", "text")
            timeout = params.get("timeout", self.config.timeout.action_timeout)
            click_count = params.get("click_count", 1)
            button = params.get("button", "left")
            modifiers = params.get("modifiers", [])
            
            # 创建定位器
            element = self._create_locator(locator, strategy)
            
            # 等待元素
            await element.wait_for(state="visible", timeout=timeout)
            
            # 执行点击
            await element.click(
                click_count=click_count,
                button=button,
                modifiers=modifiers
            )
            
            # 截图
            screenshot = await self._take_screenshot(params) if params.get("screenshot") else None
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"locator": locator, "strategy": strategy},
                screenshot=screenshot,
                duration=duration
            )
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return ActionResult(
                success=False,
                action_type=self.action_type,
                error=str(e),
                duration=duration
            )
    
    def _create_locator(self, locator: str, strategy: str):
        """创建定位器"""
        if strategy == "text":
            return self.page.locator(f"text={locator}")
        elif strategy == "css":
            return self.page.locator(locator)
        elif strategy == "xpath":
            return self.page.locator(f"xpath={locator}")
        else:
            return self.page.locator(locator)
