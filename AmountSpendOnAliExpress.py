from bs4 import BeautifulSoup
import csv

import datetime
import matplotlib.pyplot as plt

with open('orders.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

order_items = soup.find_all(class_='order-item')

total_sum = 0

list_of_orderID = []

with open('orders.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Name", "Price", "Order Date"])
    for order_item in order_items:
        # ORDER TITLE
        item_name_element = order_item.find(class_='order-item-content-info-name')
        if item_name_element:
            item_name = item_name_element.text.strip()
        else:
            item_name = "N/A"

        # ORDER PRICE
        price_element = order_item.find(class_='order-item-content-opt-price-total')
        price_tags = price_element.find_all(class_='es--char--1Z3wUdt')
        price = ''.join(tag.text for tag in price_tags)

        # Remove the "US $" prefix and convert the price to a float
        price = price.replace('US $', '')
        total_sum += float(price)

        # ORDER DATE
        order_date_element = order_item.find(class_='order-item-header-right-info')
        if order_date_element:
            order_date_id = order_date_element.text.strip()
        else:
            order_date_id = "N/A"

        # Remove "Order date: " from order_date
        order_date_id = order_date_id.replace('Order date: ', '')

        # Remove everything after "Order ID: "
        order_date = order_date_id.split('Order ID:')[0]

        # Remove the word "copy" from the order date
        order_id = order_date_id.replace('Copy', '')

        print(order_id)

        index = order_id.find("Order ID: ")

        if index != -1:
            # Extract the substring starting from the position after "Order ID: "
            order_id = order_id[index + len("Order ID: "):]
            print(order_id)
        else:
            print("No 'Order ID:' found in the input string.")
        
        list_of_orderID.append(order_id)

        # WRITE TO CSV-FILE
        writer.writerow([item_name, float(price), order_date])

        print("Item:", item_name)
        print("Price: " + str(price) + " USD")
        print("Order Date:", order_date)
        print("Total sum:", "{:.2f}".format(total_sum), "USD")
        print("----------")

# Print the total sum of all orders with 2 decimal places
print("\n\n----------")
print("Total sum:", "{:.2f}".format(total_sum), "USD")

print("Number of orders:", len(order_items))

# convert order_date to datetime object and plot a histogram


order_dates = []
for order_item in order_items:
    order_date_element = order_item.find(class_='order-item-header-right-info')
    if order_date_element:
        order_date = order_date_element.text.strip()
    else:
        order_date = "N/A"

    # Remove "Order date: " from order_date
    order_date = order_date.replace('Order date: ', '')
    # Remove everything after "Order ID: "
    order_date = order_date.split('Order ID:')[0]

    order_date = datetime.datetime.strptime(order_date, '%b %d, %Y')
    order_dates.append(order_date)
    
def get_difference(date1, date2):
    delta = date2 - date1
    return delta.days

# Calcualting the amount of weeks betwen 4th of february 2016 and today
date1 = datetime.datetime(2016, 2, 4)
date2 = datetime.datetime.now()
weeks = get_difference(date1, date2) / 7
months = get_difference(date1, date2) / 30

plt.hist(order_dates, bins=int(months))
plt.xlabel('Ordering month')
plt.ylabel('Number of orders')
plt.title('Amount of orders per month')
plt.show()
