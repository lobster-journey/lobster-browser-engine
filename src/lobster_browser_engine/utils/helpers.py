"""
Lobster Browser Engine - Helpers
辅助工具函数

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import re
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path


class Helpers:
    """辅助工具类"""
    
    @staticmethod
    def format_duration(milliseconds: float) -> str:
        """
        格式化时长
        
        Args:
            milliseconds: 毫秒数
            
        Returns:
            str: 格式化的时长字符串
        """
        seconds = milliseconds / 1000
        
        if seconds < 1:
            return f"{int(seconds * 1000)}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.2f}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            secs = seconds % 60
            return f"{hours}h {minutes}m {secs:.2f}s"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        清理文件名
        
        Args:
            filename: 原始文件名
            
        Returns:
            str: 清理后的文件名
        """
        # 移除非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # 替换空格为下划线
        filename = filename.replace(' ', '_')
        # 限制长度
        return filename[:255]
    
    @staticmethod
    def merge_dicts(base: Dict, override: Dict) -> Dict:
        """
        深度合并字典
        
        Args:
            base: 基础字典
            override: 覆盖字典
            
        Returns:
            Dict: 合并后的字典
        """
        import copy
        result = copy.deepcopy(base)
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Helpers.merge_dicts(result[key], value)
            else:
                result[key] = copy.deepcopy(value)
        
        return result
    
    @staticmethod
    def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """
        扁平化字典
        
        Args:
            d: 字典
            parent_key: 父键
            sep: 分隔符
            
        Returns:
            Dict: 扁平化的字典
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(Helpers.flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def generate_timestamp() -> str:
        """
        生成时间戳字符串
        
        Returns:
            str: 时间戳
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def ensure_dir(path: str) -> Path:
        """
        确保目录存在
        
        Args:
            path: 目录路径
            
        Returns:
            Path: Path对象
        """
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    @staticmethod
    def load_json(file_path: str) -> Dict:
        """
        加载JSON文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: JSON数据
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_json(data: Dict, file_path: str, indent: int = 2) -> None:
        """
        保存到JSON文件
        
        Args:
            data: 数据
            file_path: 文件路径
            indent: 缩进
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
