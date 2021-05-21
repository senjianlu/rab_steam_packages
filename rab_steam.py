#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: /root/GitHub/rab_steam_packages/rab_steam.py
# @DATE: 2021/05/21 Fri
# @TIME: 15:04:17
#
# @DESCRIPTION: rab_steam_packages 主对象类



"""
@description: r_steam 类
-------
@param:
-------
@return:
"""
class r_steam():

    """
    @description: 初始化
    -------
    @param:
    -------
    @return:
    """
    def __init__(self, steam_id, username, password,
                    api_key=None, session=None driver=None):
        # Steam 64 位 ID
        self._steam_id = steam_id
        # Steam 用户名
        self._username = username
        # Steam 密码
        self._password = password
        # Steam 开发者 API KEY
        self._api_key = api_key
        # Steam 登录后 Session
        self._session = session
        # Steam 登录用 Selenium Driver
        self._driver = driver
