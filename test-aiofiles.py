import os.path
from urllib.parse import urlparse
import asyncio

import aiofiles

from ananzi.crawler import Crawler

class AiofilesScraper(object):
    def __init__(self,loop,save_dir='.'):
        self.loop = loop
        self.save_dir = save_dir

    @asyncio.coroutine
    def save(self,url,html):
        res = urlparse(url)
        filename = res.netloc + ".html"
        path = os.path.join(self.save_dir, filename)
        f = yield from aiofiles.open(path,'wb')
        try:
            yield from f.write(html)
            print("Saved: " + url)
        finally:
            yield from f.close()
         
    def process(self, url, html):
        print("Processing: " + url)
        asyncio.Task(self.save(url, html))
        return (True, ['http://cnn.com', 'http://www.hockeybuzz.com'])
        
urls = [
    'http://www.google.com',
    'http://www.wikipedia.org/wiki/Barack_Obama',
    'http://reddit.com',
    'http://area-51-is-real.gov',
    'http://fhqwhgads.com/',#Actually real.
]

loop = asyncio.get_event_loop()
cr = Crawler(loop, AiofilesScraper(loop,save_dir='tmp'))
cr.launch(urls)
print("Successful: {}".format(len(cr.done)))
print("Failed: {}".format(len(cr.failed)))
loop.close()
