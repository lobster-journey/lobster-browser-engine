"""
Lobster Browser Engine - Screenshot Action
截图操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from pathlib import Path
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class ScreenshotAction(BaseActionExecutor):
    """截图操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.SCREENSHOT
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行截图操作
        
        Args:
            params: {
                "path": "/tmp/screenshot.png",
                "full_page": false,
                "clip": {"x": 0, "y": 0, "width": 800, "height": 600}
            }
        """
        import time
        start_time = time.time()
        
        try:
            # 生成文件名
            timestamp = int(time.time() * 1000)
            filename = params.get("path", f"{timestamp}_screenshot.png")
            
            if not filename.startswith("/"):
                filename = str(Path(self.config.screenshot.save_dir) / filename)
            
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            # 截图参数
            screenshot_options = {
                "path": filename,
                "full_page": params.get("full_page", self.config.screenshot.full_page)
            }
            
            if "clip" in params:
                screenshot_options["clip"] = params["clip"]
            
            # 执行截图
            await self.page.screenshot(**screenshot_options)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"path": filename},
                screenshot=filename,
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
