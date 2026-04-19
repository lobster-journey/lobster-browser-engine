"""
核心模块
Core Layer - Engine, Config, Enums, Exceptions
"""

from .engine import BrowserEngine, EngineConfig
from .result import FlowResult, StepResult, ActionResult
from .enums import ActionType, LocatorStrategy, FlowStatus, LogLevel
from .exceptions import (
    BrowserEngineException,
    ConnectionException,
    ElementNotFoundException,
    TimeoutException,
    FlowExecutionException
)

__all__ = [
    "BrowserEngine",
    "EngineConfig",
    "FlowResult",
    "StepResult",
    "ActionResult",
    "ActionType",
    "LocatorStrategy",
    "FlowStatus",
    "LogLevel",
    "BrowserEngineException",
    "ConnectionException",
    "ElementNotFoundException",
    "TimeoutException",
    "FlowExecutionException",
]
