# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def login(username, password, driver):
    initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    driver.find_element_by_id('login_user').click()
    sleep(3)
    loginname=driver.find_element_by_id('username')
    loginname.clear()
    loginname.send_keys(username)
   
    driver.find_element_by_id('password').send_keys(password)
   
    print ("Please click the verification by yourself...")
    while True:                     
        if driver.current_url != initmy_url:
            print (">>>>>>Waiting for the Correct Verification!<<<<<<")
            sleep(1)
        else:
            break
        
def relogin(username, password, driver):
    loginname=driver.find_element_by_id('username')
    loginname.clear()
    loginname.send_keys(username)
   
    driver.find_element_by_id('password').send_keys(password)
   
    print ("Please click the verification by yourself...")
    while EC.presence_of_element_located((By.ID, "relogin")):                     
        print (">>>>>>Waiting for the Correct Verification!<<<<<<")
        if EC.presence_of_element_located((By.ID, "qd_closeDefaultWarningWindowDialog_id")):
            driver.find_element_by_id("qd_closeDefaultWarningWindowDialog_id").click()