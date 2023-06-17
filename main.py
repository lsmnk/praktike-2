from bs4 import BeautifulSoup as bs4
import bs4
import requests
import xlsxwriter

main_url = 'https://trade59.ru/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
ilonmask = [('Наименование', 'цена', 'ссылка', 'картинка')]

def get_soup(url):
    
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser') 

categories_page = get_soup(main_url+'catalog.html?cid=7' )
categories = categories_page.findAll( 'a', class_='cat_item_color')
for cat in categories:
    subcategories_page = get_soup(main_url+cat['href'])
    subcategories = subcategories_page.findAll('a', class_='cat_item_color')
    for subcat in subcategories:
        iphones_page = get_soup(main_url+subcat['href'])
        iphones = iphones_page.findAll('div', class_='items-list')
        for iphone in iphones:
            title = iphone.find('a')['title'].strip()
            price_elem = iphone.find('div', class_='price')
            if price_elem is not None and isinstance(price_elem.string, str):
                price = price_elem.string.strip()
            else:
                price = 'Not found'
            url = iphone.find('a')['href'].strip()
            img = iphone.find('div', class_='image')['style'].split('url(')[1].split(')')[0].replace('/tn/', '/source/')
            ilonmask.append([title, price, url, img])

with xlsxwriter.Workbook('iphones.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    
    for row_num, info in enumerate(ilonmask):
        worksheet.write_row(row_num, 0, info)