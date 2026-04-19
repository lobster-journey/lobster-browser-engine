"""
Lobster Browser Engine - Logger
日志管理器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from ..config import LogConfig, LogLevel


class Logger:
    """
    日志管理器
    
    提供统一的日志记录功能
    """
    
    def __init__(self, config: LogConfig):
        """
        初始化日志管理器
        
        Args:
            config: 日志配置
        """
        self.config = config
        self.logger = logging.getLogger("lobster_browser_engine")
        self.logger.setLevel(getattr(logging, config.level.value))
        
        # 清除已有的handlers
        self.logger.handlers.clear()
        
        # 设置格式
        formatter = logging.Formatter(
            config.format,
            datefmt=config.time_format
        )
        
        # 添加控制台handler
        if config.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # 添加文件handler
        if config.log_to_file:
            log_file = Path(config.save_dir) / config.log_file
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录ERROR级别日志"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """记录CRITICAL级别日志"""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """记录异常日志"""
        self.logger.exception(message)
