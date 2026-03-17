# utils/request_utils.py
import requests
from utils.data_loader import *

class RequestClient:
    """封装 requests 库的客户端，统一处理 base_url, headers, timeout 等"""


    def __init__(self):
        Config = config.get('api')
        self.session = requests.Session()
        self.base_url = Config.get('base_url')
        self.timeout = Config.get('timeout')
        # 可以在这里设置全局 headers，如 Content-Type
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    def send_request(self, method, endpoint, **kwargs):
        """
        发送HTTP请求的核心方法
        :param method: 请求方法 (GET, POST, PUT, DELETE, PATCH)
        :param endpoint: API 端点 (例如 /posts)
        :param kwargs: 透传给 requests.request 的其他参数 (如 params, json, data)
        :return: requests.Response 对象
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            # 在实际项目中，这里应该有更完善的异常处理和日志记录
            print(f"请求发生错误: {e}")
            raise

# 创建一个全局的请求客户端实例，方便在测试用例中直接使用
client = RequestClient()