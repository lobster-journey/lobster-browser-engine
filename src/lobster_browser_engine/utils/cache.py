"""
Lobster Browser Engine - Cache Manager
缓存管理器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import json
import time
from typing import Any, Optional
from pathlib import Path
from ..config import CacheConfig
from ..enums import CacheStrategy


class CacheManager:
    """
    缓存管理器
    
    提供内存和磁盘缓存功能
    """
    
    def __init__(self, config: CacheConfig):
        """
        初始化缓存管理器
        
        Args:
            config: 缓存配置
        """
        self.config = config
        self._memory_cache = {}
        self._cache_times = {}
        
        if config.strategy == CacheStrategy.DISK:
            self.cache_dir = Path(config.disk_cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
            
        Returns:
            Optional[Any]: 缓存值，不存在或过期返回None
        """
        if not self.config.enabled:
            return None
        
        if self.config.strategy == CacheStrategy.MEMORY:
            return self._get_from_memory(key)
        elif self.config.strategy == CacheStrategy.DISK:
            return self._get_from_disk(key)
        
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        if not self.config.enabled:
            return
        
        if self.config.strategy == CacheStrategy.MEMORY:
            self._set_to_memory(key, value)
        elif self.config.strategy == CacheStrategy.DISK:
            self._set_to_disk(key, value)
    
    def delete(self, key: str) -> None:
        """
        删除缓存
        
        Args:
            key: 缓存键
        """
        if self.config.strategy == CacheStrategy.MEMORY:
            self._memory_cache.pop(key, None)
            self._cache_times.pop(key, None)
        elif self.config.strategy == CacheStrategy.DISK:
            cache_file = self.cache_dir / f"{key}.json"
            cache_file.unlink(missing_ok=True)
    
    def clear(self) -> None:
        """清空缓存"""
        if self.config.strategy == CacheStrategy.MEMORY:
            self._memory_cache.clear()
            self._cache_times.clear()
        elif self.config.strategy == CacheStrategy.DISK:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
    
    def _get_from_memory(self, key: str) -> Optional[Any]:
        """从内存缓存获取"""
        if key not in self._memory_cache:
            return None
        
        # 检查是否过期
        if time.time() - self._cache_times.get(key, 0) > self.config.ttl:
            self.delete(key)
            return None
        
        return self._memory_cache[key]
    
    def _set_to_memory(self, key: str, value: Any) -> None:
        """设置到内存缓存"""
        # 检查缓存数量限制
        if len(self._memory_cache) >= self.config.max_items:
            # 删除最旧的缓存
            oldest_key = min(self._cache_times.keys(), key=lambda k: self._cache_times[k])
            self.delete(oldest_key)
        
        self._memory_cache[key] = value
        self._cache_times[key] = time.time()
    
    def _get_from_disk(self, key: str) -> Optional[Any]:
        """从磁盘缓存获取"""
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        # 检查是否过期
        if time.time() - cache_file.stat().st_mtime > self.config.ttl:
            cache_file.unlink()
            return None
        
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _set_to_disk(self, key: str, value: Any) -> None:
        """设置到磁盘缓存"""
        cache_file = self.cache_dir / f"{key}.json"
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False)
