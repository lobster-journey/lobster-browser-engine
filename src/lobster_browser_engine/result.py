"""
Lobster Browser Engine - Core Result
核心结果对象定义

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from .enums import ActionType, FlowStatus


@dataclass
class ActionResult:
    """
    操作执行结果
    
    记录单个操作的执行结果
    """
    
    # 是否成功
    success: bool
    
    # 操作类型
    action_type: ActionType
    
    # 返回数据
    data: Optional[Any] = None
    
    # 截图路径
    screenshot: Optional[str] = None
    
    # 错误信息
    error: Optional[str] = None
    
    # 错误堆栈
    error_stack: Optional[str] = None
    
    # 执行时长（毫秒）
    duration: float = 0.0
    
    # 重试次数
    retry_count: int = 0
    
    # 时间戳
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 额外信息
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "action_type": self.action_type.value if isinstance(self.action_type, ActionType) else self.action_type,
            "data": self.data,
            "screenshot": self.screenshot,
            "error": self.error,
            "error_stack": self.error_stack,
            "duration": self.duration,
            "retry_count": self.retry_count,
            "timestamp": self.timestamp,
            "extra": self.extra
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActionResult":
        """从字典创建"""
        return cls(
            success=data.get("success", False),
            action_type=ActionType(data.get("action_type", "navigate")),
            data=data.get("data"),
            screenshot=data.get("screenshot"),
            error=data.get("error"),
            error_stack=data.get("error_stack"),
            duration=data.get("duration", 0.0),
            retry_count=data.get("retry_count", 0),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            extra=data.get("extra", {})
        )
    
    def is_successful(self) -> bool:
        """判断是否成功"""
        return self.success and not self.error
    
    def has_screenshot(self) -> bool:
        """判断是否有截图"""
        return self.screenshot is not None
    
    def get_duration_seconds(self) -> float:
        """获取执行时长（秒）"""
        return self.duration / 1000.0
    
    def get_duration_human(self) -> str:
        """获取人类可读的执行时长"""
        seconds = self.get_duration_seconds()
        if seconds < 1:
            return f"{int(seconds * 1000)}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        else:
            minutes = int(seconds / 60)
            seconds_remain = seconds % 60
            return f"{minutes}m {seconds_remain:.2f}s"


@dataclass
class StepResult:
    """
    步骤执行结果
    
    记录流程中单个步骤的执行结果
    """
    
    # 是否成功
    success: bool
    
    # 步骤ID
    step_id: int
    
    # 步骤名称
    step_name: str = ""
    
    # 步骤描述
    description: str = ""
    
    # 操作结果
    action_result: Optional[ActionResult] = None
    
    # 错误信息
    error: Optional[str] = None
    
    # 执行时长（毫秒）
    duration: float = 0.0
    
    # 时间戳
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 是否可选
    optional: bool = False
    
    # 是否跳过
    skipped: bool = False
    
    # 跳过原因
    skip_reason: Optional[str] = None
    
    # 截图路径列表
    screenshots: List[str] = field(default_factory=list)
    
    # 日志信息
    logs: List[str] = field(default_factory=list)
    
    # 额外信息
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "step_id": self.step_id,
            "step_name": self.step_name,
            "description": self.description,
            "action_result": self.action_result.to_dict() if self.action_result else None,
            "error": self.error,
            "duration": self.duration,
            "timestamp": self.timestamp,
            "optional": self.optional,
            "skipped": self.skipped,
            "skip_reason": self.skip_reason,
            "screenshots": self.screenshots,
            "logs": self.logs,
            "extra": self.extra
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StepResult":
        """从字典创建"""
        action_result_data = data.get("action_result")
        return cls(
            success=data.get("success", False),
            step_id=data.get("step_id", 0),
            step_name=data.get("step_name", ""),
            description=data.get("description", ""),
            action_result=ActionResult.from_dict(action_result_data) if action_result_data else None,
            error=data.get("error"),
            duration=data.get("duration", 0.0),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            optional=data.get("optional", False),
            skipped=data.get("skipped", False),
            skip_reason=data.get("skip_reason"),
            screenshots=data.get("screenshots", []),
            logs=data.get("logs", []),
            extra=data.get("extra", {})
        )
    
    def is_successful(self) -> bool:
        """判断是否成功"""
        if self.skipped:
            return self.optional
        return self.success and not self.error
    
    def add_screenshot(self, screenshot_path: str) -> None:
        """添加截图"""
        self.screenshots.append(screenshot_path)
    
    def add_log(self, log_message: str) -> None:
        """添加日志"""
        self.logs.append(log_message)


@dataclass
class FlowResult:
    """
    流程执行结果
    
    记录整个流程的执行结果
    """
    
    # 是否成功
    success: bool
    
    # 流程名称
    flow_name: str
    
    # 流程版本
    flow_version: str = "1.0.0"
    
    # 流程状态
    status: FlowStatus = FlowStatus.PENDING
    
    # 总步骤数
    steps_total: int = 0
    
    # 执行步骤数
    steps_executed: int = 0
    
    # 成功步骤数
    steps_success: int = 0
    
    # 失败步骤数
    steps_failed: int = 0
    
    # 跳过步骤数
    steps_skipped: int = 0
    
    # 步骤结果列表
    step_results: List[StepResult] = field(default_factory=list)
    
    # 截图路径列表
    screenshots: List[str] = field(default_factory=list)
    
    # 返回数据
    data: Dict[str, Any] = field(default_factory=dict)
    
    # 错误信息
    error: Optional[str] = None
    
    # 错误堆栈
    error_stack: Optional[str] = None
    
    # 失败步骤ID
    error_step: Optional[int] = None
    
    # 执行时长（毫秒）
    duration: float = 0.0
    
    # 开始时间
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 结束时间
    end_time: Optional[str] = None
    
    # 重试次数
    retry_count: int = 0
    
    # 执行环境
    environment: str = "development"
    
    # 执行参数
    params: Dict[str, Any] = field(default_factory=dict)
    
    # 性能指标
    performance: Dict[str, Any] = field(default_factory=dict)
    
    # 日志信息
    logs: List[str] = field(default_factory=list)
    
    # 额外信息
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "flow_name": self.flow_name,
            "flow_version": self.flow_version,
            "status": self.status.value if isinstance(self.status, FlowStatus) else self.status,
            "steps_total": self.steps_total,
            "steps_executed": self.steps_executed,
            "steps_success": self.steps_success,
            "steps_failed": self.steps_failed,
            "steps_skipped": self.steps_skipped,
            "step_results": [r.to_dict() for r in self.step_results],
            "screenshots": self.screenshots,
            "data": self.data,
            "error": self.error,
            "error_stack": self.error_stack,
            "error_step": self.error_step,
            "duration": self.duration,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "retry_count": self.retry_count,
            "environment": self.environment,
            "params": self.params,
            "performance": self.performance,
            "logs": self.logs,
            "extra": self.extra
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FlowResult":
        """从字典创建"""
        return cls(
            success=data.get("success", False),
            flow_name=data.get("flow_name", ""),
            flow_version=data.get("flow_version", "1.0.0"),
            status=FlowStatus(data.get("status", "pending")),
            steps_total=data.get("steps_total", 0),
            steps_executed=data.get("steps_executed", 0),
            steps_success=data.get("steps_success", 0),
            steps_failed=data.get("steps_failed", 0),
            steps_skipped=data.get("steps_skipped", 0),
            step_results=[StepResult.from_dict(r) for r in data.get("step_results", [])],
            screenshots=data.get("screenshots", []),
            data=data.get("data", {}),
            error=data.get("error"),
            error_stack=data.get("error_stack"),
            error_step=data.get("error_step"),
            duration=data.get("duration", 0.0),
            start_time=data.get("start_time", datetime.now().isoformat()),
            end_time=data.get("end_time"),
            retry_count=data.get("retry_count", 0),
            environment=data.get("environment", "development"),
            params=data.get("params", {}),
            performance=data.get("performance", {}),
            logs=data.get("logs", []),
            extra=data.get("extra", {})
        )
    
    def is_successful(self) -> bool:
        """判断是否成功"""
        return self.success and not self.error
    
    def add_step_result(self, step_result: StepResult) -> None:
        """添加步骤结果"""
        self.step_results.append(step_result)
        self.steps_executed += 1
        
        if step_result.is_successful():
            self.steps_success += 1
        elif step_result.skipped:
            self.steps_skipped += 1
        else:
            self.steps_failed += 1
    
    def add_screenshot(self, screenshot_path: str) -> None:
        """添加截图"""
        self.screenshots.append(screenshot_path)
    
    def add_log(self, log_message: str) -> None:
        """添加日志"""
        self.logs.append(log_message)
    
    def get_duration_seconds(self) -> float:
        """获取执行时长（秒）"""
        return self.duration / 1000.0
    
    def get_duration_human(self) -> str:
        """获取人类可读的执行时长"""
        seconds = self.get_duration_seconds()
        if seconds < 1:
            return f"{int(seconds * 1000)}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            seconds_remain = seconds % 60
            return f"{minutes}m {seconds_remain:.2f}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            seconds_remain = seconds % 60
            return f"{hours}h {minutes}m {seconds_remain:.2f}s"
    
    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.steps_executed == 0:
            return 0.0
        return (self.steps_success / self.steps_executed) * 100
    
    def get_failed_steps(self) -> List[StepResult]:
        """获取失败的步骤"""
        return [s for s in self.step_results if not s.is_successful() and not s.skipped]
    
    def get_last_screenshot(self) -> Optional[str]:
        """获取最后一张截图"""
        return self.screenshots[-1] if self.screenshots else None
    
    def get_all_screenshots(self) -> List[str]:
        """获取所有截图"""
        return self.screenshots
    
    def mark_completed(self, success: bool = True) -> None:
        """标记完成"""
        self.end_time = datetime.now().isoformat()
        self.success = success
        self.status = FlowStatus.SUCCESS if success else FlowStatus.FAILED
        
        # 计算总时长
        if self.start_time and self.end_time:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            self.duration = (end - start).total_seconds() * 1000
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        import json
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> "FlowResult":
        """从JSON字符串创建"""
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save_to_file(self, file_path: str) -> None:
        """保存到文件"""
        from pathlib import Path
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_from_file(cls, file_path: str) -> "FlowResult":
        """从文件加载"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    def get_summary(self) -> str:
        """获取摘要信息"""
        status_emoji = "✅" if self.success else "❌"
        return (
            f"{status_emoji} {self.flow_name} v{self.flow_version}\n"
            f"Status: {self.status.value}\n"
            f"Steps: {self.steps_executed}/{self.steps_total} "
            f"(Success: {self.steps_success}, Failed: {self.steps_failed}, Skipped: {self.steps_skipped})\n"
            f"Duration: {self.get_duration_human()}\n"
            f"Success Rate: {self.get_success_rate():.1f}%"
        )


