from bs4 import BeautifulSoup
import requests
import sys

if len(sys.argv)!=3:
  raise Exception("Usage: python simhash.py <URL1> <URL2>")

url1=sys.argv[1]
url2=sys.argv[2]

def fetchBody(url):
  raw_response=requests.get(url)
  parsed_soup=BeautifulSoup(raw_response.content, 'html.parser')
  if parsed_soup.body:
    return parsed_soup.body.get_text()
  else:
    return ""
def getWords(text):
  text=text.lower()
  for ch in text:
    if not ch.isalnum():
      text=text.replace(ch, " ")
  words=text.split()
  return words
def wordFrequency(words):
  freq={}
  for w in words:
    if w in freq:
      freq[w]+=1
    else:
      freq[w]=1
  return freq
def getHash(word):
  p = 53
  m = 2**64
  h = 0
  for i in range(len(word)):
      h=(h + ord(word[i])*(p**i))%m
  return h
def getSimhash(freq):
    v= [0] * 64
    for word, weight in freq.items():
        whash= getHash(word)
        for i in range(64):
            if (whash >> i) & 1:
                v[i]+=weight
            else:
                v[i]-=weight
    
    sim= 0
    for i in range(64):
        if v[i] > 0:
            sim |= (1 << i)
    return sim
# fetch text from both URL
text1=fetchBody(url1)
text2=fetchBody(url2)

# words list
words1=getWords(text1)
words2=getWords(text2)

# frequency dictionary
freq1=wordFrequency(words1)
freq2=wordFrequency(words2)

# simhash
sim1=getSimhash(freq1)
sim2=getSimhash(freq2)

# count common bits
xor=sim1^sim2
dif=bin(xor).count('1')
common=64-dif

print("Simhash 1:",sim1)
print("Simhash 2:",sim2)
print("Common bits:",common)
