"""
Lobster Browser Engine - Plugin Manager
插件管理器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import importlib
import json
from .base import BasePlugin
from .registry import PluginRegistry
from ..exceptions import PluginException


class PluginManager:
    """
    插件管理器
    
    负责插件的加载、启用、禁用和管理
    """
    
    def __init__(self, plugins_dir: Optional[str] = None):
        """
        初始化插件管理器
        
        Args:
            plugins_dir: 插件目录
        """
        self.plugins_dir = Path(plugins_dir) if plugins_dir else Path(__file__).parent
        self.registry = PluginRegistry()
        self.loaded_plugins: Dict[str, BasePlugin] = {}
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        加载插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 是否成功
        """
        try:
            # 动态导入插件模块
            module = importlib.import_module(f".{plugin_name}", package=__package__)
            
            # 获取插件类
            plugin_class = getattr(module, "Plugin", None)
            if not plugin_class:
                raise PluginException(f"Plugin class not found in {plugin_name}")
            
            # 创建插件实例
            plugin = plugin_class()
            
            # 初始化插件
            plugin.initialize()
            
            # 注册插件
            self.registry.register(plugin)
            self.loaded_plugins[plugin_name] = plugin
            
            return True
            
        except Exception as e:
            raise PluginException(f"Failed to load plugin {plugin_name}: {str(e)}")
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        卸载插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            bool: 是否成功
        """
        if plugin_name not in self.loaded_plugins:
            return False
        
        plugin = self.loaded_plugins[plugin_name]
        
        # 清理插件
        plugin.cleanup()
        
        # 从注册表移除
        self.registry.unregister(plugin_name)
        
        # 从已加载列表移除
        del self.loaded_plugins[plugin_name]
        
        return True
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        获取插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            Optional[BasePlugin]: 插件实例
        """
        return self.loaded_plugins.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """
        列出所有已加载的插件
        
        Returns:
            List[str]: 插件名称列表
        """
        return list(self.loaded_plugins.keys())
    
    def enable_plugin(self, plugin_name: str) -> None:
        """启用插件"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enable()
    
    def disable_plugin(self, plugin_name: str) -> None:
        """禁用插件"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.disable()
    
    def load_all_plugins(self) -> None:
        """加载所有插件"""
        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith('_'):
                try:
                    self.load_plugin(plugin_dir.name)
                except Exception:
                    # 跳过加载失败的插件
                    pass
