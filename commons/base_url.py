import logging
from iniconfig import IniConfig
from commons.logs_util import logger

def read_ini(config_file_path="./pytest.ini"):
    """
    读取 INI 配置文件中的 `base_url` 部分。

    :param config_file_path: 配置文件的路径，默认为 "./pytest.ini"
    :return: 如果 `base_url` 部分存在，返回其配置项的字典；否则返回空字典
    """
    try:
        # 尝试读取配置文件
        ini = IniConfig(config_file_path)
        # 检查配置文件中是否存在 base_url 部分
        if "base_url" in ini:
            # 若存在，将 base_url 部分的配置项转换为字典并返回
            base_url_config = dict(ini["base_url"].items())
            # logging.info(f"成功读取到 base_url 配置: {base_url_config}")
            return base_url_config
        else:
            # 若不存在，记录信息并返回空字典
            logging.info("配置文件中未找到 base_url 部分，返回空字典。")
            return {}
    except FileNotFoundError:
        # 处理文件未找到的异常，记录错误信息并返回空字典
        logging.error(f"未找到配置文件: {config_file_path}，请检查文件路径。")
        return {}
    except Exception as e:
        # 处理其他异常，记录错误信息并返回空字典
        logging.error(f"读取配置文件时出现未知错误: {e}")
        return {}