from bs4 import BeautifulSoup
import requests
import pandas as pd


def flipkart(query):

 site = "https://www.flipkart.com"

 URL = "https://www.flipkart.com/search?q="+query+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove"

 HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36','Accept-Language':'en-us, en; q=0.5'})

 webpage = requests.get(URL,headers = HEADERS)

 soup = BeautifulSoup(webpage.content,'html.parser')

 a_tag = soup.find_all("a",attrs={"class":"IRpwTa"})

 image_tag = soup.find_all("img", attrs={"class":"_2r_T1I"})

 span_tag = soup.find_all("div", attrs={"class":"_3Ay6Sb"})

 div_tag = soup.find_all("div", attrs={"class":"_30jeq3"})

 Price = []

 Image = []

 Title = []

 Links = []

 Discount = []

 Site = []

 for i in range(20):

  Title.append(a_tag[i].get("title"))

  Links.append(site+a_tag[i].get("href"))

  Image.append(image_tag[i].get("src"))

  Discount.append(int(span_tag[i].find("span").text[0:2]))

  Price.append(div_tag[i].text)

  Site.append("Flipkart")

 df3 = pd.DataFrame({

  'Title':Title,

  'Price':Price,

  'Discount':Discount,

  'Image':Image,

  'Links':Links,

  'Site':Site

 })

 return df3
