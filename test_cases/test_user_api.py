# test_cases/test_user_api.py
import allure
import pytest
from utils.request_utils import client
from utils.data_loader import load_yaml  # 1. 导入新的数据加载函数

# 2. 在类外部加载测试数据
# 这行代码会在测试收集阶段执行一次，加载数据供后续使用
USER_TEST_DATA = load_yaml("data/user_data.yaml")


@allure.epic("社区平台接口自动化")
@allure.feature("用户管理模块")
class TestUserApi:

    # 3. 使用 @pytest.mark.parametrize 进行数据驱动
    # 参数化会将 `USER_TEST_DATA['get_single_user']` 列表里的每一个字典，
    # 解包后作为 `test_data` 参数传入 `test_get_single_user` 方法。

    @allure.story("用户信息查询场景")
    @allure.title("根据用户ID获取单个用户信息: {test_data[test_case]}") # 4. 动态设置标题
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("test_data", USER_TEST_DATA['get_single_user'])
    def test_get_single_user(self, test_data): # 5. 接收参数化的数据
        """
        这是一个数据驱动的测试用例。
        它将使用 YAML 文件中定义的多个用户ID来执行相同的测试逻辑，
        验证系统对不同ID的响应是否正确。
        """
        user_id = test_data["user_id"]
        expected_status = test_data["expected_status"]
        check_fields = test_data["check_fields"]
        endpoint = f"/users/{user_id}"

        with allure.step(f"发送 GET 请求到 /users/{user_id}"):
            response = client.send_request("GET", endpoint)

        with allure.step(f"断言响应状态码为 {expected_status}"):
            assert response.status_code == expected_status

        # 只有当 YAML 数据中指明需要检查时，才执行字段断言
        if check_fields:
            response_data = response.json()
            with allure.step("断言响应数据包含预期的字段"):
                assert "name" in response_data
                assert "email" in response_data

    # ... (其他方法保持不变)
    @allure.story("用户信息查询场景")
    @allure.title("查询不存在的用户ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_non_existent_user(self):
        """验证当查询一个不存在的用户ID时，系统返回 404 Not Found。"""
        non_existent_id = 9999
        endpoint = f"/users/{non_existent_id}"

        with allure.step(f"发送 GET 请求到 /users/{non_existent_id}"):
            response = client.send_request("GET", endpoint)

        with allure.step("断言响应状态码为 404 Not Found"):
            assert response.status_code == 404

    @allure.story("用户数据检索场景")
    @allure.title("获取所有用户的列表")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_all_users(self):
        """验证可以成功获取系统中所有用户的列表。"""
        endpoint = "/users"

        with allure.step("发送 GET 请求到 /users"):
            response = client.send_request("GET", endpoint)

        with allure.step("断言响应状态码为 200 OK"):
            assert response.status_code == 200

        users = response.json()
        with allure.step("断言返回的用户列表不为空"):
            assert len(users) > 0