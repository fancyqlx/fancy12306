# -*- coding: utf-8 -*-
import configparser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def loadPassengers(driver):
    #initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    passengers_url = "https://kyfw.12306.cn/otn/passengers/init"
    driver.get(passengers_url)
    passengers = {}
    count = 0
    while True:
        table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"passengerAllTable")))
        last = table.find_element_by_class_name("last")
        if len(passengers)>0 and last.find_elements_by_tag_name("td")[1].text == passengers[str(count)]:
            break
        rows = table.find_elements_by_tag_name("tr")
        for row in rows:
            col = row.find_elements_by_tag_name("td")[1]
            count += 1
            passengers[str(count)] = col.text
        if len(passengers) == 0:
            print (">>>>>>There is no passengers<<<<<<")
            break
        else:
            driver.find_element_by_link_text("下一页").click()
            sleep(1)
    print (passengers)
    return passengers

def ConfigSectionMap(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def setConfig(information):
    username = information["username"]
    password = information["password"]
    passengers = information["passengers"]
    wanted_passengers = information["wanted_passengers"]
    from_station = information["from_station"]
    to_station = information["to_station"]
    date = information["date"]
    cfgfile = open("../config.ini","w")
    config = configparser.ConfigParser()
    config.add_section("Personal Information")
    config.set("Personal Information","username",username)
    config.set("Personal Information","password",password)
    config.add_section("Passengers")
    for i in range(1,len(passengers)+1):
        config.set("Passengers",str(i),passengers[str(i)])
    config.add_section("wanted_passengers")
    for i in range(1,len(wanted_passengers)+1):
        config.set("wanted_passengers",str(i),wanted_passengers[str(i)])
    config.add_section("Tickets Information")
    config.set("Tickets Information","from_station",from_station)
    config.set("Tickets Information","to_station",to_station)
    config.set("Tickets Information","date",date)
    config.write(cfgfile)
    cfgfile.close()
    
    
def readConfig():
    config = configparser.ConfigParser()
    config.read("../config.ini")
    information = {}
    information.update(ConfigSectionMap(config,"Personal Information"))
    information.update({"passengers":ConfigSectionMap(config,"Passengers")})
    information.update(ConfigSectionMap(config,"Tickets Information"))
    return information