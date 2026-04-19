"""
浏览器操作引擎核心模块
Browser Engine Core - Main Module

版本: v0.2.0
作者: 龙虾智能体
"""

__version__ = "0.2.0"
__author__ = "Lobster Agent"

# 核心类导出
from .core.engine import BrowserEngine, EngineConfig
from .core.result import FlowResult, StepResult, ActionResult
from .core.enums import ActionType, LocatorStrategy, FlowStatus, LogLevel
from .core.exceptions import (
    BrowserEngineException,
    ConnectionException,
    ElementNotFoundException,
    TimeoutException,
    FlowExecutionException
)

# 便捷导出
__all__ = [
    # 核心引擎
    "BrowserEngine",
    "EngineConfig",
    
    # 结果对象
    "FlowResult",
    "StepResult",
    "ActionResult",
    
    # 枚举
    "ActionType",
    "LocatorStrategy",
    "FlowStatus",
    "LogLevel",
    
    # 异常
    "BrowserEngineException",
    "ConnectionException",
    "ElementNotFoundException",
    "TimeoutException",
    "FlowExecutionException",
]
