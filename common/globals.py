
# encoding: utf-8
# @author: youxinxu
# @file: globals.py
# @time: 2020/11/1 16:46
import os


class Globals:
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



G = Globals()
