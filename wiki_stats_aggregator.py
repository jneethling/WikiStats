import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = {"message": "Welcome to my Wikipedia stats aggregator"}
        self.write(json.dumps(data))


class TotalsHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO
        self.write("This should give a json response with totals by country")


class CountHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO
        self.write("This should give a json response with count of country")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/totals", TotalsHandler),
        (r"/counts", CountHandler),
    ])


if __name__ == "__main__":

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
