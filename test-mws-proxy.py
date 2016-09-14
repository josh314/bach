import time
import os.path
from urllib.parse import urlparse

import logging
logging.basicConfig(level=logging.DEBUG)

import asyncio

import bach

class Handler(object):
    def __init__(self, save_dir='.'):
        self.save_dir = save_dir

    def save(self,url,html):
        res = urlparse(url)
        filename = "{}-{}.html".format(res.netloc, time.time())
        path = os.path.join(self.save_dir, filename)
        f = open(path,'wb')
        f.write(html)
        f.close()
         
    def handle(self, url, html):
        logging.info("Processed: " + url)
        self.save(url,html)
        return True
        
urls = [(1, 'http://localhost:9000/products/search/?q=fart')]*100

loop = asyncio.get_event_loop()
client = bach.Client(loop, Handler(save_dir='tmp'), max_connections=20)
client.launch(urls)
print("Successful: {}".format(len(client.done)))
print("Failed: {}".format(len(client.failed)))
loop.close()
