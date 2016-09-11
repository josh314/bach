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
        
urls = [
    (1, 'http://www.google.com'),
    (1, 'http://www.wikipedia.org/wiki/Barack_Obama'),
    (1, 'http://reddit.com'),
    (1, 'http://area-51-exists.gov'),#Not real, for now.
    (1, 'http://fhqwhgads.com/'),#Actually real.
]

loop = asyncio.get_event_loop()
client = bach.Client(loop, DummyHandler())
client.launch(urls)
print("Successful: {}".format(len(client.done)))
print("Failed: {}".format(len(client.failed)))
loop.close()
