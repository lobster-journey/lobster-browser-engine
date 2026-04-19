"""
Lobster Browser Engine - Screenshot Manager
截图管理器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from pathlib import Path
from typing import Optional, List
from datetime import datetime
from ..config import ScreenshotConfig


class ScreenshotManager:
    """
    截图管理器
    
    负责截图的保存、管理和清理
    """
    
    def __init__(self, config: ScreenshotConfig):
        """
        初始化截图管理器
        
        Args:
            config: 截图配置
        """
        self.config = config
        self.screenshot_dir = Path(config.save_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(
        self,
        action: str,
        step_id: Optional[int] = None,
        custom_name: Optional[str] = None
    ) -> str:
        """
        生成截图文件名
        
        Args:
            action: 操作类型
            step_id: 步骤ID
            custom_name: 自定义名称
            
        Returns:
            str: 文件名
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = self.config.format.value
        
        if custom_name:
            return f"{custom_name}.{extension}"
        
        parts = [timestamp, action]
        if step_id is not None:
            parts.append(f"step{step_id}")
        
        return f"{'_'.join(parts)}.{extension}"
    
    def get_screenshot_path(self, filename: str) -> Path:
        """
        获取截图完整路径
        
        Args:
            filename: 文件名
            
        Returns:
            Path: 完整路径
        """
        return self.screenshot_dir / filename
    
    def list_screenshots(self) -> List[Path]:
        """
        列出所有截图
        
        Returns:
            List[Path]: 截图文件列表
        """
        pattern = f"*.{self.config.format.value}"
        return list(self.screenshot_dir.glob(pattern))
    
    def cleanup_old_screenshots(self) -> int:
        """
        清理旧截图
        
        Returns:
            int: 删除的文件数量
        """
        if not self.config.auto_cleanup:
            return 0
        
        cutoff = datetime.now().timestamp() - (self.config.cleanup_after_days * 86400)
        deleted = 0
        
        for screenshot in self.list_screenshots():
            if screenshot.stat().st_mtime < cutoff:
                screenshot.unlink()
                deleted += 1
        
        return deleted
    
    def get_total_size(self) -> int:
        """
        获取截图总大小（字节）
        
        Returns:
            int: 总大小
        """
        return sum(s.stat().st_size for s in self.list_screenshots())
    
    def get_screenshot_count(self) -> int:
        """
        获取截图数量
        
        Returns:
            int: 截图数量
        """
        return len(self.list_screenshots())
