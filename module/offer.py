#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: /root/GitHub/rab_steam_packages/module/offer.py
# @DATE: 2021/05/21 Fri
# @TIME: 15:38:42
#
# @DESCRIPTION: Steam 报价模块


import json
import requests
import sys
sys.path.append("..")
from module import api


"""
@description: Steam Offer 报价类
-------
@param:
-------
@return:
"""
class r_steam_offer():

    """
    @description: 初始化
    -------
    @param:
    -------
    @return:
    """
    def __init__(self, api_key, language):
        # Steam 开发者 API KEY
        self._api_key = api_key
        # 语言
        self._language = language

    """
    @description: 获取当前满足条件的所有报价信息（默认为所有未被接受的报价信息）
    -------
    @param: /Steam_Web_API/IEconService#GetTradeOffers_(v1)
    -------
    @return:
    """
    def get_trade_offers(self,
                         get_sent_offers=True,
                         get_received_offers=True,
                         get_descriptions=True,
                         active_only=True,
                         historical_only=False,
                         time_historical_cutoff=None):
        params = {
            "key": self._api_key,
            "get_sent_offers": get_sent_offers,
            "get_received_offers": get_received_offers,
            "get_descriptions": get_descriptions,
            "language": self._language,
            "active_only": active_only,
            "historical_only": historical_only,
            "time_historical_cutoff": time_historical_cutoff
        }
        r = api.call("GET", "IEconService", "GetTradeOffers", "v1", params)
        return json.loads(r.text)
        
    """
    @description: 获取指定报价信息
    -------
    @param: /Steam_Web_API/IEconService#GetTradeOffer_(v1)
    -------
    @return:
    """
    def get_trade_offer(self, trade_offer_id):
        params = {
            "key": self._api_key,
            "tradeofferid": trade_offer_id,
            "language": self._language
        }
        r = api.call("GET", "IEconService", "GetTradeOffer", "v1", params)
        return json.loads(r.text)
    
    """
    @description: 拒绝对方的报价
    -------
    @param: /Steam_Web_API/IEconService#DeclineTradeOffer_(v1)
    -------
    @return:
    """
    def decline_trade_offer(self, trade_offer_id):
        params = {
            "key": self._api_key,
            "tradeofferid": trade_offer_id
        }
        r = api.call("POST", "IEconService", "DeclineTradeOffer", "v1", params)
        return json.loads(r.text)
    
    """
    @description: 取消己方的报价
    -------
    @param: /Steam_Web_API/IEconService#CancelTradeOffer_(v1)
    -------
    @return:
    """
    def cancel_trade_offer(self, trade_offer_id):
        params = {
            "key": self._api_key,
            "tradeofferid": trade_offer_id
        }
        r = api.call("POST", "IEconService", "CancelTradeOffer", "v1", params)
        return json.loads(r.text)
    
    """
    @description: 获取交易历史记录
    -------
    @param: /Steam_Web_API/IEconService#GetTradeHistory_(v1)
    -------
    @return:
    """
    def get_trade_history(self,
                          max_trades=10,
                          start_after_time=None,
                          start_after_tradeid=None,
                          get_descriptions=True,
                          navigating_back=True,
                          include_failed=True,
                          include_total=True):
        params = {
            'key': self._api_key,
            'max_trades': max_trades,
            'start_after_time': start_after_time,
            'start_after_tradeid': start_after_tradeid,
            'get_descriptions': get_descriptions,
            'navigating_back': navigating_back,
            'include_failed': include_failed,
            'include_total': include_total
        }
        r = api.call("GET", "IEconService", "GetTradeHistory", "v1", params)
        return json.loads(r.text)