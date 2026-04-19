"""
Lobster Browser Engine - Navigate Action
导航操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from playwright.async_api import Page
from ...config import EngineConfig
from ...result import ActionResult
from ...enums import ActionType
from ...exceptions import NavigationException
from .base import BaseActionExecutor


class NavigateAction(BaseActionExecutor):
    """导航操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.NAVIGATE
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行导航操作
        
        Args:
            params: {
                "url": "https://example.com",
                "wait_until": "networkidle",
                "timeout": 60000
            }
            
        Returns:
            ActionResult: 操作结果
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["url"])
            
            url = params["url"]
            wait_until = params.get("wait_until", "networkidle")
            timeout = params.get("timeout", self.config.timeout.navigation_timeout)
            
            # 执行导航
            await self.page.goto(
                url,
                wait_until=wait_until,
                timeout=timeout
            )
            
            # 截图
            screenshot = await self._take_screenshot(params) if params.get("screenshot") else None
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"url": url, "final_url": self.page.url},
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
