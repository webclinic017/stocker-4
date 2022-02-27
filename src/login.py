

import json
import logging
import os.path
import sys
import time

import pyotp
from kiteconnect import KiteConnect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from instrument import get_instrument_all

#import instrument
import util
from constant import Constant


def automated_login(apikey, apisecret, userid, userpassword, otpkey):  # pylint: disable-msg=too-many-locals
    """Summary

    Args:
        apikey (TYPE): Description
        apisecret (TYPE): Description
        userid (TYPE): Description
        userpassword (TYPE): Description
        otpkey (TYPE): Description

    Returns:
        TYPE: Description
    """
    logging.info('+++++++++++++AutoMated Login Start++++++++++++++++')

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    logging.info('Starting Headless Chrome Driver')
    driver = webdriver.Chrome(
        Constant.CHROME_DRIVER_LOCATION, options=chrome_options)
    driver.get(f'https://kite.trade/connect/login?api_key={apikey}&v=3')
    login_id = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="userid"]'))
    login_id.send_keys(userid)

    pwd = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="password"]'))
    pwd.send_keys(userpassword)
    submit = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/form/div[4]/button'))
    submit.click()

    time.sleep(1)

    totp = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="totp"]'))
    authkey = pyotp.TOTP(otpkey)
    totp.send_keys(authkey.now())

    continue_btn = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/form/div[3]/button'))
    continue_btn.click()
    time.sleep(5)
    url = driver.current_url
    initial_token = url.split('request_token=')[1]
    request_token = initial_token.split('&')[0]
    driver.close()
    kite = KiteConnect(api_key=apikey)
    data = kite.generate_session(request_token, api_secret=apisecret)
    kite.set_access_token(data['access_token'])
    logging.info(
        '+++++++++++++++++++++++++AutoMated Login End++++++++++++++++++++++++++')
    return data['access_token'], kite


def login_to_zerodha(apikey, apisecret, userid, userpassword, otpkey):
    """Summary

    Args:
        apikey (TYPE): Description
        apisecret (TYPE): Description
        userid (TYPE): Description
        userpassword (TYPE): Description
        otpkey (TYPE): Description

    Returns:
        TYPE: Description
    """
    logging.info('-------------apikey-------:%s', apikey)
    logging.info('-------------apisecret-------:%s', apisecret)
    logging.info('-------------userid-------:%s', userid)
    logging.info('-------------userpassword-------:%s', userpassword)
    logging.info('-------------otpkey-------:%s', otpkey)
    try:
        access_token, kite = automated_login(
            apikey, apisecret, userid, userpassword, otpkey)
        return access_token, kite
    except Exception as exception:  # pylint: disable=broad-except
        logging.exception("Error Connecting to Kite ::")
        logging.critical(exception, exc_info=True)
        sys.exit(1)


def get_access_token():
    """Summary

    Returns:
        TYPE: Description
    """
    token_file = util.get_curr_date_str() + '.json'
    token_file_path = os.path.join(Constant.DEPLOY_DIR, token_file)
    if not os.path.exists(token_file_path):
        logging.info('Token File Does Not Exists')
        return None

    with open(token_file_path, 'r', encoding='utf-8') as deploy:
        deploy_data = json.load(deploy)
        logging.info('Token File Exists')
        return deploy_data['accessToken']


def save_token_to_file(access_token):
    """Summary

    Args:
        access_token (TYPE): Description
    """
    file_name = util.get_curr_date_str() + '.json'
    file_path = os.path.join(Constant.DEPLOY_DIR, file_name)
    logging.info('Saving Access Token to File %s', file_name)
    with open(file_path, 'w', encoding='utf-8') as token_file:
        json.dump(access_token, token_file, indent=2)


def login():
    """Summary

    Returns:
        TYPE: Description
    """
    logging.info('Check If access token is present')
    access_token = get_access_token()
    logging.info('Access token --->  %s ', access_token)
    if access_token is not None:
        logging.info(
            'Access token already exists - no need for relogin - getting kite session')
        kite = KiteConnect(api_key=Constant.API_KEY)
        kite.set_access_token(access_token)
        return kite

    if util.is_today_holiday():
        logging.info('Today is Trading Holiday')
        return None

    access_token, kite = login_to_zerodha(Constant.API_KEY,
                                          Constant.API_SECRET,
                                          Constant.CLIENT_ID,
                                          Constant.CLIENT_PASSWORD,
                                          Constant.TOTP_KEY)
    logging.info('access_token => %s', access_token)
    token_file = {
        "accessToken": access_token,
        "timeStamp": util.get_epoch()
    }
    logging.info('Saving Instrument File')
    get_instrument_all(kite)
    save_token_to_file(token_file)
    return kite
