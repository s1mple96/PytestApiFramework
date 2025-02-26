import logging
from commons.assert_util import AssertUtil
from commons.extract_util import ExtractUtil
from commons.model_util import verify_yaml, CaseInfo
from commons.requests_util import RequestUtil
from commons.logs_util import logger



# 初始化工具类实例
extract_util = ExtractUtil()
request_util = RequestUtil()
assert_util = AssertUtil()

def stand_case_flow(case_obj: CaseInfo):
    """
    执行标准用例流程，包括日志记录、请求发送、变量提取和断言操作。

    :param case_obj: 用例信息对象，包含模块、接口、用例标题、请求信息、提取信息和断言信息等。
    """
    try:
        # 记录用例基本信息日志
        log_case_info(case_obj)

        # 校验 yaml 中的数据
        # 如果后续需要使用该功能，取消注释
        # case_obj = verify_yaml(case_obj)

        # 使用提取的值，把 {} 替换成具体的值
        new_request = extract_util.change(case_obj.request)

        # 发送请求
        response = send_request(new_request, request_util)
        if response is None:
            logger.error(f"请求 {case_obj.title} 失败，无法继续执行后续操作。")
            return None

        # 请求之后得到响应后去提取变量
        if case_obj.extract:
            extract_variables(response, case_obj.extract, extract_util)

        # 请求得到响应后，如果 validate 不为 None，则需要断言
        if case_obj.validate:
            perform_assertions(response, case_obj.validate, extract_util, assert_util)
        else:
            logger.info(f"用例 {case_obj.title} 未配置显式断言，将执行默认的 HTTP 状态码为 200 的断言检查。")
            # 检查 HTTP 响应状态码是否为 200
            if response.status_code == 200:
                logger.info(f"请求 {case_obj.title} 的 HTTP 响应状态码为 200，请求成功。")
            else:
                logger.error(f"请求 {case_obj.title} 的 HTTP 响应状态码为 {response.status_code}，请求失败。")

        return response

    except ValueError as e:
        logger.error(f"执行用例 {case_obj.title} 时发生值错误: {e}")
    except AttributeError as e:
        logger.error(f"执行用例 {case_obj.title} 时发生属性错误: {e}")
    except Exception as e:
        logger.error(f"执行用例 {case_obj.title} 时发生未知错误: {e}")
    return None

def log_case_info(case_obj: CaseInfo):
    """
    记录用例的基本信息，包括模块、接口和用例标题。

    :param case_obj: 用例信息对象
    """
    logger.info(
        f"模块: {case_obj.feature} | "
        f"接口: {case_obj.story} | "
        f"用例: {case_obj.title}"
    )

def send_request(new_request: dict, request_util: RequestUtil):
    """
    发送请求并记录响应信息。

    :param new_request: 处理后的请求信息
    :param request_util: 请求工具类实例
    :return: 请求响应对象
    """
    response = request_util.send_all_request(**new_request)
    return response

def extract_variables(response, extract_info: dict, extract_util: ExtractUtil):
    """
    从响应中提取变量。

    :param response: 请求响应对象
    :param extract_info: 提取信息字典
    :param extract_util: 提取工具类实例
    """
    for key, value in extract_info.items():
        extract_util.extract(response, key, *value)

def perform_assertions(response, validate_info: dict, extract_util: ExtractUtil, assert_util: AssertUtil):
    """
    执行断言操作。

    :param response: 请求响应对象
    :param validate_info: 断言信息字典
    :param extract_util: 提取工具类实例
    :param assert_util: 断言工具类实例
    """
    for assert_type, value in extract_util.change(validate_info).items():
        assert_util.assert_all_case(response, assert_type, value)