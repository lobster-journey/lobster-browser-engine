"""
Lobster Browser Engine - Flow Monitor
流程监控器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from ..result import FlowResult


class FlowMonitor:
    """
    流程监控器
    
    负责监控流程执行状态和性能指标
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        初始化监控器
        
        Args:
            log_dir: 日志目录
        """
        self.log_dir = Path(log_dir) if log_dir else Path.home() / ".openclaw/workspace/logs/flow_monitor"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.execution_history: List[Dict] = []
        self.active_flows: Dict[str, Dict] = {}
    
    def start_flow(self, flow_name: str, flow_id: str) -> None:
        """
        记录流程开始
        
        Args:
            flow_name: 流程名称
            flow_id: 流程实例ID
        """
        self.active_flows[flow_id] = {
            "flow_name": flow_name,
            "flow_id": flow_id,
            "start_time": datetime.now().isoformat(),
            "status": "running"
        }
    
    def end_flow(self, flow_id: str, result: FlowResult) -> None:
        """
        记录流程结束
        
        Args:
            flow_id: 流程实例ID
            result: 流程执行结果
        """
        if flow_id in self.active_flows:
            flow_record = self.active_flows.pop(flow_id)
            flow_record["end_time"] = datetime.now().isoformat()
            flow_record["status"] = "success" if result.success else "failed"
            flow_record["result"] = result.to_dict()
            
            # 保存到历史记录
            self.execution_history.append(flow_record)
            
            # 保存到文件
            self._save_to_log(flow_record)
    
    def get_active_flows(self) -> List[Dict]:
        """
        获取正在执行的流程列表
        
        Returns:
            List[Dict]: 活动流程列表
        """
        return list(self.active_flows.values())
    
    def get_execution_history(self, limit: int = 100) -> List[Dict]:
        """
        获取执行历史
        
        Args:
            limit: 最大返回数量
            
        Returns:
            List[Dict]: 执行历史列表
        """
        return self.execution_history[-limit:]
    
    def get_statistics(self, flow_name: Optional[str] = None) -> Dict:
        """
        获取统计数据
        
        Args:
            flow_name: 流程名称，不指定则返回所有流程的统计
            
        Returns:
            Dict: 统计数据
        """
        history = self.execution_history
        
        if flow_name:
            history = [h for h in history if h.get("flow_name") == flow_name]
        
        if not history:
            return {
                "total_executions": 0,
                "success_count": 0,
                "failed_count": 0,
                "success_rate": 0.0,
                "avg_duration": 0.0
            }
        
        total = len(history)
        success_count = sum(1 for h in history if h.get("status") == "success")
        failed_count = total - success_count
        
        # 计算平均执行时长
        durations = []
        for h in history:
            if "result" in h:
                durations.append(h["result"].get("duration", 0))
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_executions": total,
            "success_count": success_count,
            "failed_count": failed_count,
            "success_rate": (success_count / total * 100) if total > 0 else 0.0,
            "avg_duration": avg_duration
        }
    
    def clear_history(self) -> None:
        """清空历史记录"""
        self.execution_history.clear()
    
    def _save_to_log(self, flow_record: Dict) -> None:
        """保存到日志文件"""
        log_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(flow_record, ensure_ascii=False) + "\n")
    
    def export_history(self, file_path: str, flow_name: Optional[str] = None) -> None:
        """
        导出历史记录
        
        Args:
            file_path: 导出文件路径
            flow_name: 流程名称，不指定则导出所有
        """
        history = self.execution_history
        
        if flow_name:
            history = [h for h in history if h.get("flow_name") == flow_name]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
