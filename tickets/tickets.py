# -*- coding: utf-8 -*-
"""A command-line interface.

Usage:
    tickets.py [<username> <password> <from_station> <to_station> <date>]

Options:
    -h,--help   显示帮助菜单

Example:
    tickets.py username password beijing shanghai 2017-01-01
    tickets.py
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from login import login, relogin
from fancy12306.docopt import docopt


ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
confirm_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

driver = webdriver.Chrome()

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    username = arguments['<username>']
    password = arguments['<password>']
    from_station = arguments['<from_station>']
    to_station = arguments['<to_station>']
    date = arguments['<date>']

def bookTickets(username,password,from_station,to_station,date):
    driver.get(ticket_url)
    while driver.find_element_by_id("login_user").is_displayed():
        sleep(1)
        login(username,password,driver)    
        if driver.current_url == initmy_url:
            print ("Login Success!")
            break
    
    try:
        print ("Reversing...")
        # 跳回购票页面
        driver.get(ticket_url)
   
        # 加载查询信息
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "train_date")))
        #WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_id('train_date').is_displayed())
        driver.add_cookie({'name':'_jc_save_fromDate', 'value':date})
      
        driver.find_element_by_id('query_ticket').submit()
        sleep(1)
        driver.find_element_by_id('fromStationText').click()
        driver.find_element_by_id('fromStationText').send_keys(from_station)
        driver.find_element_by_id('fromStationText').send_keys(Keys.ENTER)
        sleep(1)
        driver.find_element_by_id('toStationText').click()
        driver.find_element_by_id('toStationText').send_keys(to_station)
        driver.find_element_by_id('toStationText').send_keys(Keys.ENTER)                      
        sleep(1)
      
        count = 0                     
        while driver.current_url[0:41] == ticket_url:
            driver.find_element_by_id('query_ticket').click()
            #WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_id('t-list').is_displayed())
            sleep(5)
            count +=1
            print ("Reserving for %d times" % count)
            sleep(1)
            try:
                driver.find_element_by_link_text("预订").click()
                sleep(1)
            except:
                print ("还没开始预订")
                continue                    
      
        #driver.get(confirm_url)
    except Exception as e:
        print (e)
    
if __name__ == '__main__':
    bookTickets("qlx810773948","810773948qlx","武汉","合肥","2017-01-19")
