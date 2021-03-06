import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from enum import Enum, auto

class Conjugations(Enum):
    PLAIN_NONPAST = auto()
    PLAIN_NEGATIVE = auto()
    PLAIN_PAST = auto()
    PLAIN_PAST_NEGATIVE = auto()
    PLAIN_TE = auto()
    PLAIN_TAI = auto()
    KEIGO_NONPAST = auto()
    KEIGO_NEGATIVE = auto()
    KEIGO_PAST = auto()
    KEIGO_PAST_NEGATIVE = auto()
    KEIGO_TE = auto()
    KEIGO_TAI = auto()

class JishoApi:

    def get_audio_file(self, word):
        word = word.split(",")[0]
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

    def get_conjugations(self, word):
        word = word.split(",")[0]
        conjugations = {}
        req = urllib.request.Request("https://www.japandict.com/" + quote(word), headers={'User-Agent': 'Mozilla/5.0'})

        try:
            with urllib.request.urlopen(req) as response:
                page = response.read()        
                soup = BeautifulSoup(page, "html.parser")

                # Check if there's a heading with verb conjugations
                isVerb = False
                for heading in soup.select(".pt-5"):
                    if "verb" in heading.getText().lower():
                        isVerb = True
                        break
                
                if not isVerb:
                    return conjugations

                # Search for conjugation info
                inflectionRows = soup.select(".col-12 .card-body .col-lg-6 tr:not(.bg-gray-200)")

                if inflectionRows is None:
                    return conjugations

                # Gather inflections: Non-keigo
                conjugations[Conjugations.PLAIN_NONPAST] = inflectionRows[0].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_NEGATIVE] = inflectionRows[1].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_PAST] = inflectionRows[2].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_PAST_NEGATIVE] = inflectionRows[3].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_TE] = inflectionRows[4].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_TAI] = inflectionRows[5].select_one('.ps-3').getText()

                # Gather inflections: Keigo
                conjugations[Conjugations.KEIGO_NONPAST] = inflectionRows[13].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_NEGATIVE] = inflectionRows[14].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_PAST] = inflectionRows[15].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_PAST_NEGATIVE] = inflectionRows[16].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_TE] = inflectionRows[17].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_TAI] = inflectionRows[18].select_one('.ps-3').getText()

        except HTTPError as httpError:
            if httpError.code == 404:
                return ""
            else: 
                raise httpError

        return conjugations            

    def get_declensions(self, word):
        word = word.split(",")[0]
        conjugations = {}
        req = urllib.request.Request("https://www.japandict.com/" + quote(word), headers={'User-Agent': 'Mozilla/5.0'})

        try:
            with urllib.request.urlopen(req) as response:
                page = response.read()        
                soup = BeautifulSoup(page, "html.parser")

                # Check if there's a heading with adjective
                isAdjective = False
                for heading in soup.select(".pt-5"):
                    if "adjective " in heading.getText().lower():
                        isAdjective = True
                        break
                
                if not isAdjective:
                    return conjugations

                # Search for conjugation info
                inflectionRows = soup.select(".col-12 .card-body .col-lg-6 tr:not(.bg-gray-200)")

                if inflectionRows is None:
                    return conjugations

                # Gather inflections: Non-keigo
                conjugations[Conjugations.PLAIN_NONPAST] = inflectionRows[0].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_NEGATIVE] = inflectionRows[1].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_PAST] = inflectionRows[2].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_PAST_NEGATIVE] = inflectionRows[3].select_one('.ps-3').getText()
                conjugations[Conjugations.PLAIN_TE] = inflectionRows[4].select_one('.ps-3').getText()

                # Gather inflections: Keigo
                conjugations[Conjugations.KEIGO_NONPAST] = inflectionRows[6].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_NEGATIVE] = inflectionRows[7].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_PAST] = inflectionRows[8].select_one('.ps-3').getText()
                conjugations[Conjugations.KEIGO_PAST_NEGATIVE] = inflectionRows[9].select_one('.ps-3').getText()

        except HTTPError as httpError:
            if httpError.code == 404:
                return ""
            else: 
                raise httpError

        return conjugations

    def get_example_sentence(self, word):
        req = urllib.request.Request("https://jisho.org/word/" + quote(word))

        try:
            with urllib.request.urlopen(req) as response:
                page = response.read()        
                soup = BeautifulSoup(page, "html.parser")

                # Grab first example sentence
                sentenceElem = soup.find("div", {"class": "sentence"})
                
                if sentenceElem is None:
                    return None

                # Find kana part without furigana
                kanaElements = sentenceElem.select("span.unlinked")
                kanaText = ""
                for elem in kanaElements:
                    kanaText += elem.getText()

                # Get translation
                enText = sentenceElem.select_one("li.english").getText()
                return (kanaText, enText)
                

        except HTTPError as httpError:
            if httpError.code == 404:
                return ""
            else: 
                raise httpError

        return "" 

    def get_reading(self, word):
        word = word.split(",")[0]
        req = urllib.request.Request("https://www.japandict.com/" + quote(word), headers={'User-Agent': 'Mozilla/5.0'})

        try:
            with urllib.request.urlopen(req) as response:
                page = response.read()        
                soup = BeautifulSoup(page, "html.parser")    

                # Find reading
                readingElem = soup.find("div", {"class": "xxsmall text-muted text-center mt-2"})

                if readingElem is None:
                    return None

                return readingElem.getText().strip()

        except HTTPError as httpError:
            if httpError.code == 404:
                return None
            else: 
                raise httpError                