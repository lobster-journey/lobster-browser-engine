"""
浏览器操作引擎核心模块
Browser Engine Core Module

版本: v0.1.0
作者: 龙虾智能体
创建时间: 2026-04-19
"""

import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page, Browser, BrowserContext


@dataclass
class StepResult:
    """单个步骤执行结果"""
    success: bool
    action: str
    data: Any = None
    screenshot: Optional[str] = None
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class FlowResult:
    """流程执行结果"""
    success: bool
    flow_name: str
    steps_executed: int = 0
    steps_total: int = 0
    screenshots: List[str] = field(default_factory=list)
    data: Dict = field(default_factory=dict)
    error: Optional[str] = None
    duration: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class BrowserEngine:
    """
    浏览器操作引擎
    
    提供可靠的浏览器自动化操作能力
    """
    
    def __init__(
        self,
        cdp_url: str = "http://127.0.0.1:9222",
        headless: bool = False,
        timeout: int = 30000,
        retry_times: int = 3,
        screenshot_dir: str = "/tmp/browser_screenshots"
    ):
        """
        初始化浏览器引擎
        
        Args:
            cdp_url: CDP连接地址
            headless: 是否无头模式
            timeout: 默认超时时间（毫秒）
            retry_times: 失败重试次数
            screenshot_dir: 截图保存目录
        """
        self.cdp_url = cdp_url
        self.headless = headless
        self.timeout = timeout
        self.retry_times = retry_times
        self.screenshot_dir = screenshot_dir
        
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # 创建截图目录
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
        
        # 流程配置目录
        self.flows_dir = Path(__file__).parent.parent / "flows"
    
    async def connect(self) -> None:
        """连接到浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.connect_over_cdp(self.cdp_url)
        self.context = self.browser.contexts[0]
        self.page = self.context.pages[0]
    
    async def disconnect(self) -> None:
        """断开浏览器连接"""
        if self.browser:
            await self.browser.close()
    
    def get_page(self) -> Page:
        """获取当前页面对象"""
        return self.page
    
    async def execute_flow(
        self,
        flow_name: str,
        params: Optional[Dict] = None
    ) -> FlowResult:
        """
        执行预定义的流程
        
        Args:
            flow_name: 流程名称
            params: 流程参数
            
        Returns:
            FlowResult: 流程执行结果
        """
        # 加载流程配置
        flow_path = self.flows_dir / f"{flow_name}.json"
        if not flow_path.exists():
            return FlowResult(
                success=False,
                flow_name=flow_name,
                error=f"流程配置文件不存在: {flow_path}"
            )
        
        with open(flow_path, 'r', encoding='utf-8') as f:
            flow = json.load(f)
        
        return await self._execute_flow_internal(flow, params)
    
    async def execute_custom_flow(
        self,
        flow: Dict,
        params: Optional[Dict] = None
    ) -> FlowResult:
        """
        执行自定义流程
        
        Args:
            flow: 流程配置
            params: 流程参数
            
        Returns:
            FlowResult: 流程执行结果
        """
        return await self._execute_flow_internal(flow, params)
    
    async def _execute_flow_internal(
        self,
        flow: Dict,
        params: Optional[Dict] = None
    ) -> FlowResult:
        """内部流程执行逻辑"""
        start_time = datetime.now()
        
        result = FlowResult(
            success=True,
            flow_name=flow.get('name', 'unknown'),
            steps_total=len(flow.get('steps', []))
        )
        
        try:
            # 确保已连接
            if not self.page:
                await self.connect()
            
            # 执行每个步骤
            for step in flow.get('steps', []):
                step_result = await self._execute_step(step, params)
                result.steps_executed += 1
                
                if not step_result.success:
                    result.success = False
                    result.error = f"步骤 {step.get('description', step.get('action'))} 失败: {step_result.error}"
                    break
                
                # 保存截图
                if step_result.screenshot:
                    result.screenshots.append(step_result.screenshot)
            
            # 成功后的操作
            if result.success and 'on_success' in flow:
                await self._execute_step(flow['on_success'], params)
        
        except Exception as e:
            result.success = False
            result.error = str(e)
        
        # 失败后的操作
        if not result.success and 'on_failure' in flow:
            await self._execute_step(flow['on_failure'], params)
        
        result.duration = (datetime.now() - start_time).total_seconds()
        return result
    
    async def _execute_step(
        self,
        step: Dict,
        params: Optional[Dict] = None
    ) -> StepResult:
        """执行单个步骤"""
        action = step.get('action')
        start_time = datetime.now()
        
        try:
            # 替换参数占位符
            step_resolved = self._resolve_params(step, params)
            
            # 根据action类型执行对应操作
            if action == 'navigate':
                await self.page.goto(
                    step_resolved['url'],
                    wait_until=step_resolved.get('wait_until', 'networkidle')
                )
            
            elif action == 'click':
                locator = self._create_locator(step_resolved['locator'])
                await locator.click(timeout=step_resolved.get('timeout', 5000))
                await asyncio.sleep(step_resolved.get('wait_after', 0))
            
            elif action == 'fill':
                locator = self._create_locator(step_resolved['locator'])
                if step_resolved.get('clear_first', True):
                    await locator.clear()
                await locator.fill(step_resolved['value'])
                await asyncio.sleep(step_resolved.get('wait_after', 0))
            
            elif action == 'wait':
                if 'time' in step_resolved:
                    await asyncio.sleep(step_resolved['time'])
                elif 'locator' in step_resolved:
                    locator = self._create_locator(step_resolved['locator'])
                    await locator.wait_for(timeout=step_resolved.get('timeout', 10000))
                elif 'url' in step_resolved:
                    await self.page.wait_for_url(
                        step_resolved['url'],
                        timeout=step_resolved.get('timeout', 10000)
                    )
            
            elif action == 'screenshot':
                screenshot_path = step_resolved.get(
                    'path',
                    f"{self.screenshot_dir}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                await self.page.screenshot(
                    path=screenshot_path,
                    full_page=step_resolved.get('full_page', False)
                )
                return StepResult(
                    success=True,
                    action=action,
                    screenshot=screenshot_path
                )
            
            elif action == 'evaluate':
                script = step_resolved['script']
                data = await self.page.evaluate(script)
                await asyncio.sleep(step_resolved.get('wait_after', 0))
                return StepResult(
                    success=True,
                    action=action,
                    data=data
                )
            
            elif action == 'press':
                await self.page.keyboard.press(step_resolved['key'])
                await asyncio.sleep(step_resolved.get('wait_after', 0))
            
            elif action == 'refresh':
                await self.page.reload(wait_until=step_resolved.get('wait_until', 'networkidle'))
            
            else:
                return StepResult(
                    success=False,
                    action=action,
                    error=f"未知操作类型: {action}"
                )
            
            return StepResult(
                success=True,
                action=action,
                duration=(datetime.now() - start_time).total_seconds()
            )
        
        except Exception as e:
            return StepResult(
                success=False,
                action=action,
                error=str(e),
                duration=(datetime.now() - start_time).total_seconds()
            )
    
    def _create_locator(self, locator_str: str):
        """创建定位器"""
        # 解析定位器格式: strategy=value
        if '=' in locator_str:
            strategy, value = locator_str.split('=', 1)
        else:
            strategy = 'css'
            value = locator_str
        
        if strategy == 'text':
            return self.page.locator(f'text={value}')
        elif strategy == 'css':
            return self.page.locator(value)
        elif strategy == 'xpath':
            return self.page.locator(f'xpath={value}')
        elif strategy == 'role':
            return self.page.get_by_role(value)
        else:
            return self.page.locator(value)
    
    def _resolve_params(self, step: Dict, params: Optional[Dict]) -> Dict:
        """解析参数占位符"""
        if not params:
            return step
        
        import copy
        step_resolved = copy.deepcopy(step)
        
        # 递归替换 {{params.xxx}} 占位符
        def replace_placeholders(obj):
            if isinstance(obj, str):
                if obj.startswith('{{params.') and obj.endswith('}}'):
                    key = obj[10:-2]  # 提取参数名
                    return params.get(key, obj)
                return obj
            elif isinstance(obj, dict):
                return {k: replace_placeholders(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_placeholders(item) for item in obj]
            return obj
        
        return replace_placeholders(step_resolved)


# 便捷函数
async def execute_jimeng_login(cdp_url: str = "http://127.0.0.1:9222") -> FlowResult:
    """
    执行即梦登录流程
    
    Args:
        cdp_url: CDP连接地址
        
    Returns:
        FlowResult: 执行结果
    """
    engine = BrowserEngine(cdp_url=cdp_url)
    return await engine.execute_flow("jimeng_login")


if __name__ == "__main__":
    # 测试代码
    async def test():
        result = await execute_jimeng_login()
        print(f"登录结果: {result.success}")
        print(f"截图数量: {len(result.screenshots)}")
        if not result.success:
            print(f"错误: {result.error}")
    
    asyncio.run(test())
