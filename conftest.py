import pytest
import logging
import requests
from commons.yaml_util import clean_yaml
from commons.logs_util import logger

# 企业微信机器人的 Webhook 地址
WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ea5dc04e-f36c-487e-bdd3-8c7051b38a3e"

# 测试报告的访问地址，需要根据实际情况修改
ALLURE_REPORT_URL = "https://github.com/s1mple96/PytestAPIFramework"


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    捕获每个测试用例的执行报告
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, "report", report)


def pytest_sessionfinish(session, exitstatus):
    """
    在整个测试会话结束时，通过企业微信机器人发送测试结果和 Allure 报告链接
    :param session: pytest 会话对象
    :param exitstatus: 测试会话的退出状态
    """
    try:
        # 获取测试结果统计信息
        total = 0
        passed = 0
        failed = 0
        skipped = 0

        for item in session.items:
            total += 1
            if hasattr(item, "report"):
                if item.report.outcome == 'passed':
                    passed += 1
                elif item.report.outcome == 'failed':
                    failed += 1
                elif item.report.outcome == 'skipped':
                    skipped += 1

        # 构造企业微信消息
        message = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": "Allure 测试报告",
                        "description": f"本次测试已完成，共执行 {total} 条用例，其中成功 {passed} 条，失败 {failed} 条，跳过 {skipped} 条。",
                        "url": ALLURE_REPORT_URL,
                        "picurl": f"https://avatars.githubusercontent.com/u/51851184?v=4"
                    }
                ]
            }
        }

        # 发送请求到企业微信机器人的 Webhook 地址
        response = requests.post(WECOM_WEBHOOK, json=message)
        response.raise_for_status()
        logger.info("成功发送 Allure 报告链接及测试结果到企业微信。")
    except requests.RequestException as e:
        logger.error(f"发送 Allure 报告链接及测试结果到企业微信时出现错误: {e}")
    except Exception as e:
        logger.error(f"未知错误: {e}")
