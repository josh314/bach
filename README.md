# Ananzi
Asynchronous web crawler. For Python 3.4 or more recent, since it relies on the standard library `asyncio` module (if unfamiliar, [see the docs](https://docs.python.org/3.4/library/asyncio.html)). Also uses the asynchronous HTTP client functionality in the third-party module `aiohttp`. The `aiohttp`[github page](https://docs.python.org/3.4/library/asyncio.html) has a crawler in their example code from which I got a bit of guidance for this project.

## Usage

### Scraper

The `Crawler` class performs asynchronous web crawling but does not analyze the returned responses nor determine which new urls (if any) should be added to the crawling queue. Instead, the Crawler must be instantiated with a `Scraper` object, whose only requirement be that it implements a `process` method. This method accepts a url and its html response and returns a tuple containing a Boolean indicating success or failure of the scraping, and a list of target urls for the `Crawler` to scrape next (these could be outgoing links on the scraped page, but don't have to be). 

```
class Scraper(object):
    # .....

    def process(self, url, html):
        ## Does stuff ###
        return (success, target_urls)
```
Besides determining `success` and `target_urls`, the other "stuff" done in `process` can be whatever you want, parsing the page for info, saving to file, etc.

### Crawl order

The traversal order of the `Crawler` can be controlled with the `traversal` argument, which accepts the string values `'depth-first'` and `'breadth-first'` (the default). Newly discovered pages are added to the back of the crawling queue for breadth-first traversal, and to the front of the queue for depth-first traversal. This is similar to the graph traversal algorithms [BFS](http://wikipedia.org/wiki/Breadth-first_search) and [DFS](http://wikipedia.org/wiki/Depth-first_search).
Note that while the order of scheduling tasks can be set deterministically, the asynchronous nature of the crawler doesn't provide any guarantees on the order in which the tasks finish. Therefore, these crawling schemes do not truly implement the BFS or DFS algorithms, but are qualitatively similar.

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