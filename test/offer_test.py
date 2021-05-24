#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: D:\GitHub\rab_steam_packages\test\api_test.py
# @DATE: 2021/05/24 周一
# @TIME: 08:44:02
#
# @DESCRIPTION: Offer 报价模块测试


import sys
sys.path.append("..")
import accounts
from modules import offer


"""
@description: 获取当前满足条件的所有报价信息的测试
-------
@param:
-------
@return:
"""
def get_trade_offers_test(r_steam_offer):
    print(r_steam_offer.get_trade_offers(active_only=False))

"""
@description: 获取指定报价信息测试
-------
@param:
-------
@return:
"""
def get_trade_offer_test(r_steam_offer):
    trade_offer_id = r_steam_offer.get_trade_offers(active_only=False)[
        "response"]["trade_offers_received"][0]["tradeofferid"]
    print(r_steam_offer.get_trade_offer(trade_offer_id))

"""
@description: 获取指定报价信息测试
-------
@param:
-------
@return:
"""
def get_trade_history_test(r_steam_offer):
    print(r_steam_offer.get_trade_history())


"""
@description: 测试用类初始化和测试入口
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    username, password, api_key = accounts.get_private_info_by_steam_id(no=1)
    r_steam_offer_for_test = offer.r_steam_offer(api_key, "english")
    # 测试 CASE01
    get_trade_offers_test(r_steam_offer_for_test)
    # 测试 CASE02
    get_trade_offer_test(r_steam_offer_for_test)
    # 测试 CASE03
    get_trade_history_test(r_steam_offer_for_test)