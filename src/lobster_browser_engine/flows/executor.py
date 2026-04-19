"""
Lobster Browser Engine - Flow Executor
流程执行器

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from pathlib import Path
from playwright.async_api import Page
from ..config import EngineConfig
from ..result import FlowResult, StepResult
from ..enums import FlowStatus
from ..exceptions import FlowNotFoundException, FlowExecutionException
from ..actions.factory import ActionFactory


class FlowExecutor:
    """
    流程执行器
    
    负责执行预定义的浏览器自动化流程
    """
    
    def __init__(self, page: Page, config: EngineConfig):
        """
        初始化流程执行器
        
        Args:
            page: Playwright页面对象
            config: 引擎配置
        """
        self.page = page
        self.config = config
        self.flows_dir = Path(__file__).parent.parent.parent.parent / "flows"
    
    async def execute(
        self,
        flow_name: str,
        params: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """
        执行流程
        
        Args:
            flow_name: 流程名称（不含.json扩展名）
            params: 流程参数
            variables: 流程变量
            
        Returns:
            FlowResult: 流程执行结果
            
        Raises:
            FlowNotFoundException: 流程未找到
            FlowExecutionException: 流程执行失败
        """
        # 加载流程配置
        flow_config = await self._load_flow(flow_name)
        if not flow_config:
            raise FlowNotFoundException(flow_name)
        
        # 创建结果对象
        result = FlowResult(
            success=False,
            flow_name=flow_config.get("name", flow_name),
            flow_version=flow_config.get("version", "1.0.0"),
            status=FlowStatus.RUNNING,
            steps_total=len(flow_config.get("steps", [])),
            params=params or {},
            environment=self.config.environment
        )
        
        try:
            # 执行前置钩子
            await self._execute_hooks(flow_config.get("before_hooks", []))
            
            # 执行步骤
            steps = flow_config.get("steps", [])
            variables_ctx = variables or {}
            
            for step in steps:
                # 替换变量
                step = self._replace_variables(step, variables_ctx)
                
                # 执行步骤
                step_result = await self._execute_step(step, params or {})
                result.add_step_result(step_result)
                
                # 如果步骤失败且不是可选的，停止执行
                if not step_result.success and not step_result.optional:
                    result.mark_completed(success=False)
                    result.error = step_result.error
                    result.error_step = step_result.step_id
                    result.error_stack = step_result.action_result.error_stack if step_result.action_result else None
                    return result
                
                # 收集变量
                if step_result.action_result and step_result.action_result.data:
                    variables_ctx.update(step_result.action_result.data)
            
            # 执行后置钩子
            await self._execute_hooks(flow_config.get("after_hooks", []))
            
            # 标记完成
            result.mark_completed(success=True)
            
        except Exception as e:
            result.mark_completed(success=False)
            result.error = str(e)
            raise FlowExecutionException(flow_name, str(e))
        
        return result
    
    async def _load_flow(self, flow_name: str) -> Optional[Dict[str, Any]]:
        """加载流程配置文件"""
        flow_file = self.flows_dir / f"{flow_name}.json"
        
        if not flow_file.exists():
            return None
        
        with open(flow_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def _execute_step(
        self,
        step: Dict[str, Any],
        params: Dict[str, Any]
    ) -> StepResult:
        """执行单个步骤"""
        import time
        start_time = time.time()
        
        step_result = StepResult(
            success=False,
            step_id=step.get("step_id", 0),
            step_name=step.get("name", ""),
            description=step.get("description", ""),
            optional=step.get("optional", False)
        )
        
        try:
            # 检查条件
            if "condition" in step:
                condition_met = await self._evaluate_condition(step["condition"])
                if not condition_met:
                    step_result.skipped = True
                    step_result.skip_reason = "Condition not met"
                    step_result.success = True
                    return step_result
            
            # 创建操作执行器
            action_type = step.get("action")
            action_params = step.get("params", {})
            
            # 合并参数
            if "params_key" in step:
                key = step["params_key"]
                if key in params:
                    action_params.update(params[key])
            
            executor = ActionFactory.create(action_type, self.page, self.config)
            
            # 执行操作
            action_result = await executor.execute(action_params)
            
            step_result.action_result = action_result
            step_result.success = action_result.success
            
            # 添加截图
            if action_result.screenshot:
                step_result.add_screenshot(action_result.screenshot)
            
            # 等待
            wait_after = step.get("wait_after", self.config.performance.default_wait_after)
            if wait_after > 0:
                await asyncio.sleep(wait_after)
            
            step_result.duration = (time.time() - start_time) * 1000
            
        except Exception as e:
            step_result.error = str(e)
            step_result.duration = (time.time() - start_time) * 1000
        
        return step_result
    
    async def _execute_hooks(self, hooks: List[Dict[str, Any]]) -> None:
        """执行钩子"""
        for hook in hooks:
            try:
                action_type = hook.get("action")
                action_params = hook.get("params", {})
                
                executor = ActionFactory.create(action_type, self.page, self.config)
                await executor.execute(action_params)
            except Exception:
                # 钩子失败不影响主流程
                pass
    
    async def _evaluate_condition(self, condition: Dict[str, Any]) -> bool:
        """评估条件"""
        condition_type = condition.get("type")
        
        if condition_type == "element_exists":
            selector = condition.get("selector")
            element = self.page.locator(selector)
            count = await element.count()
            return count > 0
        
        elif condition_type == "element_visible":
            selector = condition.get("selector")
            element = self.page.locator(selector)
            return await element.is_visible()
        
        elif condition_type == "url_contains":
            text = condition.get("text")
            return text in self.page.url
        
        elif condition_type == "title_contains":
            text = condition.get("text")
            title = await self.page.title()
            return text in title
        
        elif condition_type == "javascript":
            script = condition.get("script")
            result = await self.page.evaluate(script)
            return bool(result)
        
        return True
    
    def _replace_variables(
        self,
        step: Dict[str, Any],
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """替换变量"""
        import copy
        import re
        
        step_str = json.dumps(step)
        
        # 替换 ${variable_name} 格式的变量
        for key, value in variables.items():
            step_str = step_str.replace(f"${{{key}}}", str(value))
        
        return json.loads(step_str)
