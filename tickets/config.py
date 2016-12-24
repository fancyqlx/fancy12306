# -*- coding: utf-8 -*-
import ConfigParser

def loadPassenger(driver):
    #initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    passengers_url = "https://kyfw.12306.cn/otn/passengers/init"
    driver.get(passengers_url)
    passengers = []
    count = 0
    while True:
        table = driver.find_element_by_id("passenderALLTable")
        last = table.find_element_by_class("last")
        if len(passengers)>0 and last.find_element_by_tag_name("tr")[1].text == passengers[-1][1]:
            break
        rows = table.find_elements_by_tag_name("tr")
        for row in rows:
            col = row.find_elements_by_tag_name("td")[1]
            count += 1
            passengers.append((count, col.text))
        if len(passengers) == 0:
            print (">>>>>>There is no passengers<<<<<<")
            break
        else:
            driver.find_element_by_class("btn92 next disable").click()
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

def setConfig(username, password, passengers, from_station, to_station, date):
    cfgfile = open("../config.ini","w")
    config = ConfigParser.ConfigParser()
    config.add_section("Personal Information")
    config.set("Personal Information","username",username)
    config.set("Personal Information","password",password)
    config.add_section("Passengers")
    for passenger in passengers:
        config.set("Passengers",passenger[0],passenger[1])
    config.add_section("Tickets Information")
    config.set("Tickets Information","from_station",from_station)
    config.set("Tickets Information","to_station",to_station)
    config.set("Tickets Information","date",date)
    config.write(cfgfile)
    cfgfile.close()
    
    
def readConfig():
    config = ConfigParser.ConfigParser()
    config.read("../config.ini")
    passengers = ConfigSectionMap(config, "Passengers")