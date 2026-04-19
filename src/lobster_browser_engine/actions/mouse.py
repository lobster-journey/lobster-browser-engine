"""
Lobster Browser Engine - Mouse Action
鼠标操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class MouseAction(BaseActionExecutor):
    """鼠标操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.MOUSE
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行鼠标操作
        
        Args:
            params: {
                "action": "click/dblclick/move/down/up/wheel",
                "x": 100,
                "y": 200,
                "button": "left",  # left/right/middle
                "click_count": 1,
                "delay": 50,
                "delta_x": 0,  # wheel时使用
                "delta_y": -100  # wheel时使用
            }
        """
        import time
        start_time = time.time()
        
        try:
            action = params.get("action", "click")
            x = params.get("x", 0)
            y = params.get("y", 0)
            button = params.get("button", "left")
            delay = params.get("delay", 50)
            
            if action == "click":
                await self.page.mouse.click(
                    x, y,
                    button=button,
                    click_count=params.get("click_count", 1),
                    delay=delay
                )
            
            elif action == "dblclick":
                await self.page.mouse.dblclick(x, y, button=button, delay=delay)
            
            elif action == "move":
                steps = params.get("steps", 1)
                await self.page.mouse.move(x, y, steps=steps)
            
            elif action == "down":
                await self.page.mouse.down(button=button, click_count=params.get("click_count", 1))
            
            elif action == "up":
                await self.page.mouse.up(button=button, click_count=params.get("click_count", 1))
            
            elif action == "wheel":
                delta_x = params.get("delta_x", 0)
                delta_y = params.get("delta_y", 0)
                await self.page.mouse.wheel(delta_x, delta_y)
            
            else:
                raise ValueError(f"Unknown mouse action: {action}")
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"action": action, "x": x, "y": y},
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
