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
from module import chat
from module import guard
from module import login
from module import offer


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
        # Steam Login 登录类（暂时不使用类只使用其 Session 登录方法）
        # self.login = None
        # Steam Maket 市场类
        self.market = None
        # Steam Offer 报价类
        self.offer = None
        # Steam API 语言
        self._language = "english"
    
    """
    @description: 根据 config.ini 配置文件进行初始化（包括模块和其他语言设置等）
    -------
    @param:
    -------
    @return:
    """
    def init(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        # 基础信息初始化
        # Steam API 语言
        self._language = config.get("api config", "language")
        # 子模块初始化
        # Steam Chat 聊天模块
        if (config.get("moudule to enable", "chat").lower() == "true"):
            self.chat = chat.r_steam_chat()
        # Steam Guard 令牌模块
        self.guard = guard.r_steam_guard(self._steam_id)
        # Steam Login 登录模块（暂时不使用类只使用其 Session 登录方法）
        self._session = login.login_by_session(
            self._username, self._password, self.guard)
        # Steam Info 账户信息模块
        # self.info = info.r_steam_info()
        # Steam Maket 市场模块
        # self.market = login.r_steam_market()
        # Steam Offer 报价模块
        self.offer = offer.r_steam_offer(self._api_key, self._language)


"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":

    from module import api
    from test import accounts

    # # 获取 Steam 私密信息
    # username, password, api_key, steam_id = accounts \
    #     .get_private_info_by_steam_id(no=3)
    # r_steam = r_steam(steam_id, username, password, api_key=api_key)
    # r_steam.init()
    # response = r_steam._session.get(api.STEAM.URL.COMMUNITY).text
    # if (username.lower() in response.lower()):
    #     print("OK")
    #     confirmations = r_steam.guard.get_confirmations(r_steam._session, "conf")
    #     print(confirmations)
    #     for confirmation in confirmations:
    #         print(confirmation._id)
    #         print(r_steam.guard.get_confirmation_info(r_steam._session, confirmation))
    #         # print(r_steam.guard.cancel_confirmation(r_steam._session, confirmation))
    # else:
    #     print("NG")
