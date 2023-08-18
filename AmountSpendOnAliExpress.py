from bs4 import BeautifulSoup
import csv

with open('orders.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

order_items = soup.find_all(class_='order-item')

total_sum = 0

with open('orders.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Name", "Price", "Order Date"])
    for order_item in order_items:
        item_name_element = order_item.find(class_='order-item-content-info-name')
        if item_name_element:
            item_name = item_name_element.text.strip()
        else:
            item_name = "N/A"

        price_element = order_item.find(class_='order-item-content-opt-price-total')
        price_tags = price_element.find_all(class_='es--char--1Z3wUdt')
        price = ''.join(tag.text for tag in price_tags)

        # Remove the "US $" prefix and convert the price to a float
        price = price.replace('US $', '')
        total_sum += float(price)

        order_date_element = order_item.find('div', string='Order date:')
        if order_date_element:
            order_date = order_date_element.find_next('div', class_='comet-widget-datetime').get_text(strip=True)
        else:
            order_date = "N/A"

        writer.writerow([item_name, float(price), order_date])

        print("Item:", item_name)
        print("Price:" + str(price) + " USD")
        print("Order Date:", order_date)
        print("Total sum:", "{:.2f}".format(total_sum), "USD")
        print("----------")

# Print the total sum of all orders with 2 decimal places
print("\n\n----------")
print("Total sum:", "{:.2f}".format(total_sum), "USD")
