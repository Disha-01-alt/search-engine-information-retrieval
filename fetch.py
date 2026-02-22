'''Python Project
Write a python program that takes a URL on the command line, fetches the page, and outputs (one per line)
Page Title (without any HTML tags)
Page Body (just the text, without any html tags)
All the URLs that the page points/links to'''

from bs4 import BeautifulSoup
import sys
import requests
# to check whether you have passed the URL
if len(sys.argv)!=2:
  raise Exception("Usage: python fetch.py <URL>")
# taking the second argument for URL
url=sys.argv[1]
# request the raw response
raw_response=requests.get(url)
# print(raw_response.content)
# parsed soup
parsed_soup=BeautifulSoup(raw_response.content,'html.parser')
# title
if parsed_soup.title:
  print(parsed_soup.title.get_text(strip=True))
else:
  print()
# body
if parsed_soup.body:
  print(parsed_soup.body.get_text(strip=True))
else:
  print()
# All URLs
for link in parsed_soup.find_all('a',href=True):
  print(link['href'])
