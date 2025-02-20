import yaml
import logging
from config import setting
from commons.logs_util import logger

def _open_yaml_file(mode):
    """
    内部方法，用于打开 extract.yaml 文件。
    :param mode: 文件打开模式
    :return: 文件对象
    """
    try:
        return open(setting.extract_name, encoding='utf-8', mode=mode)
    except FileNotFoundError:
        logging.error(f"未找到 extract.yaml 文件: {setting.extract_name}")
        return None
    except Exception as e:
        logging.error(f"打开 extract.yaml 文件时出现错误: {e}")
        return None

def read_yaml(key):
    """
    读取 extract.yaml 文件中指定键的值。
    :param key: 要读取的键
    :return: 指定键的值，如果键不存在或出现错误则返回 None
    """
    with _open_yaml_file('r') as f:
        if f:
            try:
                value = yaml.safe_load(f)
                if value and key in value:
                    return value[key]
                else:
                    logging.warning(f"未找到键 '{key}' 或 extract.yaml 文件为空。")
            except yaml.YAMLError as e:
                logging.error(f"解析 extract.yaml 文件时出现错误: {e}")
    return None

def read_all():
    """
    读取 extract.yaml 文件中的所有值。
    :return: extract.yaml 文件中的所有值，如果出现错误则返回 None
    """
    with _open_yaml_file('r') as f:
        if f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error(f"解析 extract.yaml 文件时出现错误: {e}")
    return None

def write_yaml(data):
    """
    将数据写入 extract.yaml 文件。
    :param data: 要写入的数据
    """
    with _open_yaml_file('a') as f:
        if f:
            try:
                yaml.safe_dump(data, f, allow_unicode=True)
                logging.info(f"成功将数据写入 extract.yaml 文件: {data}")
            except yaml.YAMLError as e:
                logging.error(f"写入 extract.yaml 文件时出现错误: {e}")

def clean_yaml():
    """
    清空 extract.yaml 文件的内容。
    """
    with _open_yaml_file('w') as f:
        pass