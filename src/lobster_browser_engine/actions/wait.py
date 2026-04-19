"""
Lobster Browser Engine - Wait Action
等待操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import asyncio
from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class WaitAction(BaseActionExecutor):
    """等待操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.WAIT
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行等待操作
        
        Args:
            params: {
                "time": 3,  # 或
                "locator": "text=加载完成",
                "url": "https://example.com/success",
                "state": "visible",
                "timeout": 10000
            }
        """
        import time
        start_time = time.time()
        
        try:
            # 等待时间
            if "time" in params:
                wait_time = params["time"]
                await asyncio.sleep(wait_time)
            
            # 等待元素
            elif "locator" in params:
                locator = params["locator"]
                state = params.get("state", "visible")
                timeout = params.get("timeout", self.config.timeout.element_wait_timeout)
                
                element = self.page.locator(locator)
                await element.wait_for(state=state, timeout=timeout)
            
            # 等待URL
            elif "url" in params:
                url = params["url"]
                timeout = params.get("timeout", self.config.timeout.navigation_timeout)
                await self.page.wait_for_url(url, timeout=timeout)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
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
