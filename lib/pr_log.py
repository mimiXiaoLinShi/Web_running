# encoding: utf-8
# @author: youxinxu
# @Software: PyCharm
# @file: pr_log.py
# @time: 2020/11/1 21:03

import logging
import sys
from common.globals import G
import time
import os


def get_log(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formattr = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(lineno)d:%(message)s')
    fh = logging.FileHandler(log_file, encoding='utf8')
    fh.setFormatter(formattr)
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formattr)
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


file = os.path.join(G.base_path, 'logs/{}.log'.format(time.strftime('%m_%d', time.localtime())))
print(file)
# noinspection PyStatementEffect


logger = get_log(file)

if __name__ == '__main__':
    logger.info('hell world')
