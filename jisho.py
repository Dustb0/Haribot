import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class JishoApi:

    def getAudioFile(self, word):
        req = urllib.request.Request("https://jisho.org/word/" + quote(word))

        try:
            with urllib.request.urlopen(req) as response:
                page = response.read()        
                soup = BeautifulSoup(page, "html.parser")

                # Search for audio
                audioElem = soup.find("audio")
                if audioElem is not None:
                    sourceElem = audioElem.find("source")
                    return "https:" + sourceElem["src"]

        except HTTPError as httpError:
            if httpError.code == 404:
                return ""
            else: 
                raise httpError

        return ""


testApi = JishoApi()
print(testApi.getAudioFile("病院"))