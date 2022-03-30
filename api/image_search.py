import random
from urllib.parse import quote
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession

class ImageSearch:

  async def get_image(self, term):
    import nest_asyncio
    nest_asyncio.apply()

    # Run JavaScript code on webpage
    session = AsyncHTMLSession()
    resp = await session.get('https://www.irasutoya.com/search?q=' + quote(term))    
    await resp.html.arender()

    soup = BeautifulSoup(resp.html.html, "lxml")
    
    images = soup.select(".boxim img", limit=10)
    print(images)

    image = random.choice(images)
    return image['src'] 