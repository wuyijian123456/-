import pytest
import requests


@pytest.fixture(autouse=True,scope="session")
def func():
    print(f"测试开始执行")
    # def multiplication(x):
    #     return x * 2
    yield
    print("测试执行完成")


# session =  requests.session()
# session.request()

