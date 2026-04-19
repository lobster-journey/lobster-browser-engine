"""
Lobster Browser Engine - Core Config
核心配置类定义

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from pathlib import Path
from .enums import (
    LogLevel,
    BrowserType,
    ConnectionType,
    ScreenshotFormat,
    RetryStrategy,
    CacheStrategy
)


@dataclass
class ConnectionConfig:
    """
    连接配置
    
    管理浏览器连接相关配置
    """
    
    # 连接类型
    connection_type: ConnectionType = ConnectionType.CDP
    
    # CDP连接配置
    cdp_url: str = "http://127.0.0.1:9222"
    connection_timeout: int = 30000  # 毫秒
    
    # 浏览器服务器配置
    browser_server_url: Optional[str] = None
    
    # 持久化上下文配置
    user_data_dir: Optional[str] = None
    headless: bool = False
    
    # 浏览器类型
    browser_type: BrowserType = BrowserType.CHROMIUM
    
    # 启动参数
    args: List[str] = field(default_factory=lambda: [])
    
    # 环境变量
    env: Dict[str, str] = field(default_factory=dict)
    
    # 代理配置
    proxy: Optional[Dict[str, Any]] = None
    
    # 忽略HTTPS错误
    ignore_https_errors: bool = True
    
    # 接受下载
    accept_downloads: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "connection_type": self.connection_type.value,
            "cdp_url": self.cdp_url,
            "connection_timeout": self.connection_timeout,
            "browser_server_url": self.browser_server_url,
            "user_data_dir": self.user_data_dir,
            "headless": self.headless,
            "browser_type": self.browser_type.value,
            "args": self.args,
            "env": self.env,
            "proxy": self.proxy,
            "ignore_https_errors": self.ignore_https_errors,
            "accept_downloads": self.accept_downloads
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConnectionConfig":
        """从字典创建"""
        return cls(
            connection_type=ConnectionType(data.get("connection_type", "cdp")),
            cdp_url=data.get("cdp_url", "http://127.0.0.1:9222"),
            connection_timeout=data.get("connection_timeout", 30000),
            browser_server_url=data.get("browser_server_url"),
            user_data_dir=data.get("user_data_dir"),
            headless=data.get("headless", False),
            browser_type=BrowserType(data.get("browser_type", "chromium")),
            args=data.get("args", []),
            env=data.get("env", {}),
            proxy=data.get("proxy"),
            ignore_https_errors=data.get("ignore_https_errors", True),
            accept_downloads=data.get("accept_downloads", True)
        )


@dataclass
class TimeoutConfig:
    """
    超时配置
    
    管理各类超时设置
    """
    
    # 默认超时
    default_timeout: int = 30000  # 毫秒
    
    # 导航超时
    navigation_timeout: int = 60000
    
    # 页面加载超时
    page_load_timeout: int = 60000
    
    # 元素等待超时
    element_wait_timeout: int = 10000
    
    # 操作超时
    action_timeout: int = 10000
    
    # 流程执行超时
    flow_timeout: int = 300000
    
    # JavaScript执行超时
    js_timeout: int = 10000
    
    # 截图超时
    screenshot_timeout: int = 5000
    
    # 连接超时
    connection_timeout: int = 30000
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "default_timeout": self.default_timeout,
            "navigation_timeout": self.navigation_timeout,
            "page_load_timeout": self.page_load_timeout,
            "element_wait_timeout": self.element_wait_timeout,
            "action_timeout": self.action_timeout,
            "flow_timeout": self.flow_timeout,
            "js_timeout": self.js_timeout,
            "screenshot_timeout": self.screenshot_timeout,
            "connection_timeout": self.connection_timeout
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeoutConfig":
        """从字典创建"""
        return cls(
            default_timeout=data.get("default_timeout", 30000),
            navigation_timeout=data.get("navigation_timeout", 60000),
            page_load_timeout=data.get("page_load_timeout", 60000),
            element_wait_timeout=data.get("element_wait_timeout", 10000),
            action_timeout=data.get("action_timeout", 10000),
            flow_timeout=data.get("flow_timeout", 300000),
            js_timeout=data.get("js_timeout", 10000),
            screenshot_timeout=data.get("screenshot_timeout", 5000),
            connection_timeout=data.get("connection_timeout", 30000)
        )


@dataclass
class RetryConfig:
    """
    重试配置
    
    管理重试策略和参数
    """
    
    # 是否启用重试
    enabled: bool = True
    
    # 默认重试次数
    default_retry_times: int = 3
    
    # 重试策略
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    
    # 初始延迟（毫秒）
    initial_delay: int = 1000
    
    # 最大延迟（毫秒）
    max_delay: int = 30000
    
    # 延迟倍数（用于指数退避）
    delay_multiplier: float = 2.0
    
    # 重试特定错误
    retry_on_errors: List[str] = field(default_factory=lambda: [
        "ELEMENT_NOT_FOUND",
        "ELEMENT_TIMEOUT",
        "ACTION_TIMEOUT",
        "NETWORK_ERROR"
    ])
    
    # 跳过重试的错误
    skip_retry_on_errors: List[str] = field(default_factory=lambda: [
        "CONFIG_INVALID",
        "PARAM_INVALID",
        "SELECTOR_INVALID"
    ])
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "enabled": self.enabled,
            "default_retry_times": self.default_retry_times,
            "strategy": self.strategy.value,
            "initial_delay": self.initial_delay,
            "max_delay": self.max_delay,
            "delay_multiplier": self.delay_multiplier,
            "retry_on_errors": self.retry_on_errors,
            "skip_retry_on_errors": self.skip_retry_on_errors
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RetryConfig":
        """从字典创建"""
        return cls(
            enabled=data.get("enabled", True),
            default_retry_times=data.get("default_retry_times", 3),
            strategy=RetryStrategy(data.get("strategy", "exponential_backoff")),
            initial_delay=data.get("initial_delay", 1000),
            max_delay=data.get("max_delay", 30000),
            delay_multiplier=data.get("delay_multiplier", 2.0),
            retry_on_errors=data.get("retry_on_errors", []),
            skip_retry_on_errors=data.get("skip_retry_on_errors", [])
        )


@dataclass
class ScreenshotConfig:
    """
    截图配置
    
    管理截图相关设置
    """
    
    # 是否启用截图
    enabled: bool = True
    
    # 截图保存目录
    save_dir: str = "/tmp/lobster_browser_engine/screenshots"
    
    # 截图格式
    format: ScreenshotFormat = ScreenshotFormat.PNG
    
    # 图片质量（仅JPEG）
    quality: int = 80
    
    # 是否全页截图
    full_page: bool = False
    
    # 是否保留所有截图
    keep_all_screenshots: bool = False
    
    # 截图命名模式
    naming_pattern: str = "{timestamp}_{action}_{step_id}"
    
    # 自动截图
    auto_screenshot_on_error: bool = True
    auto_screenshot_on_success: bool = False
    auto_screenshot_between_steps: bool = False
    
    # 最大截图数量
    max_screenshots: int = 100
    
    # 自动清理旧截图
    auto_cleanup: bool = True
    cleanup_after_days: int = 7
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "enabled": self.enabled,
            "save_dir": self.save_dir,
            "format": self.format.value,
            "quality": self.quality,
            "full_page": self.full_page,
            "keep_all_screenshots": self.keep_all_screenshots,
            "naming_pattern": self.naming_pattern,
            "auto_screenshot_on_error": self.auto_screenshot_on_error,
            "auto_screenshot_on_success": self.auto_screenshot_on_success,
            "auto_screenshot_between_steps": self.auto_screenshot_between_steps,
            "max_screenshots": self.max_screenshots,
            "auto_cleanup": self.auto_cleanup,
            "cleanup_after_days": self.cleanup_after_days
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScreenshotConfig":
        """从字典创建"""
        return cls(
            enabled=data.get("enabled", True),
            save_dir=data.get("save_dir", "/tmp/lobster_browser_engine/screenshots"),
            format=ScreenshotFormat(data.get("format", "png")),
            quality=data.get("quality", 80),
            full_page=data.get("full_page", False),
            keep_all_screenshots=data.get("keep_all_screenshots", False),
            naming_pattern=data.get("naming_pattern", "{timestamp}_{action}_{step_id}"),
            auto_screenshot_on_error=data.get("auto_screenshot_on_error", True),
            auto_screenshot_on_success=data.get("auto_screenshot_on_success", False),
            auto_screenshot_between_steps=data.get("auto_screenshot_between_steps", False),
            max_screenshots=data.get("max_screenshots", 100),
            auto_cleanup=data.get("auto_cleanup", True),
            cleanup_after_days=data.get("cleanup_after_days", 7)
        )


@dataclass
class LogConfig:
    """
    日志配置
    
    管理日志相关设置
    """
    
    # 是否启用日志
    enabled: bool = True
    
    # 日志级别
    level: LogLevel = LogLevel.INFO
    
    # 日志保存目录
    save_dir: str = "/tmp/lobster_browser_engine/logs"
    
    # 日志文件名
    log_file: str = "browser_engine.log"
    
    # 日志格式
    format: str = "[{timestamp}] [{level}] [{module}] {message}"
    
    # 日志级别格式
    level_format: str = "{levelname:8s}"
    
    # 时间格式
    time_format: str = "%Y-%m-%d %H:%M:%S"
    
    # 是否输出到文件
    log_to_file: bool = True
    
    # 是否输出到控制台
    log_to_console: bool = True
    
    # 是否输出到系统日志
    log_to_syslog: bool = False
    
    # 最大日志文件大小（MB）
    max_file_size: int = 100
    
    # 保留日志文件数量
    backup_count: int = 10
    
    # 自动清理
    auto_cleanup: bool = True
    cleanup_after_days: int = 30
    
    # 是否记录详细错误
    verbose_errors: bool = True
    
    # 是否记录堆栈跟踪
    log_stack_trace: bool = True
    
    # 是否记录性能指标
    log_performance: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "enabled": self.enabled,
            "level": self.level.value,
            "save_dir": self.save_dir,
            "log_file": self.log_file,
            "format": self.format,
            "level_format": self.level_format,
            "time_format": self.time_format,
            "log_to_file": self.log_to_file,
            "log_to_console": self.log_to_console,
            "log_to_syslog": self.log_to_syslog,
            "max_file_size": self.max_file_size,
            "backup_count": self.backup_count,
            "auto_cleanup": self.auto_cleanup,
            "cleanup_after_days": self.cleanup_after_days,
            "verbose_errors": self.verbose_errors,
            "log_stack_trace": self.log_stack_trace,
            "log_performance": self.log_performance
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogConfig":
        """从字典创建"""
        return cls(
            enabled=data.get("enabled", True),
            level=LogLevel(data.get("level", "INFO")),
            save_dir=data.get("save_dir", "/tmp/lobster_browser_engine/logs"),
            log_file=data.get("log_file", "browser_engine.log"),
            format=data.get("format", "[{timestamp}] [{level}] [{module}] {message}"),
            level_format=data.get("level_format", "{levelname:8s}"),
            time_format=data.get("time_format", "%Y-%m-%d %H:%M:%S"),
            log_to_file=data.get("log_to_file", True),
            log_to_console=data.get("log_to_console", True),
            log_to_syslog=data.get("log_to_syslog", False),
            max_file_size=data.get("max_file_size", 100),
            backup_count=data.get("backup_count", 10),
            auto_cleanup=data.get("auto_cleanup", True),
            cleanup_after_days=data.get("cleanup_after_days", 30),
            verbose_errors=data.get("verbose_errors", True),
            log_stack_trace=data.get("log_stack_trace", True),
            log_performance=data.get("log_performance", True)
        )


@dataclass
class CacheConfig:
    """
    缓存配置
    
    管理缓存相关设置
    """
    
    # 是否启用缓存
    enabled: bool = True
    
    # 缓存策略
    strategy: CacheStrategy = CacheStrategy.MEMORY
    
    # 缓存过期时间（秒）
    ttl: int = 3600
    
    # 最大缓存数量
    max_items: int = 1000
    
    # Redis配置（如果使用Redis策略）
    redis_url: Optional[str] = None
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # 磁盘缓存目录（如果使用Disk策略）
    disk_cache_dir: str = "/tmp/lobster_browser_engine/cache"
    
    # 自动清理过期缓存
    auto_cleanup: bool = True
    
    # 清理间隔（秒）
    cleanup_interval: int = 300
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "enabled": self.enabled,
            "strategy": self.strategy.value,
            "ttl": self.ttl,
            "max_items": self.max_items,
            "redis_url": self.redis_url,
            "redis_db": self.redis_db,
            "redis_password": self.redis_password,
            "disk_cache_dir": self.disk_cache_dir,
            "auto_cleanup": self.auto_cleanup,
            "cleanup_interval": self.cleanup_interval
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheConfig":
        """从字典创建"""
        return cls(
            enabled=data.get("enabled", True),
            strategy=CacheStrategy(data.get("strategy", "memory")),
            ttl=data.get("ttl", 3600),
            max_items=data.get("max_items", 1000),
            redis_url=data.get("redis_url"),
            redis_db=data.get("redis_db", 0),
            redis_password=data.get("redis_password"),
            disk_cache_dir=data.get("disk_cache_dir", "/tmp/lobster_browser_engine/cache"),
            auto_cleanup=data.get("auto_cleanup", True),
            cleanup_interval=data.get("cleanup_interval", 300)
        )


@dataclass
class PerformanceConfig:
    """
    性能配置
    
    管理性能相关设置
    """
    
    # 最大并发操作数
    max_concurrent_actions: int = 5
    
    # 页面加载等待时间
    page_load_wait: float = 0.5
    
    # 操作后等待时间
    default_wait_after: float = 1.0
    
    # 慢动作模式（用于调试）
    slow_mo: int = 0  # 毫秒
    
    # 是否启用性能监控
    enable_performance_monitoring: bool = True
    
    # 性能阈值（毫秒）
    performance_threshold_warning: int = 5000
    performance_threshold_error: int = 10000
    
    # 是否启用资源优化
    enable_resource_optimization: bool = True
    
    # 资源加载策略
    resource_load_strategy: str = "normal"  # normal, eager, lazy
    
    # 是否阻止图片加载
    block_images: bool = False
    
    # 是否阻止CSS加载
    block_css: bool = False
    
    # 是否阻止字体加载
    block_fonts: bool = False
    
    # 网络限速（仅用于测试）
    network_throttling: Optional[Dict[str, int]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "max_concurrent_actions": self.max_concurrent_actions,
            "page_load_wait": self.page_load_wait,
            "default_wait_after": self.default_wait_after,
            "slow_mo": self.slow_mo,
            "enable_performance_monitoring": self.enable_performance_monitoring,
            "performance_threshold_warning": self.performance_threshold_warning,
            "performance_threshold_error": self.performance_threshold_error,
            "enable_resource_optimization": self.enable_resource_optimization,
            "resource_load_strategy": self.resource_load_strategy,
            "block_images": self.block_images,
            "block_css": self.block_css,
            "block_fonts": self.block_fonts,
            "network_throttling": self.network_throttling
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PerformanceConfig":
        """从字典创建"""
        return cls(
            max_concurrent_actions=data.get("max_concurrent_actions", 5),
            page_load_wait=data.get("page_load_wait", 0.5),
            default_wait_after=data.get("default_wait_after", 1.0),
            slow_mo=data.get("slow_mo", 0),
            enable_performance_monitoring=data.get("enable_performance_monitoring", True),
            performance_threshold_warning=data.get("performance_threshold_warning", 5000),
            performance_threshold_error=data.get("performance_threshold_error", 10000),
            enable_resource_optimization=data.get("enable_resource_optimization", True),
            resource_load_strategy=data.get("resource_load_strategy", "normal"),
            block_images=data.get("block_images", False),
            block_css=data.get("block_css", False),
            block_fonts=data.get("block_fonts", False),
            network_throttling=data.get("network_throttling")
        )


@dataclass
class EngineConfig:
    """
    引擎主配置
    
    整合所有配置项的主配置类
    """
    
    # 连接配置
    connection: ConnectionConfig = field(default_factory=ConnectionConfig)
    
    # 超时配置
    timeout: TimeoutConfig = field(default_factory=TimeoutConfig)
    
    # 重试配置
    retry: RetryConfig = field(default_factory=RetryConfig)
    
    # 截图配置
    screenshot: ScreenshotConfig = field(default_factory=ScreenshotConfig)
    
    # 日志配置
    log: LogConfig = field(default_factory=LogConfig)
    
    # 缓存配置
    cache: CacheConfig = field(default_factory=CacheConfig)
    
    # 性能配置
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # 调试模式
    debug: bool = False
    
    # 环境名称
    environment: str = "development"
    
    # 项目名称
    project_name: str = "lobster-browser-engine"
    
    # 版本
    version: str = "0.2.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "connection": self.connection.to_dict(),
            "timeout": self.timeout.to_dict(),
            "retry": self.retry.to_dict(),
            "screenshot": self.screenshot.to_dict(),
            "log": self.log.to_dict(),
            "cache": self.cache.to_dict(),
            "performance": self.performance.to_dict(),
            "debug": self.debug,
            "environment": self.environment,
            "project_name": self.project_name,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EngineConfig":
        """从字典创建"""
        return cls(
            connection=ConnectionConfig.from_dict(data.get("connection", {})),
            timeout=TimeoutConfig.from_dict(data.get("timeout", {})),
            retry=RetryConfig.from_dict(data.get("retry", {})),
            screenshot=ScreenshotConfig.from_dict(data.get("screenshot", {})),
            log=LogConfig.from_dict(data.get("log", {})),
            cache=CacheConfig.from_dict(data.get("cache", {})),
            performance=PerformanceConfig.from_dict(data.get("performance", {})),
            debug=data.get("debug", False),
            environment=data.get("environment", "development"),
            project_name=data.get("project_name", "lobster-browser-engine"),
            version=data.get("version", "0.2.0")
        )
    
    @classmethod
    def from_json_file(cls, file_path: str) -> "EngineConfig":
        """从JSON文件加载配置"""
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def to_json_file(self, file_path: str) -> None:
        """保存配置到JSON文件"""
        import json
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def merge(self, other: "EngineConfig") -> "EngineConfig":
        """合并配置（other覆盖self）"""
        import copy
        merged = copy.deepcopy(self)
        
        # 合并各个子配置
        for attr in ['connection', 'timeout', 'retry', 'screenshot', 'log', 'cache', 'performance']:
            other_value = getattr(other, attr)
            self_value = getattr(merged, attr)
            
            # 合并字典
            merged_dict = self_value.to_dict()
            merged_dict.update(other_value.to_dict())
            
            setattr(merged, attr, type(self_value).from_dict(merged_dict))
        
        # 合并简单属性
        for attr in ['debug', 'environment', 'project_name', 'version']:
            other_value = getattr(other, attr)
            if other_value is not None:
                setattr(merged, attr, other_value)
        
        return merged
