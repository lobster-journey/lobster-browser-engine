"""
Lobster Browser Engine - Flow Validator
流程验证器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import json
from typing import Dict, List, Tuple
from pathlib import Path
from ..enums import ActionType
from ..exceptions import FlowValidationException


class FlowValidator:
    """
    流程验证器
    
    负责验证流程配置的正确性和完整性
    """
    
    def __init__(self):
        """初始化验证器"""
        self.errors = []
        self.warnings = []
    
    def validate(self, flow_config: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        验证流程配置
        
        Args:
            flow_config: 流程配置
            
        Returns:
            Tuple[bool, List[str], List[str]]: (是否有效, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []
        
        # 验证基本信息
        self._validate_basic_info(flow_config)
        
        # 验证步骤
        self._validate_steps(flow_config.get("steps", []))
        
        # 验证钩子
        self._validate_hooks(flow_config.get("before_hooks", []), "before_hooks")
        self._validate_hooks(flow_config.get("after_hooks", []), "after_hooks")
        
        # 验证参数定义
        self._validate_params(flow_config.get("params", {}))
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_basic_info(self, flow_config: Dict) -> None:
        """验证基本信息"""
        if "name" not in flow_config:
            self.errors.append("Missing required field: name")
        
        if "version" not in flow_config:
            self.warnings.append("Missing recommended field: version")
        
        if "description" not in flow_config:
            self.warnings.append("Missing recommended field: description")
        
        if "steps" not in flow_config or not flow_config["steps"]:
            self.errors.append("Flow must have at least one step")
    
    def _validate_steps(self, steps: List[Dict]) -> None:
        """验证步骤列表"""
        if not steps:
            return
        
        step_ids = set()
        
        for i, step in enumerate(steps):
            step_num = i + 1
            
            # 验证步骤ID
            step_id = step.get("step_id", i)
            if step_id in step_ids:
                self.errors.append(f"Step {step_num}: Duplicate step_id {step_id}")
            step_ids.add(step_id)
            
            # 验证步骤名称
            if "name" not in step:
                self.warnings.append(f"Step {step_num}: Missing recommended field: name")
            
            # 验证操作类型
            if "action" not in step:
                self.errors.append(f"Step {step_num}: Missing required field: action")
            else:
                action = step["action"]
                try:
                    ActionType(action)
                except ValueError:
                    self.errors.append(f"Step {step_num}: Invalid action type: {action}")
            
            # 验证参数
            if "params" not in step:
                self.warnings.append(f"Step {step_num}: Missing params field")
            else:
                self._validate_step_params(step["params"], step_num)
            
            # 验证条件
            if "condition" in step:
                self._validate_condition(step["condition"], step_num)
    
    def _validate_step_params(self, params: Dict, step_num: int) -> None:
        """验证步骤参数"""
        if not isinstance(params, dict):
            self.errors.append(f"Step {step_num}: params must be a dictionary")
            return
        
        # 这里可以添加更详细的参数验证
        # 例如：检查必需参数、参数类型等
    
    def _validate_condition(self, condition: Dict, step_num: int) -> None:
        """验证条件"""
        if "type" not in condition:
            self.errors.append(f"Step {step_num}: Condition missing required field: type")
            return
        
        condition_type = condition["type"]
        valid_types = [
            "element_exists", "element_visible", "element_hidden",
            "url_contains", "url_matches", "title_contains",
            "javascript"
        ]
        
        if condition_type not in valid_types:
            self.errors.append(f"Step {step_num}: Invalid condition type: {condition_type}")
    
    def _validate_hooks(self, hooks: List[Dict], hook_type: str) -> None:
        """验证钩子"""
        if not hooks:
            return
        
        for i, hook in enumerate(hooks):
            hook_num = i + 1
            
            if "action" not in hook:
                self.errors.append(f"{hook_type}[{hook_num}]: Missing required field: action")
            
            if "params" not in hook:
                self.warnings.append(f"{hook_type}[{hook_num}]: Missing params field")
    
    def _validate_params(self, params: Dict) -> None:
        """验证参数定义"""
        if not params:
            return
        
        for param_name, param_config in params.items():
            if "type" not in param_config:
                self.warnings.append(f"Param '{param_name}': Missing type field")
            
            if "default" not in param_config and param_config.get("required", False):
                self.errors.append(f"Param '{param_name}': Required parameter must have default value")
    
    def validate_file(self, file_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        验证流程文件
        
        Args:
            file_path: 流程文件路径
            
        Returns:
            Tuple[bool, List[str], List[str]]: (是否有效, 错误列表, 警告列表)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                flow_config = json.load(f)
            
            return self.validate(flow_config)
            
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {str(e)}"], []
        except FileNotFoundError:
            return False, [f"File not found: {file_path}"], []
        except Exception as e:
            return False, [f"Validation error: {str(e)}"], []
