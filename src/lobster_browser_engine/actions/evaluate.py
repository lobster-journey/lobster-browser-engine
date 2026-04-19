"""
Lobster Browser Engine - Evaluate Action
JavaScript执行操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class EvaluateAction(BaseActionExecutor):
    """JavaScript执行操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.EVALUATE
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行JavaScript操作
        
        Args:
            params: {
                "script": "document.querySelector('#btn').click()",
                "arg": null
            }
        """
        import time
        start_time = time.time()
        
        try:
            self._validate_params(params, ["script"])
            
            script = params["script"]
            arg = params.get("arg")
            
            # 执行JavaScript
            if arg is not None:
                result = await self.page.evaluate(script, arg)
            else:
                result = await self.page.evaluate(script)
            
            duration = (time.time() - start_time) * 1000
            
            return ActionResult(
                success=True,
                action_type=self.action_type,
                data={"result": result},
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
