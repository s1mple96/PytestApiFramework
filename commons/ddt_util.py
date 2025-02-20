import yaml
from commons.logs_util import logger


# 读取测试用例
def read_testcase(yaml_path):
    """
    读取指定路径的 YAML 测试用例文件。
    若用例列表长度大于等于 2，将整个用例列表作为一个元素返回；
    若用例列表长度为 1 且包含 'parametrize' 字段，则进行数据驱动处理；
    否则直接返回用例列表。

    :param yaml_path: YAML 文件的路径
    :return: 处理后的测试用例列表
    """
    try:
        logger.info(f"开始读取 YAML 文件: {yaml_path}")
        with open(yaml_path, encoding='utf-8') as f:
            case_list = yaml.safe_load(f)
            if not isinstance(case_list, list):
                error_msg = f"YAML 文件内容不是有效的列表格式: {yaml_path}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            if len(case_list) >= 2:
                logger.info(f"YAML 文件中有多个用例，返回用例列表: {yaml_path}")
                return [case_list]
            elif len(case_list) == 1:
                case_dict = case_list[0]
                if "parametrize" in case_dict:
                    logger.info(f"YAML 文件中有数据驱动用例，进行数据驱动处理: {yaml_path}")
                    new_caseinfo = ddts(case_dict)
                    return new_caseinfo
                logger.info(f"YAML 文件中只有一个非数据驱动用例，返回该用例: {yaml_path}")
                return case_list
            logger.info(f"YAML 文件中用例列表为空，返回空列表: {yaml_path}")
            return case_list
    except FileNotFoundError:
        error_msg = f"未找到指定的 YAML 文件: {yaml_path}"
        logger.error(error_msg)
        return []
    except yaml.YAMLError as e:
        error_msg = f"解析 YAML 文件时出错: {e}"
        logger.error(error_msg)
        return []
    except Exception as e:
        error_msg = f"读取测试用例时出现未知错误: {e}"
        logger.error(error_msg)
        return []

def is_valid_parametrize(data_list):
    """
    检查 parametrize 字段是否有效
    :param data_list: parametrize 字段的数据列表
    :return: 有效返回 True，无效返回 False
    """
    if not data_list or not isinstance(data_list, list):
        return False
    name_len = len(data_list[0]) if data_list else 0
    for data in data_list:
        if len(data) != name_len:
            return False
    return True

def ddts(caseinfo: dict):
    """
    处理数据驱动用例，将参数化数据应用到测试用例中。

    :param caseinfo: 包含 'parametrize' 字段的测试用例字典
    :return: 处理后的测试用例列表
    """
    data_list = caseinfo.get("parametrize")
    if not is_valid_parametrize(data_list):
        error_msg = f"parametrize 字段不是有效的列表或参数长度不一致: {data_list}"
        logger.error(error_msg)
        return []

    str_caseinfo = yaml.dump(caseinfo)
    new_caseinfo = []
    for x in range(1, len(data_list)):
        raw_caseinfo = str_caseinfo
        for y in range(len(data_list[0])):
            param_value = data_list[x][y]
            if isinstance(param_value, str) and param_value.isdigit():
                param_value = f"'{param_value}'"
            raw_caseinfo = raw_caseinfo.replace(f"$ddt{{{data_list[0][y]}}}", str(param_value))
        case_dict = yaml.safe_load(raw_caseinfo)
        case_dict.pop("parametrize", None)
        new_caseinfo.append(case_dict)
    logger.info("数据驱动用例处理完成")
    return new_caseinfo