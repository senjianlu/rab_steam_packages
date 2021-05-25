#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: /root/GitHub/rab_steam_packages/main/login.py
# @DATE: 2021/05/21 Fri
# @TIME: 15:37:58
#
# @DESCRIPTION: Steam 登录模块


import rsa
import time
import json
import base64
import requests
import sys
sys.path.append("..")
from modules.api import STEAM


"""
@description: 获取 RSA 参数
-------
@param:
-------
@return:
"""
def get_rsa_params_for_session_login(session, username):
    key_response = session.post(
        STEAM.URL.STORE+"/login/getrsakey/", data={"username": username})
    key_response = json.loads(key_response.text)
    rsa_mod = int(key_response["publickey_mod"], 16)
    rsa_exp = int(key_response["publickey_exp"], 16)
    rsa_timestamp = key_response["timestamp"]
    return {"rsa_key": rsa.PublicKey(rsa_mod, rsa_exp),
            "rsa_timestamp": rsa_timestamp}

"""
@description: 生成登录所需所有参数
-------
@param:
-------
@return:
"""
def get_params_for_session_login(username,
                                 encrypted_password,
                                 two_factor_code,
                                 rsa_timestamp) -> dict:
    params = {
        "password": encrypted_password,
        "username": username,
        "twofactorcode": two_factor_code,
        "emailauth": "",
        "loginfriendlyname": "",
        "captchagid": "-1",
        "captcha_text": "",
        "emailsteamid": "",
        "rsatimestamp": rsa_timestamp,
        "remember_login": "true",
        "donotcache": str(int(time.time()*1000))
    }
    return params

"""
@description: 使用 Session 的 Steam 登录
-------
@param:
-------
@return:
"""
def login_by_session(username, password, two_factor_code=None):
    # 主 Session
    login_session = requests.session()
    # 获取 RSA 公钥
    rsa_params = get_rsa_params_for_session_login(login_session, username)
    # 加密 Steam 密码
    encrypted_password = base64.b64encode(
        rsa.encrypt(password.encode("utf-8"), rsa_params["rsa_key"]))
    # 获取服务器端生成 RSA 公钥的时间戳
    rsa_timestamp = rsa_params['rsa_timestamp']
    # 登录所需参数
    params = get_params_for_session_login(
            username, encrypted_password, two_factor_code, rsa_timestamp)
    # 登录
    login_response = login_session.post(
        STEAM.URL.STORE+"/login/dologin", data=params)
    # 执行登录成功后的跳转
    transfer_parameters = json.loads(login_response.text)["transfer_parameters"]
    for transfer_url in json.loads(login_response.text)['transfer_urls']:
        login_session.post(transfer_url, transfer_parameters)
    return login_session


"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    pass