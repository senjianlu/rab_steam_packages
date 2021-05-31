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
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

    
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
                                rsa_timestamp):
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
def login_by_session(username, password, guard, session=None):
    # 主 Session
    if (session):
        login_session = session
    else:
        login_session = requests.session()
    # 获取 RSA 公钥
    rsa_params = get_rsa_params_for_session_login(login_session, username)
    # 加密 Steam 密码
    encrypted_password = base64.b64encode(
        rsa.encrypt(password.encode("utf-8"), rsa_params["rsa_key"]))
    # 获取服务器端生成 RSA 公钥的时间戳
    rsa_timestamp = rsa_params['rsa_timestamp']
    # 使用 Steam 令牌类获取一次性登录令牌
    two_factor_code = guard.get_two_factor_code()
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
@description: 使用 Selenium 的 Steam 登录
-------
@param:
-------
@return:
"""
def login_by_selenium(username, password, driver, btn_xpath, guard=None):
    # 主 Driver
    login_driver = driver
    # 记录 Steam 登录按钮点击前的页面，登录后切换回原窗口
    print("需要 Steam 登录的网页标题：" + login_driver.title)
    handle_before_login = login_driver.current_window_handle
    handles_num_before_login = len(login_driver.window_handles)
    # 点击登录按钮
    login_driver.find_element_by_xpath(btn_xpath).click()
    # 等待 1 秒
    time.sleep(1)
    # 循环所有窗口以捕获 Steam 登录窗口
    for window_handle in login_driver.window_handles:
        login_driver.switch_to.window(window_handle)
        if ("steam community" == login_driver.title.lower().strip()):
            break
    print("切换至 Steam 登录窗口，当前窗口标题：" + login_driver.title)
    # 等待登录按钮出现
    element = WebDriverWait(login_driver, 10, 0.1).until(
        EC.presence_of_element_located((By.XPATH,
            "//input[@id='imageLogin']")))
    # 检查是否已经登录
    try:
        time.sleep(1)
        # 如果有当前账户名说明已经登录完成了
        account_div = login_driver.find_element_by_class_name(
            "OpenID_loggedInAccount")
        logined_flg = True
    except Exception as e:
        logined_flg = False
    # 登录的情况下进行登出操作
    if (logined_flg):
        print("Steam 当前已经处于登录状态，尝试登出...")
        # 选择登出这个账号
        logout_div_a = login_driver.find_element_by_xpath(
            "//div[@class='OpenID_Logout']/a")
        logout_div_a.click()
        time.sleep(1)
    print("Steam 开始尝试登录，账户名：" + username)
    # Steam 用户名输入框
    steam_account_name_input = login_driver \
                                .find_element_by_id("steamAccountName")
    # Steam 密码输入框
    steam_password_input = login_driver \
                                .find_element_by_id("steamPassword")
    # 输入用户名和密码
    steam_account_name_input.send_keys(username)
    steam_password_input.send_keys(password)
    # 点击登录按钮
    login_driver.find_element_by_id("imageLogin").click()
    # 有令牌的情况下等待弹出令牌输入窗口
    if (guard):
        # 等待需要令牌的弹窗出现
        element = WebDriverWait(login_driver, 10, 0.1).until(
            EC.presence_of_element_located((By.XPATH,
                "//input[@id='twofactorcode_entry']")))
        twofactorcode_entry_input = login_driver.find_element_by_id(
            "twofactorcode_entry")
        # 等待 3 秒弹窗可见后，生成并输入令牌
        time.sleep(3)
        two_factor_code = guard.get_two_factor_code()
        print("登录令牌码：" + two_factor_code)
        twofactorcode_entry_input.send_keys(guard.get_two_factor_code())
        # 提交按钮
        submit_btn = login_driver.find_element_by_xpath(
            "//div[@id='login_twofactorauth_buttonset_entercode']/div")
        submit_btn.click()
    # 到这里 Steam 登录就已经完成，开始切换至原窗口
    for _ in range(0, 60):
        time.sleep(1)
        if (len(login_driver.window_handles) == handles_num_before_login):
            break
    time.sleep(3)
    login_driver.switch_to.window(handle_before_login)
    print("已经切换回原窗口，当前窗口标题：" + login_driver.title)
    # 返回
    return login_driver
    

"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    pass