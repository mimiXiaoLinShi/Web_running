
# encoding: utf-8
# @author: youxinxu

# @file: get_conf_data.py
# @time: 2020/11/1 16:50
import configparser
from common.globals import G
import os



class ConfFile:
    '''
    读取conf文件
    '''
    def __init__(self, file):
        self.cf = configparser.ConfigParser()
        self.cf.read(file)

    def get_section(self):
        return self.cf.sections()

    def get_options(self, sec):
        options = self.cf.options(sec)
        return options


    def get_items(self, item):
        '''
        返回对应值的列表
        :param item:
        :return:
        '''
        item = self.cf.items(item)
        print(item)
        return item


    def get_dict(self, key, value):
        '''

        :param key: 获取键
        :param value: 获取值
        :return:
        '''
        data = self.cf.get(key, value)
        return data

if __name__ == '__main__':
    file_path = os.path.join(G.base_path, 'conf/setting.conf')
    coon = ConfFile(file_path)
    print(coon.get_section())
    print(coon.get_options('HOST'))
    coon.get_items('HOST')
    coon.get_dict("ENVIROMENT", "SWITCH")

