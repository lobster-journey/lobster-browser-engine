"""
Lobster Browser Engine - Plugins Package
插件系统包

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from .manager import PluginManager
from .base import BasePlugin
from .registry import PluginRegistry
from .hooks import HookSystem

__all__ = [
    "PluginManager",
    "BasePlugin",
    "PluginRegistry",
    "HookSystem",
]
