"""
Lobster Browser Engine - Core Enums
核心枚举类型定义

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from enum import Enum
from typing import Optional


class ActionType(Enum):
    """操作动作类型枚举"""
    
    # 导航操作
    NAVIGATE = "navigate"
    REFRESH = "refresh"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    
    # 点击操作
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    RIGHT_CLICK = "right_click"
    HOVER = "hover"
    
    # 输入操作
    FILL = "fill"
    TYPE = "type"
    PRESS = "press"
    CLEAR = "clear"
    
    # 等待操作
    WAIT = "wait"
    WAIT_FOR_SELECTOR = "wait_for_selector"
    WAIT_FOR_URL = "wait_for_url"
    WAIT_FOR_LOAD_STATE = "wait_for_load_state"
    
    # 截图操作
    SCREENSHOT = "screenshot"
    
    # JavaScript操作
    EVALUATE = "evaluate"
    EVALUATE_HANDLE = "evaluate_handle"
    
    # 选择操作
    SELECT = "select"
    SELECT_OPTION = "select_option"
    
    # 文件操作
    UPLOAD = "upload"
    DOWNLOAD = "download"
    
    # 滚动操作
    SCROLL = "scroll"
    SCROLL_TO = "scroll_to"
    
    # 拖拽操作
    DRAG = "drag"
    DRAG_AND_DROP = "drag_and_drop"
    
    # 框架操作
    SWITCH_TO_FRAME = "switch_to_frame"
    SWITCH_TO_MAIN = "switch_to_main"
    
    # 对话框操作
    ACCEPT_DIALOG = "accept_dialog"
    DISMISS_DIALOG = "dismiss_dialog"
    
    # Cookie操作
    GET_COOKIES = "get_cookies"
    SET_COOKIES = "set_cookies"
    CLEAR_COOKIES = "clear_cookies"
    
    # 存储操作
    GET_LOCAL_STORAGE = "get_local_storage"
    SET_LOCAL_STORAGE = "set_local_storage"
    CLEAR_LOCAL_STORAGE = "clear_local_storage"
    
    # 流程控制
    FLOW = "flow"
    PARALLEL = "parallel"
    CONDITION = "condition"
    LOOP = "loop"
    
    # 验证操作
    ASSERT = "assert"
    VERIFY = "verify"
    
    # 自定义操作
    CUSTOM = "custom"


class LocatorStrategy(Enum):
    """元素定位策略枚举"""
    
    # 文本定位
    TEXT = "text"
    TEXT_CONTAINS = "text_contains"
    
    # CSS定位
    CSS = "css"
    CSS_ALL = "css_all"
    
    # XPath定位
    XPATH = "xpath"
    XPATH_ALL = "xpath_all"
    
    # 角色定位
    ROLE = "role"
    
    # 标签定位
    LABEL = "label"
    LABEL_TEXT = "label_text"
    
    # 占位符定位
    PLACEHOLDER = "placeholder"
    
    # Alt文本定位
    ALT_TEXT = "alt_text"
    
    # 标题定位
    TITLE = "title"
    
    # 测试ID定位
    TEST_ID = "test_id"
    DATA_TEST_ID = "data_test_id"
    
    # 属性定位
    ATTRIBUTE = "attribute"
    
    # 组合定位
    CHAIN = "chain"
    FILTER = "filter"
    
    # 智能定位
    SMART = "smart"
    AUTO = "auto"


class WaitCondition(Enum):
    """等待条件枚举"""
    
    # 元素状态
    VISIBLE = "visible"
    HIDDEN = "hidden"
    ATTACHED = "attached"
    DETACHED = "detached"
    ENABLED = "enabled"
    DISABLED = "disabled"
    EDITABLE = "editable"
    READONLY = "readonly"
    CHECKED = "checked"
    UNCHECKED = "unchecked"
    FOCUSED = "focused"
    DEFOCUSED = "defocused"
    
    # 页面状态
    LOAD = "load"
    DOMCONTENTLOADED = "domcontentloaded"
    NETWORKIDLE = "networkidle"
    COMMIT = "commit"
    
    # URL状态
    URL_MATCHES = "url_matches"
    URL_CONTAINS = "url_contains"
    URL_EQUALS = "url_equals"
    
    # 函数返回
    FUNCTION = "function"
    
    # 自定义条件
    CUSTOM = "custom"


class FlowStatus(Enum):
    """流程状态枚举"""
    
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
    RETRY = "retry"
    PAUSED = "paused"
    ABORTED = "aborted"


class LogLevel(Enum):
    """日志级别枚举"""
    
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    TRACE = "TRACE"


class BrowserType(Enum):
    """浏览器类型枚举"""
    
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"
    CHROME = "chrome"
    EDGE = "edge"


class ConnectionType(Enum):
    """连接类型枚举"""
    
    CDP = "cdp"
    BROWSER_SERVER = "browser_server"
    PERSISTENT_CONTEXT = "persistent_context"


class ScreenshotFormat(Enum):
    """截图格式枚举"""
    
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


class ElementState(Enum):
    """元素状态枚举"""
    
    VISIBLE = "visible"
    HIDDEN = "hidden"
    STABLE = "stable"
    ENABLED = "enabled"
    DISABLED = "disabled"
    EDITABLE = "editable"


class ErrorCode(Enum):
    """错误代码枚举"""
    
    # 连接错误 (1xxx)
    CONNECTION_FAILED = 1001
    CONNECTION_TIMEOUT = 1002
    CONNECTION_CLOSED = 1003
    BROWSER_NOT_FOUND = 1004
    BROWSER_CRASHED = 1005
    
    # 元素错误 (2xxx)
    ELEMENT_NOT_FOUND = 2001
    ELEMENT_NOT_VISIBLE = 2002
    ELEMENT_NOT_INTERACTABLE = 2003
    ELEMENT_STALE = 2004
    ELEMENT_TIMEOUT = 2005
    SELECTOR_INVALID = 2006
    
    # 操作错误 (3xxx)
    ACTION_FAILED = 3001
    ACTION_TIMEOUT = 3002
    ACTION_NOT_SUPPORTED = 3003
    INVALID_ACTION_PARAMS = 3004
    NAVIGATION_FAILED = 3005
    CLICK_FAILED = 3006
    FILL_FAILED = 3007
    
    # 流程错误 (4xxx)
    FLOW_NOT_FOUND = 4001
    FLOW_EXECUTION_FAILED = 4002
    FLOW_TIMEOUT = 4003
    FLOW_VALIDATION_FAILED = 4004
    STEP_FAILED = 4005
    PRE_CHECK_FAILED = 4006
    POST_CHECK_FAILED = 4007
    
    # 页面错误 (5xxx)
    PAGE_LOAD_FAILED = 5001
    PAGE_TIMEOUT = 5002
    PAGE_CRASHED = 5003
    NAVIGATION_ERROR = 5004
    
    # JavaScript错误 (6xxx)
    JS_EXECUTION_FAILED = 6001
    JS_ERROR = 6002
    JS_TIMEOUT = 6003
    
    # 截图错误 (7xxx)
    SCREENSHOT_FAILED = 7001
    SCREENSHOT_TIMEOUT = 7002
    
    # 文件错误 (8xxx)
    FILE_NOT_FOUND = 8001
    FILE_UPLOAD_FAILED = 8002
    FILE_DOWNLOAD_FAILED = 8003
    
    # 配置错误 (9xxx)
    CONFIG_INVALID = 9001
    CONFIG_MISSING = 9002
    PARAM_INVALID = 9003
    
    # 未知错误
    UNKNOWN = 9999


class RetryStrategy(Enum):
    """重试策略枚举"""
    
    NONE = "none"
    IMMEDIATE = "immediate"
    LINEAR_BACKOFF = "linear_backoff"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_DELAY = "fixed_delay"


class ErrorRecoveryAction(Enum):
    """错误恢复动作枚举"""
    
    IGNORE = "ignore"
    RETRY = "retry"
    SKIP = "skip"
    ABORT = "abort"
    ROLLBACK = "rollback"
    CUSTOM = "custom"


class CacheStrategy(Enum):
    """缓存策略枚举"""
    
    NONE = "none"
    MEMORY = "memory"
    DISK = "disk"
    REDIS = "redis"


class ValidationType(Enum):
    """验证类型枚举"""
    
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"
    TEXT_EQUALS = "text_equals"
    TEXT_CONTAINS = "text_contains"
    TEXT_MATCHES = "text_matches"
    ATTRIBUTE_EQUALS = "attribute_equals"
    ATTRIBUTE_CONTAINS = "attribute_contains"
    VALUE_EQUALS = "value_equals"
    VALUE_CONTAINS = "value_contains"
    URL_EQUALS = "url_equals"
    URL_CONTAINS = "url_contains"
    URL_MATCHES = "url_matches"
    TITLE_EQUALS = "title_equals"
    TITLE_CONTAINS = "title_contains"
    COUNT_EQUALS = "count_equals"
    COUNT_GREATER_THAN = "count_greater_than"
    COUNT_LESS_THAN = "count_less_than"
    VISIBLE = "visible"
    HIDDEN = "hidden"
    ENABLED = "enabled"
    DISABLED = "disabled"
    CUSTOM = "custom"


class PluginPriority(Enum):
    """插件优先级枚举"""
    
    HIGHEST = 100
    HIGH = 80
    NORMAL = 50
    LOW = 20
    LOWEST = 10


class HookType(Enum):
    """钩子类型枚举"""
    
    BEFORE_ENGINE_START = "before_engine_start"
    AFTER_ENGINE_START = "after_engine_start"
    BEFORE_ENGINE_STOP = "before_engine_stop"
    AFTER_ENGINE_STOP = "after_engine_stop"
    
    BEFORE_FLOW = "before_flow"
    AFTER_FLOW = "after_flow"
    ON_FLOW_ERROR = "on_flow_error"
    
    BEFORE_STEP = "before_step"
    AFTER_STEP = "after_step"
    ON_STEP_ERROR = "on_step_error"
    
    BEFORE_ACTION = "before_action"
    AFTER_ACTION = "after_action"
    ON_ACTION_ERROR = "on_action_error"
    
    BEFORE_LOCATE = "before_locate"
    AFTER_LOCATE = "after_locate"
    ON_LOCATE_ERROR = "on_locate_error"
    
    BEFORE_NAVIGATION = "before_navigation"
    AFTER_NAVIGATION = "after_navigation"
    ON_NAVIGATION_ERROR = "on_navigation_error"
    
    BEFORE_CLICK = "before_click"
    AFTER_CLICK = "after_click"
    ON_CLICK_ERROR = "on_click_error"
    
    BEFORE_FILL = "before_fill"
    AFTER_FILL = "after_fill"
    ON_FILL_ERROR = "on_fill_error"
    
    BEFORE_SCREENSHOT = "before_screenshot"
    AFTER_SCREENSHOT = "after_screenshot"
    ON_SCREENSHOT_ERROR = "on_screenshot_error"
    
    ON_DIALOG = "on_dialog"
    ON_POPUP = "on_popup"
    ON_DOWNLOAD = "on_download"
    
    CUSTOM = "custom"


class LogLevel(Enum):
    """日志级别枚举（重新定义，确保完整性）"""
    
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
