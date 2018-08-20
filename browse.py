import urllib.request
from random import randint
import re

site = 'https://www.google.com/search?tbm=isch&q=cat'
hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
        'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
req = urllib.request.Request(site, headers=hdr)
page = urllib.request.urlopen(req)
html = page.read()
pat = re.compile(rb'<img [^>]*src="([^"]+)')
img = pat.findall(html)
# content = page.read()
url = img[randint(0, len(img))].decode("utf-8")
