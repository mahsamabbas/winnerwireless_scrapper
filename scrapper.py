import requests
import xlsxwriter
from bs4 import BeautifulSoup
import re
import urllib.parse

links = list()



def write_sheet(main_page, page, text):
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Page Start")
    file_name = main_page.split("date=")[1]
    print(file_name)
    print("Main Page - ", main_page)
    print("Page - ", page)
    print("Text - ", text)

    headers = ['Main Page Link', 'Page Link', 'Text', 'Url', 'Title', 'Description']

    workbook = xlsxwriter.Workbook(file_name + '.xlsx')
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet()
    col = 0

    for item in headers:
        worksheet.write(0, col, item, bold)
        col += 1

    images = text.findAll("a", attrs={"data-ca-image-id":True})
    #print(images)

    for img in images:
        print(img['href'])

    title = text.find("h1", {"class" : "mainbox-title"}).text

    print(title)

    all_images = text.findAll('img')

    r = re.compile('id=(\d+)')

    for image in all_images:
        if "upc_barcode" in image['src']:
            print(r.search(image['src']).group(1))

    product_code = text.find("span", {"class": "ty-control-group__item"})
    #url = urllib.parse.urlparse(product_code)

    #params = urllib.parse.parse_qs(url.query)
    print(product_code.text)

    #if 'id' in params:
        #print(params['id'])

    product_desc_parent = text.find("div", {"id": "content_description"})

    product_desc = product_desc_parent.findAll('p')

    print(product_desc[1].text)

    # worksheet.write('A1', 'Main Page Link')
    # worksheet.write('B1', 'Page Link')
    workbook.close()
    raise SystemExit


def hit_links():

    if len(links) == 0:
        return;

    for l in links:
        print("Page - ", l)
        page = requests.get(l)
        soup = BeautifulSoup(page.text, 'html.parser')

        products_div = soup.findAll(class_='ty-grid-list__item-name')


        for index, item in enumerate(products_div):
            product_page = requests.get(item.find('a')['href'])
            soup = BeautifulSoup(product_page.text, 'html.parser')

            write_sheet(l,item.find('a')['href'], soup )



def get_links():
    page = requests.get('http://www.winnerwireless.com/new-arrivals.html')

    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    new_arrival_div = soup.find(id='sidebox_71')

    new_arrival_div_links = new_arrival_div.find_all('a')

    for link in new_arrival_div_links:
        links.append(link['href'])
    #Calling HIT LINKS
    hit_links()

get_links()

