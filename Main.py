#!/usr/bin/env python

from selenium import webdriver
import time

#Opening the webpage
options = webdriver.ChromeOptions() 

try:
    browser = webdriver.Chrome("C:/Users/---PATH_TO_FILE---/chromedriver.exe")
except:
    try:
        browser = webdriver.Chrome("/home/---PATH_TO_FILE---/chromedriver_100")
    except:
        try:
            browser = webdriver.Chrome("/home/---PATH_TO_FILE---/chromedriver_99")
        except:
            browser = webdriver.Chrome("/home/---PATH_TO_FILE---/chromedriver_98")


browser.get('https://www.aliexpress.com/p/order/index.html')

print("")
print("------------------------------------------------------------------------------------")
print("-----------------------   Login to AliExpress                -----------------------")
print("-----------------------   Close additional tabs if opened    -----------------------")
print("-----------------------   Accept/decline cookies if needed   -----------------------")
print("-----------------------   Press Enter to continue...         -----------------------")
print("------------------------------------------------------------------------------------")
raw_input("")

btn_DeletedOrders = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]')
btn_DeletedOrders.click()
time.sleep(1)

while(True):
    try:
        #Finding target
        btn_ViewMoreOrders = browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[3]/button/span')
        #Scrolling to target
        browser.execute_script("return arguments[0].scrollIntoView(true);", btn_ViewMoreOrders)
        time.sleep(2)

        btn_ViewMoreOrders.click()
        time.sleep(2)

    except:
        break

i = 1
amount_spent = 0

while(True):
    try:
        #Finding target
        text_price = browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[2]/div/div[' + str(i) + ']/div[3]/div[2]/div[1]/span')
        #Scrolling to target
        browser.execute_script("return arguments[0].scrollIntoView(true);", text_price)

        #Reading target
        text_price_string = browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[2]/div/div[' + str(i) + ']/div[3]/div[2]/div[1]/span').text
        text_price_string = text_price_string.replace("Total: US $", "")
        text_price_float = float(text_price_string)

        amount_spent = amount_spent + text_price_float

        print("text_price_float: " + str(text_price_float))
        print("amount_spent: " + str(amount_spent))

        i = i + 1
    except:
        break

print("amount_spent: " + str(amount_spent))

time.sleep(1)


#Closing browser
browser.close()
