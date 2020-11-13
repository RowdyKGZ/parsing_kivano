import requests
from bs4 import BeautifulSoup
import csv


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
    
    return(telephon)
    



def main():
    html = get_html(url)
    data = get_content(html)
    write_csv(data)

if __name__ == '__main__':
    main()