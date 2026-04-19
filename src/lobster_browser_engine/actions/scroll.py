"""
Lobster Browser Engine - Scroll Action
滚动操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any, Optional
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class ScrollAction(BaseActionExecutor):
    """滚动操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.SCROLL
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行滚动操作
        
        Args:
            params: {
                "direction": "down",  # up/down/top/bottom
                "distance": 300,  # 像素，可选
                "selector": "#content",  # 可选，指定滚动元素
                "smooth": true
            }
        """
        import time
        start_time = time.time()
        
        try:
            direction = params.get("direction", "down")
            distance = params.get("distance", 300)
            selector = params.get("selector")
            smooth = params.get("smooth", True)
            
            # 确定滚动距离
            if direction == "top":
                scroll_y = 0
            elif direction == "bottom":
                scroll_y = "document.body.scrollHeight"
            elif direction == "up":
                scroll_y = f"-{distance}"
            else:  # down
                scroll_y = str(distance)
            
            # 构建滚动脚本
            if smooth:
                behavior = "smooth"
            else:
                behavior = "auto"
            
            if selector:
                # 滚动指定元素
                script = f"""
                const element = document.querySelector('{selector}');
                if (element) {{
                    element.scrollTo({{
                        top: {scroll_y},
                        behavior: '{behavior}'
                    }});
                }}
                """
            else:
                # 滚动整个页面
                script = f"window.scrollTo({{top: {scroll_y}, behavior: '{behavior}'}})"
            
            await self.page.evaluate(script)
            
            # 等待滚动完成
            if smooth:
                await asyncio.sleep(0.5)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"direction": direction, "distance": distance},
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
