# Bach
Bach (Batch Asynchronous Client for HTTP) performs batch HTTP requests asynchronously. For Python 3.4 or more recent, since it relies on the standard library `asyncio` module (if unfamiliar, [see the docs](https://docs.python.org/3.4/library/asyncio.html)). Also uses the asynchronous HTTP client functionality in the third-party module `aiohttp`. The `aiohttp`[github page](http://aiohttp.readthedocs.io/en/stable/) has a crawler in their example code from which I got a bit of guidance for this project.

## Usage

### Handler

The `Client` class performs asynchronous HTTP requests but does not contain logic to analyze the returned responses. Instead, the `Client` must be instantiated with a `Handler` object, whose only requirement be that it implements a `handle` method. This method accepts a url and its html response and returns a Boolean indicating success or failure of the processing. 

```
class Handler(object):
    # .....

    def handle(self, url, html):
        ## Does stuff ###
        return success_status
```
Besides determining `success_status`, the other "stuff" done in `handle` can be whatever you want, parsing the page for info, saving to file, etc.

### Sample code

In the following sample code, we drive the `Crawler` with a simple dummy class for a scraper. We pass in a handful of urls to crawl initially and the scraper doesn't do anything with the html responses. It does, however, return a list of urls to crawl next. It's always the same urls, but the `Crawler` will only crawl them the first time they are seen.

```
import asyncio

from ananzi.crawler import Crawler

class DummyScraper(object):
    def __init__(self):
        pass

    def process(self, url, html):
        print("Processing: " + url)
        return (True, ['http://cnn.com', 
                       'http://www.hockeybuzz.com'])
        
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
```