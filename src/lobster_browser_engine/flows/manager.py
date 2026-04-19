"""
Lobster Browser Engine - Flow Manager
流程管理器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from ..exceptions import FlowNotFoundException


class FlowManager:
    """
    流程管理器
    
    负责流程的CRUD操作和管理
    """
    
    def __init__(self, flows_dir: Optional[str] = None):
        """
        初始化流程管理器
        
        Args:
            flows_dir: 流程配置目录，默认为项目的flows目录
        """
        self.flows_dir = Path(flows_dir) if flows_dir else Path(__file__).parent.parent.parent.parent / "flows"
        self.flows_dir.mkdir(parents=True, exist_ok=True)
    
    def create(self, flow_config: Dict) -> str:
        """
        创建新流程
        
        Args:
            flow_config: 流程配置
            
        Returns:
            str: 流程名称
        """
        flow_name = flow_config.get("name")
        if not flow_name:
            raise ValueError("Flow name is required")
        
        # 添加元数据
        flow_config["created_at"] = datetime.now().isoformat()
        flow_config["updated_at"] = datetime.now().isoformat()
        
        # 保存流程文件
        flow_file = self.flows_dir / f"{flow_name}.json"
        with open(flow_file, 'w', encoding='utf-8') as f:
            json.dump(flow_config, f, indent=2, ensure_ascii=False)
        
        return flow_name
    
    def read(self, flow_name: str) -> Dict:
        """
        读取流程配置
        
        Args:
            flow_name: 流程名称
            
        Returns:
            Dict: 流程配置
            
        Raises:
            FlowNotFoundException: 流程未找到
        """
        flow_file = self.flows_dir / f"{flow_name}.json"
        
        if not flow_file.exists():
            raise FlowNotFoundException(flow_name)
        
        with open(flow_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update(self, flow_name: str, updates: Dict) -> Dict:
        """
        更新流程配置
        
        Args:
            flow_name: 流程名称
            updates: 更新内容
            
        Returns:
            Dict: 更新后的流程配置
            
        Raises:
            FlowNotFoundException: 流程未找到
        """
        flow_config = self.read(flow_name)
        
        # 合并更新
        flow_config.update(updates)
        flow_config["updated_at"] = datetime.now().isoformat()
        
        # 保存
        flow_file = self.flows_dir / f"{flow_name}.json"
        with open(flow_file, 'w', encoding='utf-8') as f:
            json.dump(flow_config, f, indent=2, ensure_ascii=False)
        
        return flow_config
    
    def delete(self, flow_name: str) -> bool:
        """
        删除流程
        
        Args:
            flow_name: 流程名称
            
        Returns:
            bool: 是否成功
            
        Raises:
            FlowNotFoundException: 流程未找到
        """
        flow_file = self.flows_dir / f"{flow_name}.json"
        
        if not flow_file.exists():
            raise FlowNotFoundException(flow_name)
        
        flow_file.unlink()
        return True
    
    def list_flows(self) -> List[Dict]:
        """
        列出所有流程
        
        Returns:
            List[Dict]: 流程列表
        """
        flows = []
        
        for flow_file in self.flows_dir.glob("*.json"):
            try:
                with open(flow_file, 'r', encoding='utf-8') as f:
                    flow_config = json.load(f)
                
                flows.append({
                    "name": flow_config.get("name", flow_file.stem),
                    "version": flow_config.get("version", "1.0.0"),
                    "description": flow_config.get("description", ""),
                    "steps_count": len(flow_config.get("steps", [])),
                    "created_at": flow_config.get("created_at", ""),
                    "updated_at": flow_config.get("updated_at", "")
                })
            except Exception:
                # 跳过无效的流程文件
                continue
        
        return flows
    
    def duplicate(self, flow_name: str, new_name: str) -> str:
        """
        复制流程
        
        Args:
            flow_name: 原流程名称
            new_name: 新流程名称
            
        Returns:
            str: 新流程名称
        """
        flow_config = self.read(flow_name)
        flow_config["name"] = new_name
        
        return self.create(flow_config)
    
    def export(self, flow_name: str) -> str:
        """
        导出流程为JSON字符串
        
        Args:
            flow_name: 流程名称
            
        Returns:
            str: JSON字符串
        """
        flow_config = self.read(flow_name)
        return json.dumps(flow_config, indent=2, ensure_ascii=False)
    
    def import_flow(self, flow_json: str) -> str:
        """
        从JSON字符串导入流程
        
        Args:
            flow_json: JSON字符串
            
        Returns:
            str: 流程名称
        """
        flow_config = json.loads(flow_json)
        return self.create(flow_config)
