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
from bs4 import BeautifulSoup
from modules import api


"""
@description: Steam 确认交易类
-------
@param:
-------
@return:
"""
class r_steam_guard_confirmation():
    
    """
    @description: 初始化
    -------
    @param:
    -------
    @return:
    """
    def __init__(self, id, data_confid, data_key):
        self._id = id
        self._data_confid = data_confid
        self._data_key = data_key


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
        # Steam ID
        self._steam_id = steam_id
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
    
    """
    @description: 生成交易确认码
    -------
    @param:
    -------
    @return:
    """
    def generate_confirmation_key(self, tag) -> bytes:
        buffer = struct.pack(">Q", int(time.time())) + tag.encode("ascii")
        confirmation_key = base64.b64encode(
            hmac.new(base64.b64decode(self._identity_secret),
                     buffer,
                     digestmod=sha1).digest())
        return confirmation_key

    """
    @description: 生成设备 ID
    -------
    @param:
    -------
    @return:
    """
    def generate_device_id(self) -> str:
        hexed_steam_id = sha1(self._steam_id.encode("ascii")).hexdigest()
        return "android:" + "-".join([hexed_steam_id[:8],
                                      hexed_steam_id[8:12],
                                      hexed_steam_id[12:16],
                                      hexed_steam_id[16:20],
                                      hexed_steam_id[20:32]])
    
    """
    @description: 生成访问交易确认页面所需的参数
    -------
    @param:
    -------
    @return:
    """
    def generate_params(self, tag):
        params = {
            "p": self.generate_device_id(),
            "a": self._steam_id,
            "k": self.generate_confirmation_key(tag),
            "t": int(time.time()),
            "m": "android",
            "tag": tag
        }
        return params

    """
    @description: 获取所有待确认交易
    -------
    @param:
    -------
    @return:
    """
    def get_confirmations(self, logined_session, tag):
        # 待确认交易类列表
        confirmations = []
        # 访问该页面所需的对象
        params = generate_params(tag)
        headers = {
            "X-Requested-With": "com.valvesoftware.android.steam.community"
        }
        # 访问
        response = logined_session.get(
            api.STEAM.URL.COMMUNITY+"/mobileconf/conf", params=params, headers=headers)
        # 判断
        if (response.status_code != 200):
            pass
        else:
            error_key_word = "Steam Guard Mobile Authenticator is " \
                             + "providing incorrect Steam Guard codes."
            if (error_key_word in response.text):
                pass
            # 成功访问待确认交易列表页面
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                # 无待确认交易
                if (soup.select('#mobileconf_empty')):
                    pass
                # 有待确认交易
                else:
                    # 循环并将交易信息生成对象放入列表
                    for confirmation_div in soup.select(
                            "#mobileconf_list .mobileconf_list_entry"):
                        confirmations.append(
                            r_steam_guard_confirmation(
                                confirmation_div['id'],
                                confirmation_div['data-confid'],
                                confirmation_div['data-key']))
        return confirmations

    """
    @description: 获取待确认交易具体信息
    -------
    @param:
    -------
    @return:
    """
    def get_confirmation_info(self, logined_session, confirmation):
        tag = "details" + confirmation._id
        params = generate_params(tag)
        response = logined_session.get(
            api.STEAM.URL.COMMUNITY+"/details/"+confirmation._id, params=params)
        return json.loads(response)["html"]

    """
    @description: 通过待确认交易
    -------
    @param:
    -------
    @return:
    """
    def allow_confirmation(self, logined_session, confirmation):
        tag = "allow"
        params = self.generate_params(tag)
        params["op"] = tag
        params["cid"] = confirmation._data_confid
        params["ck"] = confirmation._data_key
        headers = {"X-Requested-With": "XMLHttpRequest"}
        response = logined_session.get(
            api.STEAM.URL.COMMUNITY+"/ajaxop", params=params, headers=headers)
        return json.loads(response)
    
    """
    @description: 取消待确认交易
    -------
    @param:
    -------
    @return:
    """
    def cancel_confirmation(self, logined_session, confirmation):
        tag = "cancel"
        params = self.generate_params(tag)
        params["op"] = tag
        params["cid"] = confirmation._data_confid
        params["ck"] = confirmation._data_key
        headers = {"X-Requested-With": "XMLHttpRequest"}
        response = logined_session.get(
            api.STEAM.URL.COMMUNITY+"/ajaxop", params=params, headers=headers)
        return json.loads(response)

