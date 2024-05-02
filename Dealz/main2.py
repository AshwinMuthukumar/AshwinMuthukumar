from selenium import webdriver

from bs4 import BeautifulSoup

import pandas as pd

import time

import requests

import threading

import concurrent.futures

var = "shirt under 1000"

var = var.replace(" ","%20")

def ajio(query):

  op = webdriver.ChromeOptions()

  op.add_argument('headless')

  driver = webdriver.Chrome(options=op)

  driver.get('https://www.ajio.com/search/?query=%3Arelevance&text='+query+'shirt&classifier=intent&gridColumns=5')

  driver.implicitly_wait(5)

  html = driver.page_source

  soup = BeautifulSoup(html,'html.parser')

  products = soup.find_all("div",attrs={"class":"item rilrtl-products-list__item item"})

  image_tag = soup.find_all("img", attrs={"class":"rilrtl-lazy-img rilrtl-lazy-img-loaded"})

  Price = []

  Image = []

  Title = []

  Links = []

  Discount = []

  for i in products:

    image_tag = i.find("img", attrs={"class":"rilrtl-lazy-img rilrtl-lazy-img-loaded"})

    if image_tag:

      Image.append(image_tag.get("src"))

      title_tag = i.find('div',attrs={'class':'nameCls'})

      if title_tag:

        Title.append(title_tag.text)

      offer_tag = i.find("span",attrs={"class":"offer-pricess-new"})

      if offer_tag:

        Discount.append(100)

        Price.append(offer_tag.text)

      else:

        discount_tag = i.find("span",attrs={"class":"discount"})

        Discount.append(int(discount_tag.text[2:4]))

        price_tag = i.find("span", attrs={"class":"price"})

        if price_tag:

          Price.append(price_tag.find("strong").text)

      link_tag = i.find("a",attrs={"class":"rilrtl-products-list__link desktop"})

      Links.append("https://www.ajio.com"+link_tag.get("href"))

  df1 = pd.DataFrame({

  'Title':Title,

  'Price':Price,

  'Discount':Discount,

  'Image':Image,

  'Links':Links

  })

  driver.quit()

  return df1

def bwf(query):

  op = webdriver.ChromeOptions()

  op.add_argument('headless')

  driver = webdriver.Chrome(options=op)

  driver.get('https://www.bewakoof.com/search/'+query+'?product_discount=70')

  driver.implicitly_wait(5)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

  time.sleep(1)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  time.sleep(1)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

  time.sleep(1)

  driver.execute_script("window.scrollTo(0, 0);")

  time.sleep(1)

  html = driver.page_source

  soup = BeautifulSoup(html,'html.parser')

  products = soup.find_all("a",attrs={"class":"col-sm-4 col-xs-6 px-2"})

  Price = []

  Image = []

  Title = []

  Links = []

  Discount = []

  j = 0

  for i in products:

    image_tag = i.find("img", attrs={"class":"productImgTag"})

    if image_tag:

      Image.append(image_tag.get("src"))

      title_tag = i.find('h2',attrs={'class':'clr-shade4 h3-p-name undefined false'})

      if title_tag:

        Title.append(title_tag.text)

      price_tag = i.find("div", attrs={"class":"discountedPriceText clr-p-black false"})

      if price_tag:

        Price.append(price_tag.text)

      Acutal_price_tag = i.find("div", attrs={"class":"actualPriceText clr-shade5"})

      if Acutal_price_tag:

        x = Price[j]

        j = j+1

        x = int(x[1:])

        y = int(Acutal_price_tag.text[1:])

        Discount.append(round(((y-x)/y)*100))

      Links.append("https://www.bewakoof.com"+i.get("href"))

  df2 = pd.DataFrame({

  'Title':Title,

  'Price':Price,

  'Discount':Discount,

  'Image':Image,

  'Links':Links

  })

  driver.quit()

  return df2

def flipkart(query):

 site = "https://www.flipkart.com"

 URL = "https://www.flipkart.com/search?q="+query+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove"

 HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36','Accept-Language':'en-us, en; q=0.5'})

 webpage = requests.get(URL,headers = HEADERS)

 soup = BeautifulSoup(webpage.content,'html.parser')

 a_tag = soup.find_all("a",attrs={"class":"IRpwTa"})

 image_tag = soup.find_all("img", attrs={"class":"_2r_T1I"})

 span_tag = soup.find_all("div", attrs={"class":"_3Ay6Sb"})

 div_tag = soup.find_all("div", attrs={"class":"_3I9_wc"})

 Price = []

 Image = []

 Title = []

 Links = []

 Discount = []

 for i in range(20):

  Title.append(a_tag[i].get("title"))

  Links.append(site+a_tag[i].get("href"))

  Image.append(image_tag[i].get("src"))

  Discount.append(int(span_tag[i].find("span").text[0:2]))

  Price.append(div_tag[i].text)

 df3 = pd.DataFrame({

  'Title':Title,

  'Price':Price,

  'Discount':Discount,

  'Image':Image,

  'Links':Links

 })

 return df3

with concurrent.futures.ThreadPoolExecutor() as executor:

  future1 = executor.submit(ajio, "shirt")
  future2 = executor.submit(bwf, "shirt")
  future3 = executor.submit(flipkart, "shirt")
  df1 = future1.result()
  df2 = future2.result()
  df3 = future3.result()

frames = [df1, df2, df3]

res1 = pd.concat(frames)

main_df = res1.sort_values(by=['Discount'],ascending=False)

main_df = main_df.reset_index(drop=True)

print(main_df)

# file_name = 'MarksData.xlsx'

# main_df.to_excel(file_name)

# print('DataFrame is written to Excel File successfully.')