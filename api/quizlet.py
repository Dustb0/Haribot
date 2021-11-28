import urllib.request
import random
from urllib.error import HTTPError
from bs4 import BeautifulSoup


class QuizletApi:

  def get_vocabulary(self, url):
    list = []
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
      with urllib.request.urlopen(req) as response:
        page = response.read()        
        soup = BeautifulSoup(page, "html.parser")

        for quizCard in soup.select(".SetPageTerms-term"):
          terms = quizCard.select(".TermText")
          deWord = terms[0].getText()
          jpWord = terms[1].getText()
          list.append((jpWord, deWord))

        random.shuffle(list)
        return list

    except HTTPError as httpError:
      if httpError.code == 404:
          return list
      else: 
          raise httpError      