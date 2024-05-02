from selenium import webdriver

from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import pandas as pd

import time

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

  Site = []

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
      Site.append("Bewakoof")

  df2 = pd.DataFrame({

  'Title':Title,

  'Price':Price,

  'Discount':Discount,

  'Image':Image,

  'Links':Links,

  'Site': Site

  })

  driver.quit()

  return df2
