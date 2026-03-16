# config.py
# 统一管理测试环境和基础URL

class Config:
    # 我们使用 jsonplaceholder 作为演示的测试环境
    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT = 10  # 请求超时时间（秒）