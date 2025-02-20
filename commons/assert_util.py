import copy
import pymysql
from config import setting
from commons.logs_util import logger

class AssertUtil:
    def __init__(self):
        # 初始化数据库连接配置
        self.db_config = {
            'user': setting.db_username,
            'password': setting.db_password,
            'host': setting.db_host,
            'database': setting.db_database,
            'port': setting.db_port
        }

    def _connect_database(self):
        """
        建立数据库连接
        :return: 数据库连接对象
        """
        logger.info("尝试建立数据库连接")
        try:
            connection = pymysql.connect(**self.db_config)
            logger.info("数据库连接成功")
            return connection
        except pymysql.Error as e:
            error_msg = f"数据库连接失败: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def _execute_sql(self, sql):
        """
        执行 SQL 语句并返回查询结果
        :param sql: SQL 语句
        :return: 查询结果
        """
        logger.info(f"准备执行 SQL 语句: {sql}")
        with self._connect_database() as conn:
            with conn.cursor() as cs:
                try:
                    cs.execute(sql)
                    result = cs.fetchone()
                    logger.info(f"SQL 语句执行成功，查询结果: {result}")
                    return result
                except pymysql.Error as e:
                    error_msg = f"执行 SQL 语句失败: {sql}, 错误信息: {e}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

    def _get_response_value(self, res, sj):
        """
        根据属性名获取响应对象的属性值
        :param res: 响应对象
        :param sj: 属性名
        :return: 属性值
        """
        logger.info(f"尝试获取响应对象的 |{sj}| 属性值")
        try:
            value = getattr(res, sj)
            logger.info(f"成功获取响应对象的 |{sj}| 属性值: |{value}|")
            return value
        except AttributeError:
            logger.warning(f"响应对象没有 |{sj}| 属性，返回属性名本身")
            return sj

    def _perform_assertion(self, assert_type, yq, sj_value, msg):
        """
        执行断言操作
        :param assert_type: 断言类型
        :param yq: 预期值
        :param sj_value: 实际值
        :param msg: 断言失败时的提示信息
        """
        supported_assert_types = ["equals", "contains", "db_equals", "db_contains"]
        if assert_type not in supported_assert_types:
            error_msg = f"不支持的断言类型: {assert_type}，支持的类型有 {supported_assert_types}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"开始执行 {assert_type} 断言，预期值: {yq}，实际值: {sj_value}")
        if assert_type == "equals":
            try:
                assert yq == sj_value, msg
                logger.info(f"{msg} 断言成功，预期值: {yq}，实际值: {sj_value}")
            except AssertionError:
                error_msg = f"{msg} 断言失败，预期值：{yq}，实际值：{sj_value}"
                logger.error(error_msg)
                raise AssertionError(error_msg)
        elif assert_type == "contains":
            try:
                assert yq in sj_value, msg
                logger.info(f"{msg} 断言成功，预期值: {yq}，实际值: {sj_value}")
            except AssertionError:
                error_msg = f"{msg} 断言失败，预期值：{yq}，实际值：{sj_value}"
                logger.error(error_msg)
                raise AssertionError(error_msg)
        elif assert_type == "db_equals":
            yq_value = self._execute_sql(yq)
            try:
                assert yq_value[0] in sj_value, msg
                logger.info(f"{msg} 断言成功，数据库查询值: {yq_value[0]}，实际值: {sj_value}")
            except AssertionError:
                error_msg = f"{msg} 断言失败，数据库查询值：{yq_value[0]}，实际值：{sj_value}"
                logger.error(error_msg)
                raise AssertionError(error_msg)
        elif assert_type == "db_contains":
            yq_value = self._execute_sql(yq)
            try:
                assert yq_value[0] in sj_value, msg
                logger.info(f"{msg} 断言成功，数据库查询值: {yq_value[0]}，实际值: {sj_value}")
            except AssertionError:
                error_msg = f"{msg} 断言失败，数据库查询值：{yq_value[0]}，实际值：{sj_value}"
                logger.error(error_msg)
                raise AssertionError(error_msg)

    def assert_all_case(self, res, assert_type, value):
        """
        执行所有断言用例
        :param res: 响应对象
        :param assert_type: 断言类型
        :param value: 断言数据，包含预期值和实际值
        """
        logger.info(f"开始执行 {assert_type} 断言用例")
        new_res = copy.deepcopy(res)
        try:
            new_res.json = new_res.json()
            logger.info("成功将响应内容转换为 JSON 格式")
        except Exception:
            new_res.json = {"msg": 'response not json data'}
            error_msg = f"将响应内容转换为 JSON 格式时出错，当前已将响应 JSON 内容设为: |{new_res.json}|"
            logger.error(error_msg)
            raise Exception(error_msg)

        for msg, yq_and_sj_data in value.items():
            yq, sj = yq_and_sj_data[0], yq_and_sj_data[1]
            sj_value = self._get_response_value(new_res, sj)
            try:
                self._perform_assertion(assert_type, yq, sj_value, msg)
            except AssertionError as e:
                error_msg = f"{msg} 断言失败，预期值：|{yq}|，实际值：|{sj_value}|"
                logger.error(error_msg)
                raise AssertionError(error_msg)