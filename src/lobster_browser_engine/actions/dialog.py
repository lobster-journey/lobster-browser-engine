"""
Lobster Browser Engine - Dialog Action
对话框操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class DialogAction(BaseActionExecutor):
    """对话框操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.DIALOG
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行对话框操作
        
        Args:
            params: {
                "action": "accept",  # accept/dismiss
                "prompt_text": "输入内容"  # 仅prompt对话框需要
            }
        """
        import time
        start_time = time.time()
        
        try:
            action = params.get("action", "accept")
            prompt_text = params.get("prompt_text")
            
            # 监听对话框事件
            dialog_handled = False
            dialog_info = {}
            
            async def handle_dialog(dialog):
                nonlocal dialog_handled, dialog_info
                dialog_info = {
                    "type": dialog.type,
                    "message": dialog.message,
                    "default_value": dialog.default_value
                }
                
                if action == "accept":
                    if prompt_text and dialog.type == "prompt":
                        await dialog.accept(prompt_text)
                    else:
                        await dialog.accept()
                else:
                    await dialog.dismiss()
                
                dialog_handled = True
            
            # 设置对话框监听器
            self.page.on("dialog", handle_dialog)
            
            # 等待对话框出现（如果在预期内）
            timeout = params.get("timeout", 5000)
            await asyncio.sleep(min(timeout / 1000, 1))
            
            duration = (time.time() - start_time) * 1000
            
            if dialog_handled:
                return ActionResult(
                    success=True,
                    action_type=self.action_type,
                    data={
                        "action": action,
                        "dialog": dialog_info
                    },
                    duration=duration
                )
            else:
                return ActionResult(
                    success=False,
                    action_type=self.action_type,
                    error="No dialog appeared",
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
