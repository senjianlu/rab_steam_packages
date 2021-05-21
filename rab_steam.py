#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: /root/GitHub/rab_steam_packages/rab_steam.py
# @DATE: 2021/05/21 Fri
# @TIME: 15:04:17
#
# @DESCRIPTION: rab_steam_packages 主对象类


import configparser
from modules import chat
from modules import guard


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
                    api_key=None, session=None, driver=None):
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
        # Steam Chat 聊天类
        self.chat = None
        # Steam Guard 令牌类
        self.guard = None
        # Steam Info 账户信息类
        self.info = None
        # Steam Login 登录类
        self.login = None
        # Steam Maket 市场类
        self.market = None
        # Steam Offer 报价类
        self.offer = None
    
    """
    @description: 根据 config.ini 配置文件对子模块进行初始化
    -------
    @param:
    -------
    @return:
    """
    def init(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        # Steam Chat 聊天模块
        if (config.get("moudule to enable", "chat").lower() == "true"):
            self.chat = chat.r_steam_chat()
        # Steam Guard 令牌模块
        self.guard = guard.r_steam_guard(self._steam_id)


"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    r_steam = r_steam("", "2", "3")
    r_steam.init()
    print(r_steam.guard._shared_secret)
    print(r_steam.guard._identity_secret)
    print(r_steam.guard.get_one_time_code())