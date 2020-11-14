import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = "https://www.kivano.kg/mobilnye-telefony"


def get_html(url):
    res = requests.get(url)
    return res.text

def write_csv(data):
    with open("kivano.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'price', 'img-url'])
        for item in data:
            writer.writerow([item['title'], item['price'], item['img-url']])


def padding_total(html):
    soup = BeautifulSoup(html, "html.parser")
    padding = soup.find('div', class_="pager-wrap").find_all('a')[-1].get('href')
    total_pages = padding.split('=')[1]
    return int(total_pages)
    

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_="product_listbox")
    
    
    telephon = []
    link = "https://www.kivano.kg"
    for item in items:
        price = item.find('div', class_="listbox_price")
        item = item.find('img')
        img = soup.find('div', class_="listbox_img pull-left")

        item = str(item).split('=')
        item = str(item).split('src')
        item = str(item).split('"')

        price = str(price).split('>')
        price = str(price[2]).split('<')
        
        img = img.find('a').get('href')
        telephon.append({
            'img-url': 
                    link + img,
            'price': 
                    price[0],
            'title':
                    item[1]})
        write_csv(telephon)
    return(telephon)
    

def main():
    start = datetime.datetime.now()
    html = get_html(url)
    data = get_content(html)
    total_padding = padding_total(html)
    
    main_url = "https://www.kivano.kg/mobilnye-telefony?page=1"
    base_url = "https://www.kivano.kg/mobilnye-telefony?"
    page_url = "page="
    
    for i in range(1, total_padding + 1):
        url_gen = base_url + page_url + str(i)
        html_page = get_html(url_gen)
        get_content(html_page)
    end = datetime.datetime.now()
    res = end - start
    print(res) 

if __name__ == '__main__':
    main()