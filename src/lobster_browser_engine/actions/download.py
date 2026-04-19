"""
Lobster Browser Engine - Download Action
下载操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from pathlib import Path
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class DownloadAction(BaseActionExecutor):
    """下载操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.DOWNLOAD
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行下载操作
        
        Args:
            params: {
                "trigger_selector": "a.download",  # 触发下载的元素
                "save_path": "/path/to/save",  # 可选，默认临时目录
                "timeout": 60000
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["trigger_selector"])
            
            trigger_selector = params["trigger_selector"]
            save_path = params.get("save_path")
            timeout = params.get("timeout", self.config.timeout.action_timeout)
            
            # 设置下载处理
            async with self.page.expect_download(timeout=timeout) as download_info:
                # 触发下载
                element = self.page.locator(trigger_selector)
                await element.click()
            
            download = await download_info.value
            
            # 保存文件
            if save_path:
                save_file = Path(save_path)
                save_file.parent.mkdir(parents=True, exist_ok=True)
                await download.save_as(save_file)
                final_path = str(save_file)
            else:
                # 使用临时路径
                final_path = download.path()
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={
                    "filename": download.suggested_filename(),
                    "path": final_path,
                    "url": download.url
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
