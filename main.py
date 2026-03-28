# main.py
import pytest
import sys

if __name__ == "__main__":
    # 可以加一些自定义逻辑
    sys.exit(pytest.main([
        "tests/",
        "--alluredir=allure-results",
        "-v"
    ]))