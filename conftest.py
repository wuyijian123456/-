import pytest
import requests


# import sys
# from pathlib import Path
# # 将项目根目录（PythonProject_test）加入 Python 路径
#
# sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(autouse=True,scope="session")
def func():
    print(f"测试开始执行")
    # def multiplication(x):
    #     return x * 2
    yield
    print("测试执行完成")


# session =  requests.session()
# session.request()

