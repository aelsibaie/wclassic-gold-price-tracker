from bs4 import BeautifulSoup
import requests
from csv import writer
import datetime
import statistics
from pathlib import Path

# Example data: 1 Gold = US $0.059 

DIR = '/home/pi/wowc_price_tracker/'

def append_list_as_row(file_name, list_of_elem):
    my_file = Path(file_name)
    if my_file.is_file():
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)
    else:
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            if len(list_of_elem) == 4:
                csv_writer.writerow(['datetime', 'avg', 'min', 'max'])
            csv_writer.writerow(list_of_elem)

def get_price_data(url, out_file_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    found = soup.find_all(class_="products__exch-rate input-gold")

    out_list = []
    price_list = []
    raw_list = []
    now = str(datetime.datetime.now())
    out_list.append(now)
    raw_list.append(now)

    for i in found:
        # print(i.span['data-ppu'])
        price_list.append(float(i.span['data-ppu']))

    mean = statistics.mean(price_list)
    my_min = min(price_list)
    my_max = max(price_list)
    out_list.append(mean)
    out_list.append(my_min)
    out_list.append(my_max)
    raw_list.append(price_list)

    append_list_as_row(DIR + out_file_name + '.csv', out_list)
    append_list_as_row(DIR + out_file_name + '_raw.csv', raw_list)


if __name__ == "__main__":
    ef_horde = "https://www.g2g.com/wow-classic-tbc/gold-29076-29077?&faction=41398&platform=41202&sorting=lowest_price"
    ef_ally =  "https://www.g2g.com/wow-classic-tbc/gold-29076-29077?&faction=41398&platform=41200&sorting=lowest_price"
    get_price_data(ef_horde, 'ef_horde')
    get_price_data(ef_ally, 'ef_ally')
