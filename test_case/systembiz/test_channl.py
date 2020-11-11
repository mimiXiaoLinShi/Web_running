# coding:utf8
from lib.parse_ymal import ParseYmal
from lib.pr_log import logger
import pytest


class TestChannal:

    def setup_class(self):
        self.yml = ParseYmal('systembiz/channel.yaml')
        self.group_name = 'channel_platform'
        self.api_belong = 'systembiz'

    def test_channal_platform_list(self, login_web):
        data = self.yml.get_special_data(self.group_name, 'channel_platform_list')
        logger.info(data)
        result = login_web.request_queue(data, self.api_belong)

    def test_channel_platform_all_list(self, login_web):
        """所有平台用例"""
        data = self.yml.get_special_data(self.group_name, "channel_platform_all_list")
        result = login_web.request_queue(data, self.api_belong)

    def test_add_channel_platform(self, login_web):
        """新增平台用例"""
        data = self.yml.get_special_data(self.group_name, "add_channel_platform")
        res = login_web.request_queue(data, self.api_belong)
        platform_id = {'id': res["data"]["id"]}
        del_data = self.yml.get_special_data(self.group_name, "delete_channel_platform")
        login_web.request_queue(del_data, self.api_belong, platform_id)


    def test_update_channel_platform(self, login_web):
        """编辑平台用例"""
        data = self.yml.get_special_data(self.group_name, "update_channel_platform")
        login_web.request_queue(data, self.api_belong)

