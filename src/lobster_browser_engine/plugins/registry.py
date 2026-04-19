"""
Lobster Browser Engine - Plugin Registry
插件注册表

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, List, Optional
from .base import BasePlugin


class PluginRegistry:
    """
    插件注册表
    
    管理所有注册的插件
    """
    
    def __init__(self):
        """初始化注册表"""
        self._plugins: Dict[str, BasePlugin] = {}
    
    def register(self, plugin: BasePlugin) -> None:
        """
        注册插件
        
        Args:
            plugin: 插件实例
        """
        self._plugins[plugin.name] = plugin
    
    def unregister(self, plugin_name: str) -> None:
        """
        注销插件
        
        Args:
            plugin_name: 插件名称
        """
        self._plugins.pop(plugin_name, None)
    
    def get(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        获取插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            Optional[BasePlugin]: 插件实例
        """
        return self._plugins.get(plugin_name)
    
    def list(self) -> List[str]:
        """
        列出所有插件名称
        
        Returns:
            List[str]: 插件名称列表
        """
        return list(self._plugins.keys())
    
    def list_enabled(self) -> List[str]:
        """
        列出所有启用的插件
        
        Returns:
            List[str]: 启用的插件名称列表
        """
        return [name for name, plugin in self._plugins.items() if plugin.is_enabled()]
    
    def clear(self) -> None:
        """清空注册表"""
        self._plugins.clear()
