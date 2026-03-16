import pytest
import json
import allure
from typing import Dict, Any

# 参数化 Fixture
@pytest.fixture(params=["chrome", "firefox", "edge"])
def browser(request):
    """测试不同浏览器"""
    # 获取测试函数名称
    test_name = request.function.__name__
    print(f"当前运行的测试函数: {test_name}")
    browser_name = request.param
    print(f"\n启动浏览器: {browser_name}")
    yield browser_name
    print(f"关闭浏览器: {browser_name}")

@allure.epic("测试")
@pytest.mark.ddt
def test_1(browser):
    print(f"正在测试浏览器：{browser}")
    assert browser in ["chrome", "firefox", "edge"]

