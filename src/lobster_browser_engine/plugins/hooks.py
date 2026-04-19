"""
Lobster Browser Engine - Hook System
钩子系统

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Callable, List, Dict, Any


class HookSystem:
    """
    钩子系统
    
    提供插件扩展点机制
    """
    
    def __init__(self):
        """初始化钩子系统"""
        self._hooks: Dict[str, List[Callable]] = {}
    
    def register(self, hook_name: str, callback: Callable) -> None:
        """
        注册钩子回调
        
        Args:
            hook_name: 钩子名称
            callback: 回调函数
        """
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        
        self._hooks[hook_name].append(callback)
    
    def unregister(self, hook_name: str, callback: Callable) -> None:
        """
        注销钩子回调
        
        Args:
            hook_name: 钩子名称
            callback: 回调函数
        """
        if hook_name in self._hooks:
            try:
                self._hooks[hook_name].remove(callback)
            except ValueError:
                pass
    
    async def execute(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        执行钩子
        
        Args:
            hook_name: 钩子名称
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            List[Any]: 所有回调的返回值列表
        """
        if hook_name not in self._hooks:
            return []
        
        results = []
        for callback in self._hooks[hook_name]:
            try:
                result = await callback(*args, **kwargs)
                results.append(result)
            except Exception:
                # 回调失败不影响其他回调
                pass
        
        return results
    
    def clear(self, hook_name: Optional[str] = None) -> None:
        """
        清除钩子
        
        Args:
            hook_name: 钩子名称，不指定则清除所有
        """
        if hook_name:
            self._hooks.pop(hook_name, None)
        else:
            self._hooks.clear()
    
    def list_hooks(self) -> List[str]:
        """
        列出所有钩子名称
        
        Returns:
            List[str]: 钩子名称列表
        """
        return list(self._hooks.keys())
