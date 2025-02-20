
"""
循环获取所有的yaml文件(一个yaml生成一个用例，然后把用例放到TestAllCase类下面)

"""
from pathlib import Path

import allure
import pytest

from commons.ddt_util import read_testcase
from commons.extract_util import ExtractUtil
from commons.main_util import stand_case_flow
from commons.model_util import verify_yaml
from config import setting
from commons.logs_util import logger


#初始化这个模板对象
eu = ExtractUtil()


@allure.epic(setting.allure_project_name)
class TestAllCase:
    pass

"""
目的:传进来用例文件路径，创建一个函数去读取yaml文件内容,返回这个函数的地址引用
yaml_path:用例文件路径
read_testcase(yaml_path):读取yaml用例的值，并且返回来给到caseinfo变量
caseinfo: 将yaml中的测试用例，放到字典中进行返回
*value:解包之后相当于json,"$.access_token",0,分别传给extract后三个变量

"""
def create_testcase(yaml_path):
    @pytest.mark.parametrize("caseinfo", read_testcase(yaml_path))
    def func(self,caseinfo):
        global case_obj
        if isinstance(caseinfo,list):
            for case in caseinfo: #流程用例
                # 校验yaml中的数据
                case_obj = verify_yaml(case,yaml_path.stem)
                # 用例标准化流程
                stand_case_flow(case_obj)
        else: #单接口用例
            # 校验yaml中的数据
            case_obj = verify_yaml(caseinfo,yaml_path.stem)
            # 用例标准化流程
            stand_case_flow(case_obj)
        # 定制Al1ure报告
        allure.dynamic.feature(case_obj.feature)
        allure.dynamic.story(case_obj.story)
        allure.dynamic.title(case_obj.title)

    return func

"""
目的:循环获取所有的yaml文件(一个yaml生成一个用例，然后把用例放到类下面)
setattr参数说明：
    第一个:要将生成的 函数放到哪一个类下面
    第二个：给这个文件重新命名，以防不符合规范
    第三个：执行的函数
执行步骤：
    1.先预加载create_testcase函数但是不执行
    2.执行下面的代码，将生成的函数，加入到TestAllCase 下面
    3.再执行加入到TestAllCase下面的函数
    4.当使用 pytest 运行测试时，pytest 会自动发现 TestAllCase 类中的所有测试方法(以test_开头的)，
        并依次执行每个测试用例，同时生成 Allure 测试报告。

"""
#获得testcases的路径
testcase_path = Path(__file__).parent
#读取所有的testcases文件夹下面的所有yaml文件,存到列表[list]中
# yaml_case_list = testcase_path.glob("**/*.yaml")
#解决yaml从上到下执行问题
yaml_case_list = list(testcase_path.glob("**/8kwq2.yaml"))#**/phpwind.yaml
yaml_case_list.sort()
for yaml_path in yaml_case_list:
    # print("yaml_path:",yaml_path)
    # 打印用例的纯名字，例如A.yaml, 打印A
    # print("yaml_path.stem:",yaml_path.stem)
    # 通过反射，这个循环每循环一个那么就生成一个函数，然后把这个函数加入到TestAllCase 下面
    setattr(TestAllCase, "test_" + yaml_path.stem, create_testcase(yaml_path))


"""
执行流程:
    1.先预加载create_testcase函数但是不执行
    2.执行下面的代码，将生成的函数，加入到TestAllCase 下面
    3.再执行加入到TestAllCase下面的函数
    
"""