"""
Lobster Browser Engine - Press Action
按键操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class PressAction(BaseActionExecutor):
    """按键操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.PRESS
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行按键操作
        
        Args:
            params: {
                "key": "Enter",
                "modifiers": ["Control"]
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["key"])
            
            key = params["key"]
            modifiers = params.get("modifiers", [])
            
            # 执行按键
            await self.page.keyboard.press(key, modifiers=modifiers)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"key": key, "modifiers": modifiers},
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
