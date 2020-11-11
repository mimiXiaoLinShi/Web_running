# coding: utf8
import pytest
import os

from common.globals import G
from lib.get_conf_data import ConfFile
from lib.parse_ymal import ParseYmal
from lib.web_request import FanWeb

@pytest.fixture(scope='session')
def login_web():
    '''
    登录环境， 判断是登录的哪个环境 switch: 1 表示online, 2表示pre, 3表示 test
    :return:
    '''
    environment_dict = {'1': 'online', '2': 'pre', '3': 'test'}
    header_value = {'1': 'RELEASE', '2': 'PRE', '3': 'TEST'}
    file_path = os.path.join(G.base_path, 'conf/setting.conf')
    login_path = os.path.join(G.base_path, 'data/login.yaml')
    env_type = 'api2'
    coon = ConfFile(file_path)
    base_url = coon.get_dict('HOST', env_type)
    env_int = coon.get_dict("ENVIROMENT", "SWITCH")
    # 获取环境类型:
    env = environment_dict[env_int]
    # 获取header参数
    env_x_stage = header_value[env_int]
    # 获取对应环境的登录用户名和密码
    login_yml = ParseYmal('login.yaml')
    result = login_yml.get_special_data('login', 'login')
    username = result['params'][env]['username']
    password = result['params'][env]['password']
    # 开始登录
    web_api = FanWeb(base_url, username, password, env_x_stage, env)
    web_api.login()
    yield web_api


if __name__ == '__main__':
    login_web()


