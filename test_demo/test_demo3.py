import pytest
from unittest.mock import Mock, patch
import time


# 模拟的 API 调用函数
def call_api(url, timeout, use_cache=False):
    """
    模拟 API 调用
    Args:
        url: API地址
        timeout: 超时时间
        use_cache: 是否使用缓存
    Returns:
        包含 status 和 data 的字典
    """
    # 模拟网络延迟
    time.sleep(0.01)  # 10ms 延迟

    # 模拟不同的响应
    if "localhost" in url:
        # 开发环境可能有更多调试信息
        return {
            "status": "success",
            "data": {"environment": "development", "debug": True},
            "metadata": {"response_time": timeout * 0.8}
        }
    elif "staging" in url:
        # 预发布环境
        return {
            "status": "success",
            "data": {"environment": "staging", "debug": False},
            "metadata": {"response_time": timeout * 0.9}
        }
    else:
        # 生产环境
        return {
            "status": "success",
            "data": {"environment": "production", "debug": False},
            "metadata": {"response_time": timeout * 0.95}
        }


# 缓存模拟
class Cache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value
        return True


# 带有缓存功能的 API 客户端
class APIClient:
    def __init__(self, cache_enabled=False):
        self.cache = Cache() if cache_enabled else None
        self.call_count = 0

    def make_request(self, url, timeout):
        """发送 API 请求，支持缓存"""
        self.call_count += 1

        # 如果启用缓存，先检查缓存
        if self.cache:
            cache_key = f"{url}_{timeout}"
            cached_response = self.cache.get(cache_key)
            if cached_response:
                cached_response["cached"] = True
                return cached_response

        # 实际调用 API
        response = call_api(url, timeout)

        # 如果启用缓存，存储结果
        if self.cache:
            cache_key = f"{url}_{timeout}"
            self.cache.set(cache_key, response)
            response["cached"] = False

        return response


# 测试配置 fixture
@pytest.fixture(params=["production", "staging", "development"])
def environment_config(request):
    """
    测试不同的环境配置
    参数化 fixture，会运行 3 次测试
    """
    configs = {
        "production": {
            "url": "https://api.company.com",
            "timeout": 10,
            "expected_env": "production"
        },
        "staging": {
            "url": "https://staging.company.com",
            "timeout": 20,
            "expected_env": "staging"
        },
        "development": {
            "url": "http://localhost:8000",
            "timeout": 30,
            "expected_env": "development"
        }
    }
    config = configs[request.param]
    config["name"] = request.param  # 添加环境名称
    return config


# 缓存配置 fixture
@pytest.fixture(params=[True, False])
def cache_enabled(request):
    """
    测试启用/禁用缓存
    参数化 fixture，会运行 2 次测试
    """
    return request.param


# API 客户端 fixture
@pytest.fixture
def api_client(cache_enabled):
    """
    创建 API 客户端实例
    依赖 cache_enabled fixture
    """
    return APIClient(cache_enabled=cache_enabled)


# 主测试函数
def test_api_performance(environment_config, cache_enabled, api_client):
    """
    测试在不同环境和缓存配置下的 API 性能
    这个测试会运行 3 × 2 = 6 次
    """
    print(f"\n测试环境: {environment_config['name']}, 缓存: {cache_enabled}")

    # 第一次调用
    response1 = api_client.make_request(
        url=environment_config["url"],
        timeout=environment_config["timeout"]
    )

    # 验证响应状态
    assert response1["status"] == "success"

    # 验证环境信息
    assert response1["data"]["environment"] == environment_config["expected_env"]

    # 验证调试模式
    if environment_config["name"] == "development":
        assert response1["data"]["debug"] is True
    else:
        assert response1["data"]["debug"] is False

    # 验证缓存标记
    if cache_enabled:
        # 第一次调用应该没有缓存
        assert response1.get("cached", False) is False
    else:
        # 禁用缓存时没有 cached 字段
        assert "cached" not in response1

    # 第二次调用（测试缓存效果）
    response2 = api_client.make_request(
        url=environment_config["url"],
        timeout=environment_config["timeout"]
    )

    if cache_enabled:
        # 启用缓存时，第二次调用应该命中缓存
        assert response2.get("cached", False) is True
        # 验证调用次数
        assert api_client.call_count == 1  # 应该只有第一次实际调用了 API
    else:
        # 禁用缓存时，应该调用了两次 API
        assert api_client.call_count == 2


# 额外的测试用例
def test_api_response_time(environment_config):
    """
    测试 API 响应时间是否符合预期
    """
    response = call_api(
        url=environment_config["url"],
        timeout=environment_config["timeout"],
        use_cache=False
    )

    # 验证响应时间
    response_time = response["metadata"]["response_time"]
    assert response_time <= environment_config["timeout"]

    # 验证响应时间比例
    timeout = environment_config["timeout"]
    if environment_config["name"] == "development":
        # 开发环境应该最快
        assert response_time <= timeout * 0.8
    elif environment_config["name"] == "staging":
        # 预发布环境中等
        assert response_time <= timeout * 0.9
    else:
        # 生产环境最慢但可靠
        assert response_time <= timeout * 0.95


# 模拟网络错误的测试
def test_api_with_network_error(environment_config, mocker):
    """
    测试 API 网络错误处理
    使用 mocker fixture 模拟异常
    """
    # 模拟网络超时
    mocker.patch('time.sleep', side_effect=Exception("Network timeout"))

    with pytest.raises(Exception) as exc_info:
        call_api(
            url=environment_config["url"],
            timeout=environment_config["timeout"]
        )

    assert "Network timeout" in str(exc_info.value)


# 测试缓存功能
def test_cache_functionality():
    """
    专门测试缓存功能
    """
    # 测试启用缓存
    client_with_cache = APIClient(cache_enabled=True)

    # 第一次调用
    response1 = client_with_cache.make_request("https://api.example.com", 10)
    assert response1.get("cached", False) is False
    assert client_with_cache.call_count == 1

    # 第二次调用应该命中缓存
    response2 = client_with_cache.make_request("https://api.example.com", 10)
    assert response2.get("cached", False) is True
    assert client_with_cache.call_count == 1  # 调用次数不变

    # 测试禁用缓存
    client_without_cache = APIClient(cache_enabled=False)

    response3 = client_without_cache.make_request("https://api.example.com", 10)
    assert "cached" not in response3
    assert client_without_cache.call_count == 1

    response4 = client_without_cache.make_request("https://api.example.com", 10)
    assert "cached" not in response4
    assert client_without_cache.call_count == 2  # 调用次数增加


# 测试参数组合
@pytest.mark.parametrize("url,timeout,expected", [
    ("https://api.example.com", 5, "success"),
    ("https://api.example.com", 0, "success"),  # 测试零超时
    ("https://api.example.com", 60, "success"),  # 测试长超时
])
def test_api_with_different_timeouts(url, timeout, expected):
    """
    测试不同超时时间的API调用
    """
    response = call_api(url=url, timeout=timeout)
    assert response["status"] == expected

    # 验证响应时间
    if timeout > 0:
        assert response["metadata"]["response_time"] <= timeout


# 运行测试
if __name__ == "__main__":
    # 手动运行测试
    import sys

    sys.exit(pytest.main([__file__, "-v", "-s"]))