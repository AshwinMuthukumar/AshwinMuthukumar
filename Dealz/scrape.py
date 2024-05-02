from bs4 import BeautifulSoup # used to parse html and xml
import pandas as pd # used for dataframe and other features like Data structure
import requests # used for sending requests to server e.g In our case, we are going to scrape amazon so python would send request to amazon
import re # used for string manipulation

search = "playstation 5"
search = search.replace(" ","+")
URL= "https://www.amazon.in/s?k="+search+"&sprefix=pla%2Caps%2C437&ref=nb_sb_ss_ts-doa-p_1_3"

#Header for HTTP Request

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36','Accept-Language':'en-us, en;q=0.5'})

#HTTP Request
webpage = requests.get(URL, headers= HEADERS)
print(webpage)

# 'print(webpage)' to check if we get <Response 200> which means connection successful or else <Response 500> if connection is not successful
# 'print(webpage.content)' would return values in bytes, for converting this into html we use beautifulSoup

# soup = BeautifulSoup(webpage.content,"html.parser")
# links = soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

# print(links)