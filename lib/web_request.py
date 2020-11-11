# encoding: utf-8
# @author: youxinxu
# @file: web_request.py
# @time: 2020/11/1 16:34
import re

import requests
from lib.pr_log import logger
import json
from urllib.parse import urljoin
import time


class FanWeb:
    def __init__(self, base_url, username, password, env_type, env):
        '''
        :param login_url: 登录url
        :param api_belong:
        :param env_type: header值，表示要登录的环境header要传的值
        :param env [test, pre, online]
        '''
        self.token = None
        self.env_type = env_type
        self.base_url = base_url
        # self.api_gelong = api_belong
        self.username = username
        self.password = password
        self.env = env


    def login(self):
        self.headers = {
            "content-type": 'application/json; charset=UTF-8',
            'X-Ca-Stage': self.env_type,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        data = {'username':self.username, 'password': self.password}
        api_params = json.dumps(data)

        request_res = requests.request(method='Post', url=urljoin(self.base_url, 'systembiz/user/userLogin.do'), data=api_params, headers=self.headers)
        response = json.loads(request_res.text)
        if response['code'] != '200':
            assert False, 'login fail response is {}'.format(request_res.content)
        self.token = response['data']['token']
        self.headers['token'] = self.token
        logger.info('login success token is {}'.format(self.token))

    def __del__(self):
        time.sleep(2)
        url = urljoin(self.base_url, 'systembiz/user/loginOut.do')
        print(url)
        url = 'https://api2.91duobaoyu.com/systembiz/user/loginOut.do'
        datas = json.dumps({'token': self.token})
        print(self.headers)
        response = requests.request(method='POST', url=url, data=datas, headers=self.headers)

        logger.info('loginOut result {}'.format(str(response.content)))

    def _parse_params(self, params, replace={}):
        """处理请求参数
            如果参数中存在${token}，则将token替换该值
            如果参数中存在${time}，则将当前时间的时间戳替换该
            :param replace: 要替换的参数，如果空字典就不需要替换
        """
        if isinstance(params, dict):
            if self.env in params:
                params = params[self.env]
                if replace:
                    print('9999999999999', replace)
                    for key in replace.keys():
                        if key not in params:
                            assert False, 'params not key: {}'.format(key)
                        else:
                            params[key] = replace[key]
            else:
                if replace:
                    for key in replace.keys():
                        if key not in params:
                            assert False, 'params not key: {}'.format(key)
                        else:
                            params[key] = replace[key]






        if "[None" in str(params):
            res = json.dumps(params).replace("null", '')
            try:
                params = json.loads(res, encoding="utf-8")
            except json.JSONDecodeError:
                assert False, "参数结构有问题，请检查"
        if isinstance(params, dict):
            for key, item in params.items():
                if isinstance(item, str):
                    if "$" in str(item):
                        if key == 'token':
                            params[key] = self.token
                        else:
                            if "{time}" in str(item):
                                now_time = int(time.time())
                                params[key] = str(item).replace('${time}', str(now_time))
                elif isinstance(item, dict):
                    for i_key, i_value in item.items():
                        if "$" in str(i_value):
                            if params[key][i_key] == 'token':
                                params[key][i_key] = self.token
                            else:
                                if "{time}" in str(item):
                                    now_time = int(time.time())
                                    params[key][i_key] = str(item[i_key]).replace('${time}', str(now_time))
        elif isinstance(params, list):
            params = params
        return params


    def _parse_url(self, params_url, params):
        regex = re.compile(r'\{(\w+)\}')
        gre = regex.findall(params_url)
        if self.env in params:
            params = params[self.env]
        if gre:
            for plan in gre:
                if plan in params.keys():
                    params_url = params_url.replace('{%s}' % plan, str(params[plan]))
                else:
                    assert False
        return params_url



    def request_queue(self, data, api_begin, replace={}):
        url = data['url']

        method = data['method']
        params = data['params']
        if params:
            params = self._parse_params(params, replace)
        url = self._parse_url(url, params)
        return self.request_response(url, method, params, api_begin)


    def request_response(self, url, method, params, api_begin):
        urls = self.base_url + '/' + api_begin + url
        if isinstance(params, dict) or isinstance(params, list):
            if method.upper() == "GET":
                api_params = params
                logger.info('Get api_params is {}'.format(api_params))
            elif method.upper() == "POST":
                api_params = json.dumps(params)
                logger.info('POST api_params is {}'.format(api_params))
        elif params is None:
            api_params = dict()
        if method.upper() == "POST":
            response = requests.request(method.upper(), url=urls, data=api_params, headers=self.headers)
            content = json.loads(response.content)
            logger.info('\f\n url is :{} method is :{} \r\n data is {} \r\n hearders is {} \r\n  response content is {}'.format(urls,method, api_params, self.headers, content))
            return content

        if method.upper() == 'GET':
            response = requests.request(method.upper(), url=urls, params=api_params)
            content = json.loads(response.content)
            logger.info('\f\n url is :{} method is :{} \r\n data is {} \r\n hearders is {} \r\n  response content is {}'.format(urls,method, api_params, self.headers, content))
            return content






if __name__ == '__main__':
    api_belong = 'aaaa'
    api_belong = 'systembiz'
    if api_belong in ["seo", "newmediabiz","sembiz"]:
        api = 'https://api.91duobaoyu.com'
    else:
        api='https://api2.91duobaoyu.com'
    url = 'https://api2.91duobaoyu.com'
    web = FanWeb(url, 'FS888888', 123456789, 'TEST')
    # web.login()

    url = 'baidu/come?sig={sain}&ligin={abc}'
    data = {'sain':'test1', 'abc':'test2'}
    datas = {'url':url, 'params': data, 'method':'aaa'}
    web.request_queue(datas, data)