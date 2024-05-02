from selenium import webdriver

from bs4 import BeautifulSoup

import pandas as pd

import time

def ajio(query):

  op = webdriver.ChromeOptions()

  op.add_argument('headless')

  driver = webdriver.Chrome(options=op)

  driver.get('https://www.ajio.com/search/?query=%3Arelevance&text='+query+'&classifier=intent&gridColumns=5')

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

  Site = []

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
      Site.append("Ajio")

  df1 = pd.DataFrame({

  'Title':Title,

  'Price':Price,

  'Discount':Discount,

  'Image':Image,

  'Links':Links,

  'Site': Site

  })

  driver.quit()

  return df1

