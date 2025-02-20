import random
import time
import hashlib
import yaml
from commons.base_url import read_ini
from faker import Faker
from config import setting
from commons.logs_util import logger

class DebugTalk:
    def __init__(self):
        # 初始化 Faker 实例
        self.fake = Faker('zh_CN')

    def read_yaml(self, key):
        """
        读取 YAML 文件中指定键的值。

        :param key: 要读取的键
        :return: 指定键的值，如果键不存在或出现错误则返回 None
        """
        # logger.info(f"调用 read_yaml 方法，参数 key: {key}")
        try:
            with open(setting.extract_name, encoding="utf-8") as f:
                value = yaml.safe_load(f)
                if value and key in value:
                    # logger.info(f"read_yaml 方法成功获取键 {key} 的值: {value[key]}")
                    return value[key]
                else:
                    logger.warning(f"未找到键 '{key}' 或 YAML 文件为空。")
        except FileNotFoundError:
            logger.error(f"未找到 YAML 文件: {setting.extract_name}")
        except yaml.YAMLError as e:
            logger.error(f"解析 YAML 文件时出现错误: {e}")
        logger.info(f"read_yaml 方法返回值: None")
        return None

    def env(self, key):
        """
        从 INI 配置文件中获取指定键的值。

        :param key: 要获取的键
        :return: 指定键的值，如果键不存在或出现错误则返回 None
        """
        # logger.info(f"调用 env 方法，参数 key: {key}")
        try:
            ini_config = read_ini()
            if key in ini_config:
                # logger.info(f"env 方法成功获取键 {key} 的值: {ini_config[key]}")
                return ini_config[key]
            else:
                logger.warning(f"未找到键 '{key}' 在 INI 配置文件中。")
        except Exception as e:
            logger.error(f"读取 INI 配置文件时出现错误: {e}")
        # logger.info(f"env 方法返回值: None")
        return None

    def add(self, a, b):
        """
        对两个数进行相加操作。

        :param a: 第一个数
        :param b: 第二个数
        :return: 两数之和
        """
        logger.info(f"调用 add 方法，参数 a: {a}, b: {b}")
        try:
            result = int(a) + int(b)
            # logger.info(f"add 方法返回值: {result}")
            return result
        except ValueError:
            logger.error(f"无法将 '{a}' 和 '{b}' 转换为整数。")
        # logger.info(f"add 方法返回值: None")
        return None

    def md5(self, data):
        """
        对输入的数据进行 MD5 加密。

        :param data: 要加密的数据
        :return: 加密后的 MD5 字符串
        """
        # logger.info(f"调用 md5 方法，参数 data: {data}")
        try:
            data_str = str(data).encode('utf-8')
            result = hashlib.md5(data_str).hexdigest()
            # logger.info(f"md5 方法返回值: {result}")
            return result
        except Exception as e:
            logger.error(f"MD5 加密时出现错误: {e}")
        # logger.info(f"md5 方法返回值: None")
        return None

    def get_random_nmber(self):
        """
        生成一个基于当前时间戳的随机数字字符串。

        :return: 随机数字字符串
        """
        # logger.info("调用 get_random_nmber 方法")
        result = str(int(time.time()))
        # logger.info(f"get_random_nmber 方法返回值: {result}")
        return result

    def random_str_name(self, length=3):
        """
        生成随机中文名字。

        :param length: 名字的长度，默认为 3
        :return: 随机中文名字
        """
        # logger.info(f"调用 random_str_name 方法，参数 length: {length}")
        if length <= 0:
            logger.warning("名字长度必须大于 0。")
            # logger.info(f"random_str_name 方法返回值: ''")
            return ""
        # 中文字符的 Unicode 范围
        chinese_char_range = (0x4E00, 0x9FFF)
        name = ''.join(chr(random.randint(*chinese_char_range)) for _ in range(length))
        # logger.info(f"random_str_name 方法返回值: {name}")
        return name

    def random_name(self):
        """
        使用 Faker 库生成随机姓名。

        :return: 随机姓名
        """
        # logger.info("调用 random_name 方法")
        result = self.fake.name()
        # logger.info(f"random_name 方法返回值: {result}")
        return result

    def random_mobile(self):
        """
        使用 Faker 库生成随机手机号码。

        :return: 随机手机号码
        """
        # logger.info("调用 random_mobile 方法")
        result = self.fake.phone_number()
        # logger.info(f"random_mobile 方法返回值: {result}")
        return result