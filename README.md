# 接口自动化测试项目

## 项目简介
本项目是一个基于 `pytest` 框架开发的接口自动化测试项目，旨在实现对接口的自动化测试，提高测试效率和准确性。项目支持从 YAML 文件中读取测试用例，使用数据驱动的方式执行测试，同时具备请求发送、变量提取、断言操作和详细的日志记录功能。

## 项目结构
```
api_frame/
├── testcases/ # 存放测试用例的 YAML 文件
│ ├── flow_test  #流程测试用例文件夹
│ ├── single_test #单接口测试用例文件
│ └── ddt_test    #数据驱动测试用例文件夹
├── commons/ # 通用工具类和方法
│ ├── assert_util.py # 断言工具类
│ ├── extract_util.py # 变量提取工具类
│ ├── requests_util.py # 请求发送工具类
│ ├── yaml_util.py # YAML 文件处理工具类
│ ├── ddt_util.py # 数据驱动处理模块
│ └── main_util.py # 用例执行流程模块
├── config/ # 配置文件目录
│ └── setting.py # 配置信息，如数据库连接配置、接口地址等
├── reports/ # 测试报告生成目录
├── conftest.py # pytest 配置文件，定义 fixture 和钩子函数
├── run.py # 项目入口文件，用于运行 pytest 测试
└── pytest.ini # pytest 配置文件
```

## 环境要求
- **Python 版本**：Python 3.7 及以上
- **依赖库**：在项目根目录下的 `requirements.txt` 文件中列出了所有依赖库，可使用以下命令进行安装：
    ```pip install -r requirements.txt```

### 配置说明

在 config/setting.py 文件中配置项目所需的信息，例如：
```
数据库连接配置
db_username = 'your_username'
db_password = 'your_password'
db_host = 'your_host'
db_database = 'your_database'
db_port = 3306
```
接口地址等其他配置
```
api_base_url = 'https://www.example.com'
```

## 使用方法
### 编写测试用例
在 testcases 目录下创建或修改 YAML 格式的测试用例文件，示例如下：
```
- name: 我要咨询接口测试
  request:
    method: POST
    url: /ajax.php?mod=online_order&code=submit
    params:
      application: app
      application_client_type: h5
    headers:
      Accept: application/json
      Content-Type: application/x-www-form-urlencoded
      Host: www.8kqw.com
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36
    data:
      mobile: '13606926898'
      name: 孔建军
      response: json
      source: bkq_pc_loan
      source_url: https://www.8kqw.com/
      submit: sign_bkqw_pc_loan
  validate:
    - equals:
        - 200
        - status_code`
```
        
### 运行测试
在项目根目录下执行以下命令运行测试：
```python run.py```
或者直接使用 pytest 命令：
```pytest```

### 查看测试报告
测试完成后，测试报告将生成在 reports 目录下，可通过浏览器打开查看详细的测试结果。

## 功能特性
### 数据驱动测试
支持从 YAML 文件中读取参数化数据，实现数据驱动的测试用例执行。在 YAML 文件中使用 parametrize 字段定义参数化数据，示例如下：
```
- name: 数据驱动测试示例
  parametrize:
    - [mobile, name]
    - ['13606926898', '孔建军']
    - ['15765001954', '张燕']
  request:
    method: POST
    url: /ajax.php?mod=online_order&code=submit
    params:
      application: app
      application_client_type: h5
    headers:
      Accept: application/json
      Content-Type: application/x-www-form-urlencoded
      Host: www.8kqw.com
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36
    data:
      mobile: $ddt{mobile}
      name: $ddt{name}
      response: json
      source: bkq_pc_loan
      source_url: https://www.8kqw.com/
      submit: sign_bkqw_pc_loan
  validate:
    - equals:
        - 200
        - status_code
```

### 变量提取与使用
支持从请求响应中提取变量，并在后续的测试用例中使用。在 YAML 文件中使用 extract 字段定义要提取的变量，示例如下：
```
- name: 变量提取测试示例
  request:
    method: POST
    url: /ajax.php?mod=online_order&code=submit
    params:
      application: app
      application_client_type: h5
    headers:
      Accept: application/json
      Content-Type: application/x-www-form-urlencoded
      Host: www.8kqw.com
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36
    data:
      mobile: '13606926898'
      name: 孔建军
      response: json
      source: bkq_pc_loan
      source_url: https://www.8kqw.com/
      submit: sign_bkqw_pc_loan
  extract:
    - msg: $.msg
  validate:
    - equals:
        - 200
        - status_code
```

### 多种断言类型
支持多种断言类型，包括 equals（相等断言）、contains（包含断言）、db_equals（数据库查询结果相等断言）、db_contains（数据库查询结果包含断言）等，示例如下：
```
- name: 断言测试示例
  request:
    method: POST
    url: /ajax.php?mod=online_order&code=submit
    params:
      application: app
      application_client_type: h5
    headers:
      Accept: application/json
      Content-Type: application/x-www-form-urlencoded
      Host: www.8kqw.com
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36
    data:
      mobile: '13606926898'
      name: 孔建军
      response: json
      source: bkq_pc_loan
      source_url: https://www.8kqw.com/
      submit: sign_bkqw_pc_loan
  validate:
    - equals:
        - 200
        - status_code
    - contains:
        - 申请成功
        - msg
```
### 注意事项
* 确保数据库连接配置正确，否则数据库相关的断言操作可能会失败。
* 在编写 YAML 测试用例文件时，注意数据格式的正确性，避免出现语法错误。
* 测试用例的执行顺序可能会影响测试结果，特别是涉及到变量提取和使用的用例，需要注意用例之间的依赖关系。
