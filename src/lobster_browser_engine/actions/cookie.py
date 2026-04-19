"""
Lobster Browser Engine - Cookie Action
Cookie操作执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, Any, List
from ...result import ActionResult
from ...enums import ActionType
from .base import BaseActionExecutor


class CookieAction(BaseActionExecutor):
    """Cookie操作执行器"""
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.COOKIE
    
    async def execute(self, params: Dict[str, Any]) -> ActionResult:
        """
        执行Cookie操作
        
        Args:
            params: {
                "action": "get/set/delete/clear",
                "name": "sessionid",  # 可选
                "value": "xxx",  # set时需要
                "domain": ".example.com",  # 可选
                "cookies": [...]  # set多个时使用
            }
        """
        import time
        start_time = time.time()
        
        try:
            action = params.get("action", "get")
            context = self.page.context
            
            if action == "get":
                # 获取Cookie
                if "name" in params:
                    # 获取指定Cookie
                    cookies = await context.cookies()
                    cookie = next((c for c in cookies if c["name"] == params["name"]), None)
                    duration = (time.time() - start_time) * 1000
                    return ActionResult(
                        success=True,
                        action_type=self.action_type,
                        data={"cookie": cookie},
                        duration=duration
                    )
                else:
                    # 获取所有Cookie
                    cookies = await context.cookies()
                    duration = (time.time() - start_time) * 1000
                    return ActionResult(
                        success=True,
                        action_type=self.action_type,
                        data={"cookies": cookies, "count": len(cookies)},
                        duration=duration
                    )
            
            elif action == "set":
                # 设置Cookie
                if "cookies" in params:
                    # 批量设置
                    await context.add_cookies(params["cookies"])
                elif "name" in params and "value" in params:
                    # 设置单个Cookie
                    cookie = {
                        "name": params["name"],
                        "value": params["value"],
                        "domain": params.get("domain", await self._get_domain()),
                        "path": params.get("path", "/"),
                    }
                    await context.add_cookies([cookie])
                else:
                    raise ValueError("Must provide name/value or cookies for set action")
                
                duration = (time.time() - start_time) * 1000
                return ActionResult(
                    success=True,
                    action_type=self.action_type,
                    duration=duration
                )
            
            elif action == "delete":
                # 删除Cookie
                if "name" in params:
                    await context.clear_cookies()
                    # 注意：Playwright没有单独删除Cookie的API，需要清除后重新添加其他Cookie
                else:
                    raise ValueError("Must provide cookie name to delete")
                
                duration = (time.time() - start_time) * 1000
                return ActionResult(
                    success=True,
                    action_type=self.action_type,
                    duration=duration
                )
            
            elif action == "clear":
                # 清除所有Cookie
                await context.clear_cookies()
                duration = (time.time() - start_time) * 1000
                return ActionResult(
                    success=True,
                    action_type=self.action_type,
                    duration=duration
                )
            
            else:
                raise ValueError(f"Unknown cookie action: {action}")
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return ActionResult(
                success=False,
                action_type=self.action_type,
                error=str(e),
                duration=duration
            )
    
    async def _get_domain(self) -> str:
        """获取当前页面域名"""
        url = self.page.url
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
