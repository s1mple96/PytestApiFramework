import logging
import requests
from config import setting

from commons.logs_util import logger


class RequestUtil:
    def __init__(self):
        # 创建一个会话对象，确保所有请求使用同一个会话
        self.session = requests.Session()

    def _update_params(self, kwargs):
        """
        更新请求参数，将全局参数追加到 params 中
        :param kwargs: 请求参数
        :return: 更新后的请求参数
        """
        params = kwargs.get("params", {})
        params.update(setting.global_args)
        kwargs["params"] = params
        logger.info(f"请求params: {params}")
        return kwargs

    def _open_files(self, kwargs):
        """
        打开文件，处理文件上传请求
        :param kwargs: 请求参数
        :return: 更新后的请求参数及文件对象列表
        """
        file_objects = []
        if "files" in kwargs:
            new_files = {}
            for file_key, file_value in kwargs["files"].items():
                try:
                    file_obj = open(file_value, "rb")
                    new_files[file_key] = file_obj
                    file_objects.append(file_obj)
                    logger.info(f"请求files - {file_key}: {file_value}")
                except Exception as e:
                    logger.error(f"文件路径有误! 错误信息: {e}")
                    # 关闭已打开的文件
                    for obj in file_objects:
                        obj.close()
                    return kwargs, []
            kwargs["files"] = new_files
        return kwargs, file_objects

    def _log_request_info(self, kwargs):
        """
        记录除 params 和 files 之外的其他请求信息
        :param kwargs: 请求参数
        """
        for key, value in kwargs.items():
            if key not in ["params", "files"]:
                logger.info(f"请求{key}: {value}")

    def _log_response_info(self, response):
        """
        记录响应信息，包括状态码、JSON 数据或文本数据
        :param response: 请求响应对象
        """
        logger.info(f"响应状态码: {response.status_code}")
        try:
            json_data = response.json()
            logger.info(f"JSON数据是{json_data}")
        except ValueError:
            logger.info(f"响应数据不是JSON格式，响应文本: {response.text}")

        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type.lower():
            try:
                logger.info(f"响应数据: {response.json()}")
            except ValueError:
                logger.info(f"响应数据不是有效的JSON格式，响应文本: {response.text}")
        else:
            logger.info(f"响应数据: {response.text}")

    def send_all_request(self, **kwargs):
        """
        发送所有类型的请求
        :param kwargs: 请求参数
        :return: 请求响应对象
        """
        # 更新请求参数
        kwargs = self._update_params(kwargs)
        # 打开文件
        kwargs, file_objects = self._open_files(kwargs)
        # 记录其他请求信息
        self._log_request_info(kwargs)

        try:
            # 发送请求
            response = self.session.request(**kwargs)
        except requests.RequestException as e:
            logger.error(f"请求发生错误: {e}")
            response = None
        finally:
            # 关闭文件
            for file in file_objects:
                try:
                    file.close()
                except Exception as e:
                    logger.error(f"关闭文件时发生错误: {e}")

        if response:
            # 记录响应信息
            self._log_response_info(response)

        return response