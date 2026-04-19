"""
Lobster Browser Engine - Keyboard Action
键盘操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any, List
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class KeyboardAction(BaseActionExecutor):
    """键盘操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.KEYBOARD
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行键盘操作
        
        Args:
            params: {
                "action": "type/down/up/insert_text",
                "text": "Hello World",  # type/insert_text时使用
                "key": "Enter",  # down/up时使用
                "delay": 50,  # 可选，按键间隔（毫秒）
                "selector": "input",  # 可选，目标元素
                "modifiers": ["Control", "Shift"]  # 可选
            }
        """
        import time
        start_time = time.time()
        
        try:
            action = params.get("action", "type")
            delay = params.get("delay", 50)
            
            if action == "type":
                # 输入文本
                text = params.get("text", "")
                if "selector" in params:
                    element = self.page.locator(params["selector"])
                    await element.type(text, delay=delay)
                else:
                    await self.page.keyboard.type(text, delay=delay)
                
            elif action == "down":
                # 按下按键
                key = params["key"]
                await self.page.keyboard.down(key)
                
            elif action == "up":
                # 释放按键
                key = params["key"]
                await self.page.keyboard.up(key)
                
            elif action == "insert_text":
                # 插入文本（不触发键盘事件）
                text = params.get("text", "")
                if "selector" in params:
                    element = self.page.locator(params["selector"])
                    await element.fill(text)
                else:
                    await self.page.keyboard.insert_text(text)
            
            else:
                raise ValueError(f"Unknown keyboard action: {action}")
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"action": action},
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
