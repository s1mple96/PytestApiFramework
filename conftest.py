import pytest
import logging
from commons.yaml_util import clean_yaml
from commons.logs_util import logger

@pytest.fixture(scope="session", autouse=True)
def clean_extract():
    """
    作为 pytest 的固件，在整个测试会话开始前自动执行，用于清空 extract.yaml 文件。
    此固件的作用范围是整个测试会话，并且会自动使用。

    在执行清空操作时，会捕获可能出现的异常，并记录相应的日志信息。
    如果清空操作成功，会记录成功信息；如果出现异常，会记录错误信息。
    """
    try:
        clean_yaml()
        logging.info("成功清空 extract.yaml 文件。")
    except Exception as e:
        logging.error(f"清空 extract.yaml 文件时出现错误: {e}")


def pytest_runtest_teardown(item, nextitem):
    """
    在每个测试用例执行完毕后添加日志
    :param item: 当前执行完毕的测试用例对象
    :param nextitem: 下一个要执行的测试用例对象，如果没有则为 None
    """
    # 记录测试用例执行结束的日志
    logger.info(f"测试用例 {item.name} 执行完毕\n")