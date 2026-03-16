# test_sample.py
import pytest
import requests


@pytest.mark.parametrize("c,b",[[1,2],[2,4],[3,6]])
def test_answer(func,c,b):
    assert func(c) == b


class TestTwo:
    def test_001(self):
        assert 3==3
    def test_002(self):
        pass