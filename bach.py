import signal
import asyncio
import logging

import aiohttp

class Client(object): 
    def __init__(self, loop, handler, max_connections=30):
        self.loop = loop
        self.handler = handler
        self.sem = asyncio.Semaphore(max_connections)#For preventing accidental DOS
        self.queue = asyncio.PriorityQueue()
        self.processing = set()
        self.done = set()
        self.failed = set()
        self.active = True
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())
        
    def enqueue(self, priority, url):
        if self.active:
            self.queue.put_nowait((priority,url))
        
    @asyncio.coroutine
    def get_html(self,url):
        html = None
        err = None
        self.log.info("Requesting: " + url)
        resp = yield from aiohttp.get(url)
        if resp.status == 200:
            html = yield from resp.read()
        else:
            if resp.status == 404:
                err = aiohtp.web.HTTPNotFound
            else:
                err = aiohttp.HttpProcessingError(
                    code=resp.status, message=resp.reason,
                    headers=resp.headers)
        resp.close()
        if(err):
            raise err
        return html

    @asyncio.coroutine
    def process_page(self, url):
        self.log.info("Processing: " + url)
        self.processing.add(url)
        try:
            with (yield from self.sem):#Limits number of concurrent requests
                html = yield from self.get_html(url)
        except Exception as e:
            self.log.error('Resource not found: ' + url)
            self.failed.add(url)
        else:
             success = self.handler.handle(url, html)
             if success:
                 self.done.add(url)
             else:
                 self.failed.add(url)
        finally:
            self.processing.remove(url)

    @asyncio.coroutine
    def batch_request(self):
        while True:
            try:
                priority, url = yield from asyncio.wait_for(self.queue.get(),5)
                self.loop.create_task(self.process_page(url))
            except asyncio.TimeoutError:
                self.log.info("No more requests.")
                break
        while self.processing:
            self.log.debug("{} tasks still processing.".format(len(self.processing)))
            yield from asyncio.sleep(5)
            

    def launch(self, urls):
        # queue up initial urls 
        for url in urls:
            self.enqueue(*url)
        task = self.loop.create_task(self.batch_request())
        try:
            self.loop.add_signal_handler(signal.SIGINT, self.shutdown)
        except RuntimeError:
            pass

        try:
            self.loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass


    def shutdown(self):
        self.log.warning("Shutdown initiated.")
        self.active = False
        try:
            while True:
                self.queue.get_nowait()
        except asyncio.QueueEmpty:
            pass
        for task in asyncio.Task.all_tasks():
            task.cancel()
