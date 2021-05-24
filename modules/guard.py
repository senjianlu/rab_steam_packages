#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: /root/GitHub/rab_steam_packages/main/guard.py
# @DATE: 2021/05/21 Fri
# @TIME: 15:40:02
#
# @DESCRIPTION: Steam 令牌模块（包含登录令牌获取和出售/报价确认）


import os
import sys
sys.path.append("..")
import json
import time
import hmac
import base64
import struct
from hashlib import sha1


"""
@description: 从 .maFile 文件中读取指定字段
-------
@param:
-------
@return:
"""
def get_value_from_mafile(steam_id, key):
    mafile_path = "maFiles/" + steam_id + ".maFile"
    # 判断 maFiles 文件夹中是否有对应的令牌文件
    if (os.path.isfile(mafile_path)):
        with open(mafile_path, "r") as mafile:
            return json.loads(mafile.read())[key]
    else:
        raise Exception(
            "没有找到 Steam 令牌文件！需要文件名：{}.maFile".format(steam_id))


"""
@description: Steam Gurad 令牌类
-------
@param:
-------
@return:
"""
class r_steam_guard():

    """
    @description: 初始化
    -------
    @param:
    -------
    @return:
    """
    def __init__(self, steam_id):
        # shared_secret Steam 账户令牌公钥
        self._shared_secret = get_value_from_mafile(
            steam_id, "shared_secret")
        # identity_secret Steam 账户私钥
        self._identity_secret = get_value_from_mafile(
            steam_id, "identity_secret")
    
    """
    @description: 获取一次性令牌码
    -------
    @param:
    -------
    @return:
    """
    def get_two_factor_code(self):
        timestamp = int(time.time())
        # 将时间戳以 Big-Endian, UIit64 类型存放内存 (pack as Big-Endian, UInt64)
        time_buffer = struct.pack(">Q", timestamp//30)
        time_hmac = hmac.new(base64.b64decode(self._shared_secret),
                             time_buffer,
                             digestmod=sha1).digest()
        begin = ord(time_hmac[19:20]) & 0xf
        # 以 UInt32 类型从内存中取出 (unpack as Big-Endian UInt32)
        full_code = struct.unpack(
            ">I", time_hmac[begin:begin+4])[0] & 0x7fffffff
        chars = "23456789BCDFGHJKMNPQRTVWXY"
        two_factor_code = ""
        # 拼凑令牌码
        for _ in range(5):
            full_code, i = divmod(full_code, len(chars))
            two_factor_code += chars[i]
        return two_factor_code