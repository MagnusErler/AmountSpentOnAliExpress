#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

browser.get('https://www.aliexpress.com/p/order/index.html')

print("")
print("------------------------------------------------------------------------------------")
print("-----------------------   Login to AliExpress                -----------------------")
print("-----------------------   Close additional tabs if opened    -----------------------")
print("-----------------------   Accept/decline cookies if needed   -----------------------")
print("-----------------------   Press Enter here to continue...    -----------------------")
print("------------------------------------------------------------------------------------")
input("")

#Going to 'deleted orders'
btn_DeletedOrders = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/div[1]/div[2]')
btn_DeletedOrders.click()

time.sleep(1)

#Open-up all deleted orders
attempts = 0
while attempts < 10:
    try:
        #Finding 'view more orders' button
        btn_ViewMoreOrders = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[2]/div[3]/button')
        #Scrolling to 'view more orders' button
        browser.execute_script("return arguments[0].scrollIntoView(true);", btn_ViewMoreOrders)

        btn_ViewMoreOrders.click()

        attempts = 0
    except:
        time.sleep(0.5)
        attempts += 1

#Calculate amount spent
i = 1
amount_spent = 0
attempts = 0
while attempts < 10:
    try:
        #Finding 'price of single item'
        text_price = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[2]/div[2]/div/div[' + str(i) + ']/div[3]/div[2]/div[1]/span')
        #Scrolling to 'price of single item'
        browser.execute_script("return arguments[0].scrollIntoView(true);", text_price)

        #Reading 'price of single item'
        text_price_string = text_price.text
        text_price_string = text_price_string.replace("Total: US $", "")
        text_price_float = float(text_price_string)

        amount_spent = amount_spent + text_price_float

        print("Price of item: $ " + str("%0.2f" % text_price_float))
        print("Current total amount spent on AliExpress: $ " + str("%0.2f" % amount_spent))

        i = i + 1

        attempts = 0
    except:
        time.sleep(0.5)
        attempts += 1
print("---------------------------------------------------")
print("Total amount spent on AliExpress: $ " + str("%0.2f" % amount_spent))

browser.close()
