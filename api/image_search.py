import urllib.request
import random
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class ImageSearch:

  def get_image(self, term):
    url = 'https://www.shutterstock.com/de/search/' + quote(term) + '?image_type=photo'

    req = urllib.request.Request(url, headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
      'sec-ch-ua-platform': "Windows",
      'sec-ch-ua-platform': "Windows"
      })

    try:
      with urllib.request.urlopen(req) as response:
        page = response.read()        
        soup = BeautifulSoup(page, "html.parser")

        images = soup.select(".jss230 img", limit=10)
        image = random.choice(images)
        return image['src']

    except HTTPError as httpError:
      if httpError.code == 404:
          return None
      else: 
          raise httpError     