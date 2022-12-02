#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime

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
list_of_orderID = []
list_of_price = []
list_of_totalPrice = []
while attempts < 10:
    try:
        #Finding price of single item
        text_price = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[2]/div[2]/div/div[' + str(i) + ']/div[3]/div[2]/div[1]/span')
        #Scrolling to price of single item
        browser.execute_script("return arguments[0].scrollIntoView(true);", text_price)
        #Reading price of single item
        text_price_string = text_price.text
        text_price_string = text_price_string.replace("Total: US $", "")
        text_price_float = float(text_price_string)

        amount_spent = amount_spent + text_price_float

        #Finding Order ID
        text_orderID = browser.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[2]/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div/div[2]')
        #Reading Order ID
        text_orderID_string = text_orderID.text
        text_orderID_string = text_orderID_string.replace("Order ID: ", "")
        text_orderID_string = text_orderID_string.replace("\\r\\n", "")
        text_orderID_string = text_orderID_string.replace("Copy", "")
        text_orderID_string = text_orderID_string.rstrip()  #Removing newline character from the end of the string


        list_of_orderID.append(text_orderID_string)
        list_of_price.append(str("%0.2f" % text_price_float))
        list_of_totalPrice.append(str("%0.2f" % amount_spent))

        print("Price of item: $ " + str("%0.2f" % text_price_float))
        print("Current total amount spent on AliExpress: $ " + str("%0.2f" % amount_spent))

        ## write a row to the csv file
        #writer.writerow([text_orderID_string, str("%0.2f" % text_price_float), str("%0.2f" % amount_spent)])

        i = i + 1

        attempts = 0
    except:
        time.sleep(0.5)

        list_of_orderID.append("N/A")
        list_of_price.append("N/A")
        list_of_totalPrice.append("N/A")

        attempts += 1


attempts = 0

list_of_orderingDate = []
list_of_deliveringDate = []
list_of_shippingTime = []
# i = 4
# list_of_orderID = ["3018265129357065", "3018382510267065", "3018172457047065"]
# list_of_price = ["1", "2", "3"]
# list_of_totalPrice = ["1", "3", "6"]

j = 0
while j < i:
    if attempts > 50:

        for k in range(i):
            list_of_orderingDate.append("N/A")
            list_of_deliveringDate.append("N/A")
            list_of_shippingTime.append("N/A")

        break

    try:    
        browser.get('https://track.aliexpress.com/logisticsdetail.htm?tradeId=' + str(list_of_orderID[j]))

        time.sleep(5)

        #Finding Delivering date
        text_deliveringDate = browser.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[1]/div[1]/div[2]/div[2]/div/ul/li[1]')
        #Reading Delivering date
        text_deliveringDate_string = text_deliveringDate.text
        text_deliveringDate_string = text_deliveringDate_string[0:16]


        a = 1
        while(True):
            try:
                #Finding Ordering date
                text_orderingDate = browser.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[1]/div[1]/div[2]/div[2]/div/ul/li[' + str(a) + ']')
                #Reading Ordering date
                text_orderingDate_string = text_orderingDate.text

                a = a + 1
            except:
                break

        text_orderingDate_string = text_orderingDate_string[0:16]

        deliveringDate = datetime.strptime(text_deliveringDate_string, '%Y-%m-%d %H:%M')
        orderingDate = datetime.strptime(text_orderingDate_string, '%Y-%m-%d %H:%M')

        shippingTime = (deliveringDate-orderingDate).days

        list_of_orderingDate.append(str(orderingDate))
        list_of_deliveringDate.append(str(deliveringDate))
        list_of_shippingTime.append(str(shippingTime))
        
        print("deliveringDate: " + str(deliveringDate))
        print("orderingDate: " + str(orderingDate))
        print("shippingTime: " + str(shippingTime))


        j = j + 1

        attempts = 0
    except:
        time.sleep(0.5)

        list_of_orderingDate.append("N/A")
        list_of_deliveringDate.append("N/A")
        list_of_shippingTime.append("N/A")

        j += 1

        attempts += 1


# open CSV-file in write mode
f = open('AmountSpendOnAliExpress.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# create header to csv file
writer.writerow(['Order ID', 'Price of item ($)', 'Current total amount spent on AliExpress ($)', 'Ordering date', 'Delivering date', 'Shipping time (days)'])

for i in range(len(list_of_orderID)):
    try:
        writer.writerow([list_of_orderID[i], list_of_price[i], list_of_totalPrice[i], list_of_orderingDate[i], list_of_deliveringDate[i], list_of_shippingTime[i]])
    except:
        continue

# close the CSV-file
f.close()



print("---------------------------------------------------")
print("Total amount spent on AliExpress: $ " + str("%0.2f" % amount_spent))

browser.close()
