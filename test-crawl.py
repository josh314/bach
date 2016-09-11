import asyncio
import logging
logging.basicConfig(level=logging.WARNING)

from ananzi.crawler import Crawler

class DummyScraper(object):
    def __init__(self):
        pass

    def process(self, url, html):
        logging.info("Processed: " + url)
        return (True, ['http://cnn.com', 'http://www.hockeybuzz.com'])
        
urls = [
    'http://www.google.com',
    'http://www.wikipedia.org/wiki/Barack_Obama',
    'http://reddit.com',
    'http://area-51-is-real.gov',
    'http://fhqwhgads.com/',#Actually real.
]

loop = asyncio.get_event_loop()
cr = Crawler(loop, DummyScraper())
cr.launch(urls)
print("Successful: {}".format(len(cr.done)))
print("Failed: {}".format(len(cr.failed)))
loop.close()