@dataclass
class BatchResult:
    """
    批量执行结果
    
    记录批量执行多个流程的结果
    """
    
    # 是否全部成功
    success: bool
    
    # 流程名称列表
    flow_names: List[str] = field(default_factory=list)
    
    # 流程结果列表
    flow_results: List[FlowResult] = field(default_factory=list)
    
    # 总流程数
    total: int = 0
    
    # 成功数
    success_count: int = 0
    
    # 失败数
    failed_count: int = 0
    
    # 执行时长（毫秒）
    duration: float = 0.0
    
    # 开始时间
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 结束时间
    end_time: Optional[str] = None
    
    # 错误信息
    error: Optional[str] = None
    
    # 额外信息
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "flow_names": self.flow_names,
            "flow_results": [r.to_dict() for r in self.flow_results],
            "total": self.total,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "duration": self.duration,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error": self.error,
            "extra": self.extra
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchResult":
        """从字典创建"""
        return cls(
            success=data.get("success", False),
            flow_names=data.get("flow_names", []),
            flow_results=[FlowResult.from_dict(r) for r in data.get("flow_results", [])],
            total=data.get("total", 0),
            success_count=data.get("success_count", 0),
            failed_count=data.get("failed_count", 0),
            duration=data.get("duration", 0.0),
            start_time=data.get("start_time", datetime.now().isoformat()),
            end_time=data.get("end_time"),
            error=data.get("error"),
            extra=data.get("extra", {})
        )
    
    def add_flow_result(self, flow_result: FlowResult) -> None:
        """添加流程结果"""
        self.flow_names.append(flow_result.flow_name)
        self.flow_results.append(flow_result)
        self.total += 1
        
        if flow_result.success:
            self.success_count += 1
        else:
            self.failed_count += 1
    
    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.total == 0:
            return 0.0
        return (self.success_count / self.total) * 100
    
    def mark_completed(self) -> None:
        """标记完成"""
        self.end_time = datetime.now().isoformat()
        self.success = self.failed_count == 0
        
        # 计算总时长
        if self.start_time and self.end_time:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            self.duration = (end - start).total_seconds() * 1000
    
    def get_summary(self) -> str:
        """获取摘要信息"""
        status_emoji = "✅" if self.success else "❌"
        return (
            f"{status_emoji} Batch Execution\n"
            f"Total: {self.total}\n"
            f"Success: {self.success_count}\n"
            f"Failed: {self.failed_count}\n"
            f"Duration: {self.duration / 1000.0:.2f}s\n"
            f"Success Rate: {self.get_success_rate():.1f}%"
        )
