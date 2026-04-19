"""
Lobster Browser Engine - Upload Action
文件上传操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from pathlib import Path
from ...result import ActionResult
from ...enums import ActionType
from ...exceptions import FileUploadException
from .base import BaseActionExecutor


class UploadAction(BaseActionExecutor):
    """文件上传操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.UPLOAD
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行文件上传操作
        
        Args:
            params: {
                "selector": "input[type='file']",
                "files": ["/path/to/file1.jpg", "/path/to/file2.png"],
                "timeout": 30000
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["selector", "files"])
            
            selector = params["selector"]
            files = params["files"]
            
            # 确保files是列表
            if isinstance(files, str):
                files = [files]
            
            # 验证文件存在
            for file_path in files:
                if not Path(file_path).exists():
                    raise FileUploadException(
                        self.action_type.value,
                        f"File not found: {file_path}"
                    )
            
            # 获取input元素
            element = self.page.locator(selector)
            
            # 上传文件
            await element.set_input_files(files)
            
            # 等待上传完成
            wait_time = params.get("wait_after", 2)
            await asyncio.sleep(wait_time)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={
                    "selector": selector,
                    "files": files,
                    "count": len(files)
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


import asyncio
