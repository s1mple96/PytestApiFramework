import copy
import re
import jsonpath
import yaml
from colorama import Fore

from commons.yaml_util import write_yaml, read_all
from hotload.debug_talk import DebugTalk

from commons.logs_util import logger

class ExtractUtil:
    """
    专门用来接口关联的类，负责解析提取变量和替换变量值。
    """
    def extract(self, res, var_name, attr_name, expr: str, index):
        """
        从请求返回结果中提取数据并更新到 YAML 文件。

        :param res: 请求返回的结果
        :param var_name: yaml 中的 key，例如: csrf_token
        :param attr_name: 请求返回结果中提取数据的属性名，例如: json, text
        :param expr: 提取数据的表达式，例如: jsonpath 表达式或者正则表达式
        :param index: 提取数据的下标
        """
        try:
            # 深拷贝 res 内容到 new_res 对象
            new_res = copy.deepcopy(res)
            # 处理 JSON 数据
            if hasattr(new_res, 'json'):
                try:
                    new_res.json = new_res.json()
                except (AttributeError, ValueError) as e:
                    self._log_error(f"响应数据不是有效的 JSON 格式: {e}")
                    return

            # 通过反射获取属性的值
            data = self._get_attribute(new_res, attr_name)
            if data is None:
                return

            # 判断提取方式并提取数据
            lis = self._extract_data(data, expr)

            # 通过下标取值并更新 YAML 文件
            if lis and 0 <= index < len(lis):
                self._update_yaml(var_name, lis[index])
            else:
                self._log_error("提取数据失败，可能是提取结果为空或下标越界 \n")

        except Exception as e:
            self._log_error(f"提取数据时发生未知错误: {e}")

    def _get_attribute(self, obj, attr_name):
        """
        通过反射获取对象的属性值。

        :param obj: 对象
        :param attr_name: 属性名
        :return: 属性值，如果属性不存在则返回 None
        """
        try:
            data = getattr(obj, attr_name)
            self._log_info(f"获取到的 {attr_name} 数据是--------> {data}")
            return data
        except AttributeError as e:
            self._log_error(f"对象没有 {attr_name} 属性: {e}")
            return None

    def _extract_data(self, data, expr):
        """
        根据表达式类型（jsonpath 或正则表达式）提取数据。

        :param data: 提取的对象
        :param expr: 提取的表达式
        :return: 提取的数据列表
        """
        try:
            if expr.startswith("$"):
                lis = jsonpath.jsonpath(dict(data), expr)
                self._log_info(f"以 jsonpath 来提取数据: {lis}")
            else:
                lis = re.findall(expr, str(data))
                self._log_info(f"使用正则表达式来提取数据: {lis}")
            return lis or []
        except Exception as e:
            self._log_error(f"使用 {expr.startswith('$') and 'jsonpath' or '正则表达式'} 提取数据时出错: {e}")
            return []

    def _update_yaml(self, var_name, value):
        """
        更新 YAML 文件中的变量值。

        :param var_name: 变量名
        :param value: 变量值
        """
        try:
            write_yaml({var_name: value})
            self._log_info(f"成功更新 YAML 文件，{var_name} 的值为: {value}")
        except Exception as e:
            self._log_error(f"更新 YAML 文件时出错: {e}")

    def change(self, request_data: dict):
        """
        解析使用变量，把 ${access_token} 替换从 extract.yaml 里面提取的具体的值。

        :param request_data: 请求数据字典
        :return: 替换后的请求数据字典
        """
        # 1. 把字典转为字符串
        data_str = yaml.safe_dump(request_data)
        # 2. 字符串替换
        new_request_dat = self.hotload_replace(data_str)
        # 3. 把字符串还原成字典
        data_dict = yaml.safe_load(new_request_dat)
        return data_dict

    def hotload_replace(self, data_str: str):
        """
        热加载方法，替换字符串中的函数调用表达式。

        :param data_str: 待替换的字符串
        :return: 替换后的字符串
        """
        # 定义正则表达式匹配函数调用表达式
        regexp = r"\$\{(.*?)\((.*?)\)\}"
        # 通过正则表达式在 data_str 字符串中匹配，得到所有的表达式列表
        fun_list = re.findall(regexp, data_str)

        for f in fun_list:
            try:
                if f[1] == "":  # 没有参数
                    new_value = getattr(DebugTalk(), f[0])()
                else:  # 有参数, 1 - N 个参数
                    new_value = getattr(DebugTalk(), f[0])(*f[1].split(","))

                # 如果 value 是一个数字格式的字符串
                if isinstance(new_value, str) and new_value.isdigit():
                    new_value = f"'{new_value}'"

                # 拼接旧的值
                old_value = f"${{{f[0]}({f[1]})}}"
                # 把旧的表达式替换成函数返回的新的值
                data_str = data_str.replace(old_value, str(new_value))
            except Exception as e:
                self._log_error(f"热加载替换时调用 {f[0]} 函数出错: {e}")

        return data_str

    def _log_info(self, message):
        """
        记录信息日志。

        :param message: 日志信息
        """
        # print(f"{Fore.GREEN}{message}{Fore.RESET}")

    def _log_error(self, message):
        """
        记录错误日志。

        :param message: 日志信息
        """
        print(f"{Fore.RED}{message}{Fore.RESET}")