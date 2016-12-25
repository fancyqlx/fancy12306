# -*- coding: utf-8 -*-
"""A command-line interface.

Usage:
    tickets.py [-c]

Options:
    -h,--help   show help
    -c  set the config

Example:
    tickets.py username password beijing shanghai 2017-01-01
    tickets.py
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from login import login, relogin
from fancy12306.docopt import docopt
from config import loadPassengers, setConfig, readConfig


ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
confirm_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

driver = webdriver.Chrome()

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    set_config = arguments['-c']
    information = {}
    if set_config:
        username = input("username: ")
        password = input("password: ")
        from_station = input("from_station: ")
        to_station = input("to_station: ")
        date = input("date(eg. 2017-01-01): ")
        information["username"] = username
        information["password"] = password
        information["from_station"] = from_station
        information["to_station"] = to_station
        information["date"] = date
        information["passengers"] = {}
    else:
        try:
            information = readConfig()
        except:
            print (">>>>>>There is no information in config.ini<<<<<<")
            print (">>>>>>You can restart the programe via 'tickets.py -c'<<<<<<")
            driver.quit()
            sys.exit()
        
    """Login"""
    #driver.get(ticket_url)
    driver.get(login_url)
    login(information["username"],information["password"],driver)    
    print ("Current url is: ", driver.current_url)
    
    """Loading passengers"""
    if len(information["passengers"]) == 0:
        information["passengers"] = loadPassengers(driver)
    
    wanted_passengers = {}
    keys = input("Please enter the numbers of passengers you want to add (eg., 1 2 3 4):").split()
    for i in keys:
        wanted_passengers[i] = information["passengers"][i]
    information["wanted_passengers"] = wanted_passengers

    print (">>>>>>Configuration is finished<<<<<<<<")
    print ("Passengers you added: ", wanted_passengers)
    print ("from_station: ", information["from_station"])
    print ("to_station: ", information["to_station"])    
    print ("date: ", information["date"])
    setConfig(information)
    return information
    
def bookTickets(information):
    username = information["username"]
    password = information["password"]
    passengers = information["passengers"]
    wanted_passengers = information["wanted_passengers"]
    from_station = information["from_station"]
    to_station = information["to_station"]
    date = information["date"]
    
    """Booking tickets"""
    
    try:
        print ("Reversing...")
        # 跳回购票页面
        driver.get(ticket_url)
        if driver.find_element_by_id("login_user").is_displayed():
            sleep(1)
            login(username,password,driver)    
        
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

def lastStep(information,driver):
    pass


if __name__ == '__main__':
    information = cli()
    bookTickets(information)