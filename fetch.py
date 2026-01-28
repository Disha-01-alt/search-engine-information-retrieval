'''Python Project
Write a python program that takes a URL on the command line, fetches the page, and outputs (one per line)
Page Title (without any HTML tags)
Page Body (just the text, without any html tags)
All the URLs that the page points/links to'''

from bs4 import BeautifulSoup
import sys
import requests
url=input("Enter the url")
response=requests.get(url)
# print(response.content)
soup=BeautifulSoup(response.content,'html.parser')
print("Page Title\n",soup.title.text)
print("Page Body\n",soup.body.get_text(strip=True))
print("\nAll URLs:")
for link in soup.find_all('a',href=True):
  print(link['href'])