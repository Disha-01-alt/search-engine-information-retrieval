import requests
from bs4 import BeautifulSoup
import sys

def get_words(text):
    text = text.lower()
    for ch in text:
        if not ch.isalnum():
            text = text.replace(ch, " ")
    return text.split()

def word_frequency(words):
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq

def get_hash(word):
    p = 53
    m = 2**64
    h = 0
    for i, char in enumerate(word):
        h = (h + ord(char) * (p**i)) % m
    return h

def get_simhash(freq):
    v = [0] * 64
    for word, weight in freq.items():
        whash = get_hash(word)
        for i in range(64):
            if (whash >> i) & 1:
                v[i] += weight
            else:
                v[i] -= weight
    
    sim = 0
    for i in range(64):
        if v[i] > 0:
            sim |= (1 << i)
    return sim

def scrape_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  
    
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.title.get_text(strip=True) if soup.title else "No Title"
    print(title)
    
    if soup.body:
        print(soup.body.get_text(strip=True))
    else:
        print("")
        
    for link in soup.find_all('a', href=True):
        print(link['href'])

def compare_urls(url1, url2):
    def fetch_body(url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.body.get_text() if soup.body else ""
        except:
            return ""

    text1 = fetch_body(url1)
    text2 = fetch_body(url2)
    
    words1 = get_words(text1)
    words2 = get_words(text2)
    
    freq1 = word_frequency(words1)
    freq2 = word_frequency(words2)
    
    sim1 = get_simhash(freq1)
    sim2 = get_simhash(freq2)
    
    xor_val = sim1 ^ sim2
    diff = bin(xor_val).count('1')
    common = 64 - diff
    
    print(f"Simhash 1: {sim1}")
    print(f"Simhash 2: {sim2}")
    print(f"Common bits: {common}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        scrape_url(sys.argv[1])
    elif len(sys.argv) == 3:
        compare_urls(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python scraper.py <URL> or python scraper.py <URL1> <URL2>")
