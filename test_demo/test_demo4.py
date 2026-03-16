# import pytest
#
# # 定义 Fixture
# @pytest.fixture
# def database_connection():
#     # 前置条件
#     connection = create_connection()
#     yield connection  # 返回给测试用例
#     # 后置清理
#     connection.close()
#
# # 使用 Fixture
# def test_query(database_connection):  # 注入 Fixture
#     result = database_connection.query("SELECT 1")
#     assert result == 1

import pytest
import time


# 不同作用域的 Fixture
@pytest.fixture(scope="function")  # 默认：每个测试函数运行一次
def function_scope():
    print("函数级别 Fixture 执行")
    yield
    print("函数级别 Fixture 清理")


@pytest.fixture(scope="class")  # 每个测试类运行一次
def class_scope():
    print("类级别 Fixture 执行")
    yield
    print("类级别 Fixture 清理")


@pytest.fixture(scope="module")  # 每个模块运行一次
def module_scope():
    print("模块级别 Fixture 执行")
    yield
    print("模块级别 Fixture 清理")


@pytest.fixture(scope="session")  # 整个测试会话运行一次
def session_scope():
    print("会话级别 Fixture 执行")
    yield
    print("会话级别 Fixture 清理")


@pytest.fixture(scope="package")  # 每个包运行一次
def package_scope():
    print("包级别 Fixture 执行")
    yield
    print("包级别 Fixture 清理")


# 使用示例
class TestScope:
    def test_one(self, function_scope, class_scope, module_scope, session_scope):
        pass

    def test_two(self, function_scope, class_scope, module_scope, session_scope):
        pass

class TestScope2:
    def test_one_1(self, function_scope, class_scope, module_scope, session_scope):
        pass

    def test_two_1(self, function_scope, class_scope, module_scope, session_scope):
        pass

def test_funtionscope(function_scope):
    pass