import pytest


def func(x):
    return x + 1

def add(a,b):
    return a + b

def test_answer():
    assert func(3) == 5

@pytest.mark.parametrize("a, b, expected",[[1,2,3],[1,2,4],[2,3,4]])
def test_add(a, b, expected):
    assert add(a, b) == expected





def setup_function(function):
    """每个测试函数前执行"""
    print(f"\n>>> 开始执行测试函数: {function.__name__}")

def teardown_function(function):
    """每个测试函数后执行"""
    print(f"\n<<< 结束执行测试函数: {function.__name__}")



def setup_module(module):
    """整个测试模块执行前运行一次"""
    print("\n*** 开始执行测试模块 ***")
    print("模块初始化...")
    # 全局初始化操作

    module.global_config = {"env": "test", "debug": True}

def teardown_module(module):
    """整个测试模块执行后运行一次"""
    print("\n*** 结束执行测试模块 ***")
    print("模块清理...")
    # 全局清理操作
    module.global_config = {}


