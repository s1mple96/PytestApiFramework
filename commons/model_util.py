from dataclasses import dataclass
from typing import Optional
from commons.logs_util import logger

@dataclass
class CaseInfo:
    # 必填
    feature: str
    story: str
    title: str
    request: dict
    validate: dict = None
    # 选填
    extract: Optional[dict] = None
    parametrize: Optional[list] = None

def validate_extract(extract, yaml_name):
    """
    校验 extract 字段
    """
    if extract:
        for key, value in extract.items():
            if not isinstance(value, list) or len(value) != 3:
                error_msg = f"{yaml_name}.yaml测试用例不符合框架的规范！'extract' 字段中 '{key}' 的值必须是包含 3 个元素的列表。"
                logger.error(error_msg)
                raise ValueError(error_msg)

def validate_validate(validate, yaml_name):
    """
    校验 validate 字段
    """
    if validate:
        valid_assert_types = ['equals', 'contains', 'db_equals', 'db_contains']
        for assert_type, values in validate.items():
            if assert_type not in valid_assert_types:
                error_msg = f"{yaml_name}.yaml测试用例不符合框架的规范！'validate' 字段中的断言类型 '{assert_type}' 必须是 {valid_assert_types} 之一。"
                logger.error(error_msg)
                raise ValueError(error_msg)
            for msg, expected_and_actual in values.items():
                if not isinstance(expected_and_actual, list) or len(expected_and_actual) != 2:
                    error_msg = f"{yaml_name}.yaml测试用例不符合框架的规范！'validate' 字段中 '{assert_type}' 下 '{msg}' 的值必须是包含 2 个元素的列表。"
                    logger.error(error_msg)
                    raise ValueError(error_msg)

def verify_yaml(caseinfo: dict, yaml_name):
    try:
        new_caseinfo = CaseInfo(**caseinfo)
        # 校验 extract 字段
        validate_extract(new_caseinfo.extract, yaml_name)
        # 校验 validate 字段
        validate_validate(new_caseinfo.validate, yaml_name)
        return new_caseinfo
    except ValueError as e:
        # 处理校验失败的异常
        logger.error(f"{yaml_name}.yaml测试用例不符合框架的规范！详细信息: {str(e)}")
        raise Exception(f"{yaml_name}.yaml测试用例不符合框架的规范！详细信息: {str(e)}")
    except TypeError as e:
        # 处理解包字典时的异常
        logger.error(f"{yaml_name}.yaml测试用例不符合框架的规范！缺少必要字段或字段类型错误。详细信息: {str(e)}")
        raise Exception(f"{yaml_name}.yaml测试用例不符合框架的规范！缺少必要字段或字段类型错误。详细信息: {str(e)}")
    except Exception as e:
        # 处理其他未知异常
        logger.error(f"{yaml_name}.yaml测试用例校验时发生未知错误。详细信息: {str(e)}")
        raise Exception(f"{yaml_name}.yaml测试用例校验时发生未知错误。详细信息: {str(e)}")