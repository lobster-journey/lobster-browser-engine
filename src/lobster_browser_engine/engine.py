"""
Lobster Browser Engine - Core Engine
核心引擎实现

Copyright (c) 2026 🦞 龙虾巡游记工作室 (Lobster Journey Studio)
"""

import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from .config import EngineConfig
from .result import FlowResult, StepResult, ActionResult
from .enums import FlowStatus, ActionType
from .exceptions import (
    BrowserEngineException,
    ConnectionException,
    FlowNotFoundException,
    FlowExecutionException
)


class BrowserEngine:
    """
    浏览器引擎主类
    
    提供完整的浏览器自动化操作能力
    """
    
    def __init__(self, config: Optional[EngineConfig] = None):
        """
        初始化浏览器引擎
        
        Args:
            config: 引擎配置，不提供则使用默认配置
        """
        self.config = config or EngineConfig()
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._connected = False
        self._playwright = None
        
    async def connect(self) -> None:
        """
        连接到浏览器
        
        Raises:
            ConnectionException: 连接失败
        """
        try:
            self._playwright = await async_playwright().start()
            
            if self.config.connection.connection_type.value == "cdp":
                # CDP连接
                self._browser = await self._playwright.chromium.connect_over_cdp(
                    self.config.connection.cdp_url,
                    timeout=self.config.timeout.connection_timeout
                )
            else:
                # 启动新浏览器
                self._browser = await self._playwright.chromium.launch(
                    headless=self.config.connection.headless,
                    args=self.config.connection.args
                )
            
            # 创建上下文
            self._context = await self._browser.new_context(
                ignore_https_errors=self.config.connection.ignore_https_errors,
                accept_downloads=self.config.connection.accept_downloads
            )
            
            # 创建页面
            self._page = await self._context.new_page()
            
            self._connected = True
            
        except Exception as e:
            raise ConnectionException(f"Failed to connect to browser: {str(e)}")
    
    async def disconnect(self) -> None:
        """断开浏览器连接"""
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        
        self._connected = False
        self._browser = None
        self._context = None
        self._page = None
        self._playwright = None
    
    async def execute_flow(self, flow_name: str, params: Optional[Dict] = None) -> FlowResult:
        """
        执行预定义流程
        
        Args:
            flow_name: 流程名称
            params: 流程参数
            
        Returns:
            FlowResult: 流程执行结果
            
        Raises:
            FlowNotFoundException: 流程未找到
            FlowExecutionException: 流程执行失败
        """
        if not self._connected:
            raise ConnectionException("Browser not connected")
        
        # 加载流程配置
        flow_config = await self._load_flow(flow_name)
        if not flow_config:
            raise FlowNotFoundException(flow_name)
        
        # 执行流程
        result = await self._execute_flow_internal(flow_config, params or {})
        return result
    
    async def _load_flow(self, flow_name: str) -> Optional[Dict]:
        """加载流程配置"""
        flow_dir = Path(__file__).parent.parent.parent / "flows"
        flow_file = flow_dir / f"{flow_name}.json"
        
        if not flow_file.exists():
            return None
        
        import json
        with open(flow_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def _execute_flow_internal(self, flow_config: Dict, params: Dict) -> FlowResult:
        """内部执行流程"""
        result = FlowResult(
            success=False,
            flow_name=flow_config.get("name", "unknown"),
            flow_version=flow_config.get("version", "1.0.0"),
            status=FlowStatus.RUNNING,
            steps_total=len(flow_config.get("steps", [])),
            params=params
        )
        
        try:
            steps = flow_config.get("steps", [])
            for step in steps:
                step_result = await self._execute_step(step, params)
                result.add_step_result(step_result)
                
                if not step_result.success and not step_result.optional:
                    result.mark_completed(success=False)
                    result.error = step_result.error
                    result.error_step = step_result.step_id
                    return result
            
            result.mark_completed(success=True)
            
        except Exception as e:
            result.mark_completed(success=False)
            result.error = str(e)
        
        return result
    
    async def _execute_step(self, step: Dict, params: Dict) -> StepResult:
        """执行单个步骤"""
        from .actions.factory import ActionFactory
        
        step_result = StepResult(
            success=False,
            step_id=step.get("step_id", 0),
            step_name=step.get("name", ""),
            description=step.get("description", "")
        )
        
        try:
            action_type = step.get("action")
            action_params = step.get("params", {})
            
            # 创建操作执行器
            executor = ActionFactory.create(action_type, self._page, self.config)
            
            # 执行操作
            action_result = await executor.execute(action_params)
            
            step_result.action_result = action_result
            step_result.success = action_result.success
            
            if action_result.screenshot:
                step_result.add_screenshot(action_result.screenshot)
            
            # 等待
            wait_after = step.get("wait_after", self.config.performance.default_wait_after)
            if wait_after > 0:
                await asyncio.sleep(wait_after)
            
        except Exception as e:
            step_result.error = str(e)
        
        return step_result
    
    def get_page(self) -> Page:
        """获取当前页面对象"""
        if not self._page:
            raise ConnectionException("Browser not connected")
        return self._page
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.disconnect()
