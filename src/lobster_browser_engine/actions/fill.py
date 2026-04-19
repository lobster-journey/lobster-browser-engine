"""
Lobster Browser Engine - Fill Action
填充操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class FillAction(BaseActionExecutor):
    """填充操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.FILL
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行填充操作
        
        Args:
            params: {
                "locator": "css=input[name='username']",
                "value": "user@example.com",
                "clear_first": true,
                "timeout": 5000
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["locator", "value"])
            
            locator = params["locator"]
            value = params["value"]
            clear_first = params.get("clear_first", True)
            timeout = params.get("timeout", self.config.timeout.action_timeout)
            
            element = self.page.locator(locator)
            await element.wait_for(state="visible", timeout=timeout)
            
            if clear_first:
                await element.clear()
            
            await element.fill(value)
            
            screenshot = await self._take_screenshot(params) if params.get("screenshot") else None
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"locator": locator, "value": value},
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
