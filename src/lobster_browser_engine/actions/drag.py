"""
Lobster Browser Engine - Drag Action
拖拽操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class DragAction(BaseActionExecutor):
    """拖拽操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.DRAG
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行拖拽操作
        
        Args:
            params: {
                "source": "div.draggable",
                "target": "div.dropzone",
                "source_position": {"x": 10, "y": 10},  # 可选
                "target_position": {"x": 50, "y": 50},  # 可选
                "steps": 10  # 可选，拖拽步数
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["source", "target"])
            
            source = params["source"]
            target = params["target"]
            source_position = params.get("source_position")
            target_position = params.get("target_position")
            steps = params.get("steps", 10)
            
            # 获取源元素
            source_element = self.page.locator(source)
            await source_element.wait_for(state="visible", timeout=self.config.timeout.action_timeout)
            
            # 执行拖拽
            await source_element.drag_to(
                self.page.locator(target),
                source_position=source_position,
                target_position=target_position,
                steps=steps
            )
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={
                    "source": source,
                    "target": target
                },
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
