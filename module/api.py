#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: D:\GitHub\rab_steam_packages\module\api.py
# @DATE: 2021/05/21 周五
# @TIME: 22:30:34
#
# @DESCRIPTION: Steam API 模块


import json
import requests


"""
@description: Steam 静态变量类
-------
@param:
-------
@return:
"""
class STEAM():

    """
    @description: 代理类
    -------
    @param:
    -------
    @return:
    """
    class PROXY():
        pass

    """
    @description: Steam URL 地址类
    -------
    @param:
    -------
    @return:
    """
    class URL():
        API = "https://api.steampowered.com"
        COMMUNITY = "https://steamcommunity.com"
        STORE = "https://store.steampowered.com"


"""
@description: Steam API 调用方法
-------
@param:
-------
@return:
"""
def call(request_method, interface, api_method, version, params=None):
    url = "/".join([STEAM.URL.API, interface, api_method, version])
    if (request_method.lower() == "get"):
        return requests.get(url, params=params)
    else:
        return requests.post(url, params=params)


"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    print(STEAM.URL.API)
