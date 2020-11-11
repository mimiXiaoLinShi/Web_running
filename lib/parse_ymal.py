# encoding: utf-8
# @author: youxinxu
# @Software: PyCharm
# @file: parse_ymal.py
# @time: 2020/11/2 23:02
import json
from common.globals import G
from lib.pr_log import logger
import yaml
import os

class ParseYmal:
    def __init__(self, file_path):
        self.file_name = os.path.join(G.base_path, os.path.join('data', file_path))

    def get_all_data(self):
        '读取文件内容'
        with open(self.file_name, 'r', encoding='utf8') as file:
            content = file.read()

        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

    def _get_all_group_data(self):
        '''获取所有接口分组数据'''
        data_group = self.get_all_data()
        if 'urls' in data_group:
            return data_group['urls']
        else:
            logger.error('urls is null：{} failed'.format(self.file_name))
            return False

    def _get_group_data(self, groups):
        data = self._get_all_group_data()

        if not data:
            return False
        for gr in data:
            if groups in gr.keys():
                logger.info('url_group is {}'.format(gr))
                return gr[groups]
        else:
            logger.error('{} not {}'.format(data, groups))
            return False


    def get_special_data(self, group, keyword):
        """获取指定key的数据"""

        group_url_data = self._get_group_data(group)

        if group_url_data:
            for request_set in group_url_data:

                if keyword == request_set['keyword']:
                    res = request_set
                    logger.info(res)
                    return res

            else:
                assert False, 'file {} nog {}'.format(self.file_name, keyword)
        else:
            assert False, '{} file failed'.format(self.file_name)




if __name__ == '__main__':
    yml = ParseYmal('systembiz/channel.yaml')
    result = yml.get_special_data('channel_platform', 'channel_platform_list')
    print(result)