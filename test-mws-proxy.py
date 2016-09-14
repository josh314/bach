import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

import bach

class DummyHandler(object):
    def __init__(self):
        pass

    def handle(self, url, html):
        logging.info("Processed: " + url)
        return True
        
urls = [(1, 'http://localhost:9000/products/search/?q=fart')]*100

loop = asyncio.get_event_loop()
client = bach.Client(loop, DummyHandler(), max_connections=20)
client.launch(urls)
print("Successful: {}".format(len(client.done)))
print("Failed: {}".format(len(client.failed)))
loop.close()
