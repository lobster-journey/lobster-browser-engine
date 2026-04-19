"""
Lobster Browser Engine - Base Plugin
插件基类

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BasePlugin(ABC):
    """
    插件基类
    
    所有插件都必须继承此类
    """
    
    def __init__(self):
        """初始化插件"""
        self.enabled = True
        self.config: Dict[str, Any] = {}
    
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass
    
    @property
    def description(self) -> str:
        """插件描述"""
        return ""
    
    @property
    def author(self) -> str:
        """插件作者"""
        return "Lobster Journey Studio"
    
    def initialize(self) -> None:
        """初始化插件"""
        pass
    
    def cleanup(self) -> None:
        """清理插件资源"""
        pass
    
    def enable(self) -> None:
        """启用插件"""
        self.enabled = True
    
    def disable(self) -> None:
        """禁用插件"""
        self.enabled = False
    
    def is_enabled(self) -> bool:
        """插件是否启用"""
        return self.enabled
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        配置插件
        
        Args:
            config: 配置字典
        """
        self.config.update(config)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        return self.config.get(key, default)
