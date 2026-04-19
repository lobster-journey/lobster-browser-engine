"""
Lobster Browser Engine - Hover Action
悬停操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class HoverAction(BaseActionExecutor):
    """悬停操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.HOVER
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行悬停操作
        
        Args:
            params: {
                "selector": "button.menu",
                "position": {"x": 10, "y": 20},  # 可选
                "modifiers": ["Shift", "Control"],  # 可选
                "force": false  # 可选，强制悬停
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["selector"])
            
            selector = params["selector"]
            position = params.get("position")
            modifiers = params.get("modifiers")
            force = params.get("force", False)
            
            element = self.page.locator(selector)
            
            # 悬停选项
            hover_options = {}
            if position:
                hover_options["position"] = position
            if modifiers:
                hover_options["modifiers"] = modifiers
            if force:
                hover_options["force"] = force
            
            # 执行悬停
            await element.hover(**hover_options)
            
            # 等待效果
            wait_after = params.get("wait_after", 0.5)
            await asyncio.sleep(wait_after)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"selector": selector},
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


import asyncio
