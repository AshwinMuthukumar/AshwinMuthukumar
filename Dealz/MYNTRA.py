from selenium import webdriver

import pandas as pd

import time

from bs4 import BeautifulSoup

import re


def myntra(var):
  options = webdriver.ChromeOptions()

  options.add_argument("--headless")

  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

  driver = webdriver.Chrome(options=options)

  driver.get("https://www.myntra.com/rawQuery="+var)

  driver.implicitly_wait(5)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  time.sleep(1)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

  time.sleep(1)

  driver.execute_script("window.scrollTo(0, 0);")

  time.sleep(1)

  html = driver.page_source

  soup = BeautifulSoup(html, "html.parser")

  products = soup.find_all("li",attrs={"class":"product-base"})

  Image = []

  Title = []

  Price = []

  Discount = []

  Links = []

  Site = []

  for i in products:

      image_tag = i.find("img",attrs={"class":"img-responsive"})
      price_tag = i.find("span",attrs={"class":"product-discountedPrice"})

      if image_tag and price_tag:

          Image.append(image_tag.get("src"))
          Price.append(price_tag.text)


          title_tag = i.find("h4",attrs={"class":"product-product"})
          if title_tag:
              Title.append(title_tag.text)


          discount_tag = i.find("span",attrs={"class":"product-discountPercentage"})
          if discount_tag:
              Discount_int = re.findall('\d+',discount_tag.text)
              Discount.append(int(Discount_int[0]))
      
          Links.append("https://www.myntra.com/"+i.find("a").get("href"))
          Site.append("Myntra")

  df4 = pd.DataFrame({

    'Title':Title,

    'Price':Price,

    'Discount':Discount,

    'Image':Image,

    'Links':Links,

    'Site':Site

  })
  driver.quit()
  return df4