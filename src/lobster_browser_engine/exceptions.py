"""
Lobster Browser Engine - Core Exceptions
核心异常类定义

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from typing import Optional, Dict, Any
from .enums import ErrorCode


class BrowserEngineException(Exception):
    """
    浏览器引擎基础异常类
    
    所有引擎相关异常的基类
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or ErrorCode.UNKNOWN
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"[{self.error_code.name}] {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "error": True,
            "error_code": self.error_code.value,
            "error_name": self.error_code.name,
            "message": self.message,
            "details": self.details
        }


class ConnectionException(BrowserEngineException):
    """
    浏览器连接异常
    
    当无法连接到浏览器时抛出
    """
    
    def __init__(
        self,
        message: str = "Failed to connect to browser",
        error_code: Optional[ErrorCode] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_code = error_code or ErrorCode.CONNECTION_FAILED
        super().__init__(message, error_code, details)


class ConnectionTimeoutException(ConnectionException):
    """连接超时异常"""
    
    def __init__(
        self,
        message: str = "Connection timeout",
        timeout: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if timeout:
            details["timeout"] = timeout
        super().__init__(message, ErrorCode.CONNECTION_TIMEOUT, details)


class BrowserNotFoundException(ConnectionException):
    """浏览器未找到异常"""
    
    def __init__(
        self,
        message: str = "Browser not found",
        browser_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if browser_type:
            details["browser_type"] = browser_type
        super().__init__(message, ErrorCode.BROWSER_NOT_FOUND, details)


class BrowserCrashedException(ConnectionException):
    """浏览器崩溃异常"""
    
    def __init__(
        self,
        message: str = "Browser crashed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.BROWSER_CRASHED, details)


class ElementException(BrowserEngineException):
    """
    元素操作异常基类
    
    当元素操作失败时抛出
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        locator: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if locator:
            details["locator"] = locator
        error_code = error_code or ErrorCode.ELEMENT_NOT_FOUND
        super().__init__(message, error_code, details)


class ElementNotFoundException(ElementException):
    """元素未找到异常"""
    
    def __init__(
        self,
        locator: Optional[str] = None,
        message: str = "Element not found",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.ELEMENT_NOT_FOUND, locator, details)


class ElementNotVisibleException(ElementException):
    """元素不可见异常"""
    
    def __init__(
        self,
        locator: Optional[str] = None,
        message: str = "Element is not visible",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.ELEMENT_NOT_VISIBLE, locator, details)


class ElementNotInteractableException(ElementException):
    """元素不可交互异常"""
    
    def __init__(
        self,
        locator: Optional[str] = None,
        message: str = "Element is not interactable",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.ELEMENT_NOT_INTERACTABLE, locator, details)


class ElementTimeoutException(ElementException):
    """元素等待超时异常"""
    
    def __init__(
        self,
        locator: Optional[str] = None,
        timeout: Optional[int] = None,
        message: str = "Element wait timeout",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if timeout:
            details["timeout"] = timeout
        super().__init__(message, ErrorCode.ELEMENT_TIMEOUT, locator, details)


class SelectorInvalidException(ElementException):
    """选择器无效异常"""
    
    def __init__(
        self,
        selector: Optional[str] = None,
        message: str = "Invalid selector",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if selector:
            details["selector"] = selector
        super().__init__(message, ErrorCode.SELECTOR_INVALID, None, details)


class ActionException(BrowserEngineException):
    """
    操作执行异常基类
    
    当操作执行失败时抛出
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        action_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if action_type:
            details["action_type"] = action_type
        error_code = error_code or ErrorCode.ACTION_FAILED
        super().__init__(message, error_code, details)


class ActionFailedException(ActionException):
    """操作失败异常"""
    
    def __init__(
        self,
        action_type: Optional[str] = None,
        message: str = "Action failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.ACTION_FAILED, action_type, details)


class ActionTimeoutException(ActionException):
    """操作超时异常"""
    
    def __init__(
        self,
        action_type: Optional[str] = None,
        timeout: Optional[int] = None,
        message: str = "Action timeout",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if timeout:
            details["timeout"] = timeout
        super().__init__(message, ErrorCode.ACTION_TIMEOUT, action_type, details)


class ActionNotSupportedException(ActionException):
    """操作不支持异常"""
    
    def __init__(
        self,
        action_type: Optional[str] = None,
        message: str = "Action not supported",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.ACTION_NOT_SUPPORTED, action_type, details)


class InvalidActionParamsException(ActionException):
    """操作参数无效异常"""
    
    def __init__(
        self,
        action_type: Optional[str] = None,
        param_name: Optional[str] = None,
        message: str = "Invalid action parameters",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if param_name:
            details["param_name"] = param_name
        super().__init__(message, ErrorCode.INVALID_ACTION_PARAMS, action_type, details)


class NavigationException(ActionException):
    """导航异常"""
    
    def __init__(
        self,
        url: Optional[str] = None,
        message: str = "Navigation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if url:
            details["url"] = url
        super().__init__(message, ErrorCode.NAVIGATION_FAILED, "navigate", details)


class ClickException(ActionException):
    """点击异常"""
    
    def __init__(
        self,
        locator: Optional[str] = None,
        message: str = "Click failed",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if locator:
            details["locator"] = locator
        super().__init__(message, ErrorCode.CLICK_FAILED, "click", details)


class FillException(ActionException):
    """填充异常"""
    
    def __init__(
        self,
        locator: Optional[str] = None,
        value: Optional[str] = None,
        message: str = "Fill failed",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if locator:
            details["locator"] = locator
        if value:
            details["value"] = value
        super().__init__(message, ErrorCode.FILL_FAILED, "fill", details)


class FlowException(BrowserEngineException):
    """
    流程执行异常基类
    
    当流程执行失败时抛出
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        flow_name: Optional[str] = None,
        step_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if flow_name:
            details["flow_name"] = flow_name
        if step_id is not None:
            details["step_id"] = step_id
        error_code = error_code or ErrorCode.FLOW_EXECUTION_FAILED
        super().__init__(message, error_code, details)


class FlowNotFoundException(FlowException):
    """流程未找到异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        message: str = "Flow not found",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.FLOW_NOT_FOUND, flow_name, None, details)


class FlowExecutionException(FlowException):
    """流程执行异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        step_id: Optional[int] = None,
        message: str = "Flow execution failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.FLOW_EXECUTION_FAILED, flow_name, step_id, details)


class FlowTimeoutException(FlowException):
    """流程超时异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        timeout: Optional[int] = None,
        message: str = "Flow execution timeout",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if timeout:
            details["timeout"] = timeout
        super().__init__(message, ErrorCode.FLOW_TIMEOUT, flow_name, None, details)


class FlowValidationException(FlowException):
    """流程验证异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        message: str = "Flow validation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.FLOW_VALIDATION_FAILED, flow_name, None, details)


class StepException(FlowException):
    """步骤执行异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        step_id: Optional[int] = None,
        message: str = "Step execution failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.STEP_FAILED, flow_name, step_id, details)


class PreCheckException(FlowException):
    """前置检查异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        message: str = "Pre-check failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.PRE_CHECK_FAILED, flow_name, None, details)


class PostCheckException(FlowException):
    """后置检查异常"""
    
    def __init__(
        self,
        flow_name: Optional[str] = None,
        message: str = "Post-check failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.POST_CHECK_FAILED, flow_name, None, details)


class PageException(BrowserEngineException):
    """
    页面相关异常基类
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        url: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if url:
            details["url"] = url
        super().__init__(message, error_code, details)


class PageLoadException(PageException):
    """页面加载异常"""
    
    def __init__(
        self,
        url: Optional[str] = None,
        message: str = "Page load failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.PAGE_LOAD_FAILED, url, details)


class PageTimeoutException(PageException):
    """页面超时异常"""
    
    def __init__(
        self,
        url: Optional[str] = None,
        timeout: Optional[int] = None,
        message: str = "Page load timeout",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if timeout:
            details["timeout"] = timeout
        super().__init__(message, ErrorCode.PAGE_TIMEOUT, url, details)


class JavaScriptException(BrowserEngineException):
    """
    JavaScript执行异常基类
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        script: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if script:
            details["script"] = script[:200]  # 只保留前200字符
        error_code = error_code or ErrorCode.JS_EXECUTION_FAILED
        super().__init__(message, error_code, details)


class JSExecutionException(JavaScriptException):
    """JavaScript执行异常"""
    
    def __init__(
        self,
        script: Optional[str] = None,
        error_message: Optional[str] = None,
        message: str = "JavaScript execution failed",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if error_message:
            details["js_error"] = error_message
        super().__init__(message, ErrorCode.JS_EXECUTION_FAILED, script, details)


class ScreenshotException(BrowserEngineException):
    """截图异常"""
    
    def __init__(
        self,
        message: str = "Screenshot failed",
        error_code: Optional[ErrorCode] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_code = error_code or ErrorCode.SCREENSHOT_FAILED
        super().__init__(message, error_code, details)


class FileException(BrowserEngineException):
    """文件操作异常基类"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        file_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if file_path:
            details["file_path"] = file_path
        super().__init__(message, error_code, details)


class FileNotFoundException(FileException):
    """文件未找到异常"""
    
    def __init__(
        self,
        file_path: Optional[str] = None,
        message: str = "File not found",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.FILE_NOT_FOUND, file_path, details)


class FileUploadException(FileException):
    """文件上传异常"""
    
    def __init__(
        self,
        file_path: Optional[str] = None,
        message: str = "File upload failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, ErrorCode.FILE_UPLOAD_FAILED, file_path, details)


class ConfigException(BrowserEngineException):
    """配置异常"""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        config_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if config_key:
            details["config_key"] = config_key
        error_code = error_code or ErrorCode.CONFIG_INVALID
        super().__init__(message, error_code, details)


class ValidationException(BrowserEngineException):
    """验证异常"""
    
    def __init__(
        self,
        message: str,
        validation_type: Optional[str] = None,
        expected: Optional[Any] = None,
        actual: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if validation_type:
            details["validation_type"] = validation_type
        if expected is not None:
            details["expected"] = expected
        if actual is not None:
            details["actual"] = actual
        super().__init__(message, ErrorCode.PARAM_INVALID, details)


class PluginException(BrowserEngineException):
    """插件异常"""
    
    def __init__(
        self,
        message: str,
        plugin_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if plugin_name:
            details["plugin_name"] = plugin_name
        super().__init__(message, ErrorCode.UNKNOWN, details)


class CacheException(BrowserEngineException):
    """缓存异常"""
    
    def __init__(
        self,
        message: str,
        cache_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if cache_key:
            details["cache_key"] = cache_key
        super().__init__(message, ErrorCode.UNKNOWN, details)
