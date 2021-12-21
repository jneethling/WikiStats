import tornado.web
import tornado.ioloop
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4,)

class pingHandler(tornado.web.RequestHandler):

    def get(self):
        
        self.write('pong')
        self.finish()

class memoryHandler(tornado.web.RequestHandler):

    def initialize(self, ref_obj):
        self.ref_obj = ref_obj

    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(executor, self.ref_obj.getMemory)
        self.write(res)

class statusHandler(tornado.web.RequestHandler):

    def initialize(self, ref_obj):       
        self.ref_obj = ref_obj

    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(executor, self.ref_obj.getStatus)
        self.write(res)

class totalsHandler(tornado.web.RequestHandler):

    def initialize(self, ref_obj):        
        self.ref_obj = ref_obj

    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(executor, self.ref_obj.getTotals)
        self.write(res)

class countsHandler(tornado.web.RequestHandler):

    def initialize(self, ref_obj):        
        self.ref_obj = ref_obj

    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(executor, self.ref_obj.getCounts)
        self.write(res)

class startHandler(tornado.web.RequestHandler):

    def initialize(self, ref_obj):       
        self.ref_obj = ref_obj

    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(executor, self.ref_obj.startWork)
        self.write(res)

class stopHandler(tornado.web.RequestHandler):

    def initialize(self, ref_obj):        
        self.ref_obj = ref_obj

    async def get(self):
        res = await tornado.ioloop.IOLoop.current().run_in_executor(executor, self.ref_obj.stopWork)
        self.write(res)

def make_app(c_handler):
    return tornado.web.Application([
                    (r"/ping", pingHandler),
                    (r"/memory", memoryHandler, {"ref_obj": c_handler}),
                    (r"/status", statusHandler, {"ref_obj":c_handler}),
                    (r"/start", startHandler, {"ref_obj":c_handler}),
                    (r"/stop", stopHandler, {"ref_obj":c_handler}),
                    (r"/totals", totalsHandler, {"ref_obj":c_handler}),
                    (r"/counts", countsHandler, {"ref_obj":c_handler})
                    ])

if __name__ == '__main__':

    from handlers import CustomHandler
    c_handler = CustomHandler()
    application = make_app(c_handler)
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()