# test_cases/test_post_api.py
import allure
import pytest
from utils.request_utils import client
from utils.data_loader import load_yaml

# 加载复杂测试数据
POST_TEST_DATA = load_yaml("data/post_data.yaml")


@allure.epic("社区平台接口自动化")
@allure.feature("内容管理模块")
class TestPostApi:

    # 辅助方法：根据配置执行断言
    def _run_assertions(self, response, assertions):
        """
        遍历断言列表，并根据类型执行相应的校验。
        :param response: requests.Response 对象
        :param assertions: 从 YAML 加载的断言配置列表
        """
        response_json = response.json()  # 假设响应是 JSON
        for assertion in assertions:
            with allure.step(f"执行断言: {assertion['type']} on key '{assertion.get('key', 'N/A')}'"):
                assert_type = assertion["type"]

                if assert_type == "status_code":
                    assert response.status_code == assertion["value"], \
                        f"期望状态码 {assertion['value']}, 但实际是 {response.status_code}"

                elif assert_type == "json_key_exists":
                    key = assertion["key"]
                    assert key in response_json, \
                        f"响应 JSON 中缺少预期的键: '{key}'"

                elif assert_type == "json_value_equals":
                    key = assertion["key"]
                    expected_value = assertion["value"]
                    actual_value = response_json.get(key)
                    assert actual_value == expected_value, \
                        f"键 '{key}' 的值不匹配! 期望: '{expected_value}', 实际: '{actual_value}'"

                # 可以轻松扩展更多断言类型
                # elif assert_type == "json_contains":
                #   ...

    # 改造后的、数据驱动的复杂测试用例
    @allure.story("文章发布场景")
    @allure.title("创建文章: {test_data[test_case]}")  # 动态标题
    @pytest.mark.parametrize("test_data", POST_TEST_DATA['create_post'])
    def test_create_new_post(self, test_data):
        """
        这是一个数据驱动的复杂接口测试用例。
        它从 YAML 文件中读取请求数据、请求头、预期状态和多种断言规则，
        然后执行测试并验证所有规则。
        """
        payload = test_data["payload"]
        headers = test_data.get("headers", {})  # 使用 .get 提供默认值
        expected_status = test_data["expected_status"]
        assertions = test_data["assertions"]
        endpoint = "/posts"

        # 合并全局 headers 和用例特定的 headers
        request_headers = client.session.headers.copy()
        request_headers.update(headers)

        with allure.step(f"准备请求数据: {payload}"):
            pass

        with allure.step(f"发送 POST 请求到 {endpoint}，携带 Headers: {request_headers}"):
            response = client.send_request("POST", endpoint, json=payload, headers=request_headers)

        with allure.step(f"执行 {len(assertions)} 条断言规则..."):
            self._run_assertions(response, assertions)

    # ... (其他方法保持不变)
    @allure.story("文章查询场景")
    @allure.title("根据文章ID获取单篇文章")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_post(self):
        """验证通过有效的文章ID可以成功获取文章详情。"""
        post_id = 1
        endpoint = f"/posts/{post_id}"

        with allure.step(f"发送 GET 请求到 {endpoint}"):
            response = client.send_request("GET", endpoint)

        with allure.step("断言响应状态码为 200 OK"):
            assert response.status_code == 200

        post_data = response.json()
        with allure.step("断言返回的文章ID与请求的ID一致"):
            assert post_data["id"] == post_id

    @allure.story("文章更新场景")
    @allure.title("成功更新一篇文章的内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_post(self):
        """验证可以成功更新一篇已有文章的内容。"""
        post_id_to_update = 1
        updated_data = {
            "id": post_id_to_update,
            "title": "Updated Title for Post 1",
            "body": "The content has been modified.",
            "userId": 1
        }
        endpoint = f"/posts/{post_id_to_update}"

        with allure.step(f"发送 PUT 请求到 {endpoint}，更新文章内容"):
            response = client.send_request("PUT", endpoint, json=updated_data)

        with allure.step("断言响应状态码为 200 OK"):
            assert response.status_code == 200

        updated_post = response.json()
        with allure.step("断言返回的文章内容与更新的数据一致"):
            assert updated_post["title"] == updated_data["title"]
            assert updated_post["body"] == updated_data["body"]

    @allure.story("文章删除场景")
    @allure.title("成功删除一篇文章")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_post(self):
        """验证可以成功删除一篇文章。"""
        post_id_to_delete = 1
        endpoint = f"/posts/{post_id_to_delete}"

        with allure.step(f"发送 DELETE 请求到 {endpoint}"):
            response = client.send_request("DELETE", endpoint)

        with allure.step("断言响应状态码为 200 OK (或204 No Content)"):
            assert response.status_code == 200