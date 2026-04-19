"""
Lobster Browser Engine - Select Action
选择操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any, List
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class SelectAction(BaseActionExecutor):
    """选择操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.SELECT
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行选择操作
        
        Args:
            params: {
                "selector": "select#country",
                "value": "china",  # 或 values: ["china", "usa"]
                "label": "中国",  # 或 labels: ["中国", "美国"]
                "index": 0  # 或 indices: [0, 1]
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["selector"])
            
            selector = params["selector"]
            
            element = self.page.locator(selector)
            await element.wait_for(state="visible", timeout=self.config.timeout.action_timeout)
            
            # 按值选择
            if "value" in params:
                await element.select_option(value=params["value"])
            elif "values" in params:
                await element.select_option(value=params["values"])
            # 按标签选择
            elif "label" in params:
                await element.select_option(label=params["label"])
            elif "labels" in params:
                await element.select_option(label=params["labels"])
            # 按索引选择
            elif "index" in params:
                await element.select_option(index=params["index"])
            elif "indices" in params:
                await element.select_option(index=params["indices"])
            else:
                raise ValueError("Must specify value/label/index for selection")
            
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
