import urllib.request
from random import randint
import re
from constants import *


def web():
    request = urllib.request.Request(SITE, headers=HEADER)
    page = urllib.request.urlopen(request)
    html = page.read()
    pat = re.compile(rb'<img [^>]*src="([^"]+)')
    img = pat.findall(html)
    url = img[randint(0, len(img))].decode("utf-8")
    return url
