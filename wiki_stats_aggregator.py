"""This application makes a web socket connection to a service supplying
    statistics relating to Wikipedia.  It continues to receive data
    from the socket until it has added 10 usable records to the database.
    The records of interest are the ones that contains some geo_ip data.
    Once the 10 records are committed to the database the API service
    is ready for use.

    The API exposes 2 endpoints:
    /totals - Total number of characters edited by country
    /counts - Count of edit sessions by country

    The app will harvest 10 samples for the database
    each time it is run, meaning that the available data will grow with
    each run unless the database is deleted between runs.
"""

import tornado.ioloop
import tornado.web
import json
import sqlite3
from websocket import create_connection

db = sqlite3.connect('wiki_statsDB')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS stats(\
    id INTEGER PRIMARY KEY,\
    country_name TEXT,\
    change_size INTEGER)''')
db.commit()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = {"message": "Welcome to my Wikipedia stats aggregator"}
        self.write(json.dumps(data))


class TotalsHandler(tornado.web.RequestHandler):
    def get(self):
        data = {}
        cursor.execute('''SELECT country_name, SUM(change_size) FROM stats GROUP BY country_name''')
        for row in cursor:
            data[row[0]] = row[1]
        self.write(json.dumps(data))


class CountHandler(tornado.web.RequestHandler):
    def get(self):
        data = {}
        cursor.execute('''SELECT country_name, COUNT(country_name) FROM stats GROUP BY country_name''')
        for row in cursor:
            data[row[0]] = row[1]
        self.write(json.dumps(data))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/totals", TotalsHandler),
        (r"/counts", CountHandler),
    ])


if __name__ == "__main__":

    print("Initializing the service...")
    ws = create_connection("ws://wikimon.hatnote.com:9000")
    counter = 0

    while counter < 10:

        print("Receiving sample data (looking for 10 usable records)...")
        result = ws.recv()

        if "geo_ip" in result:
            j_dict = json.loads(result)
            geo = j_dict.get("geo_ip")
            country = geo.get("country_name")
            change = j_dict.get("change_size")
            if change is None:
                change = 0

            if country is not None:
                print("Writing to database (record {} of 10)...".format(str(counter + 1)))
                cursor.execute('''INSERT INTO stats(country_name, change_size) VALUES(?,?)''', (country, change))
                db.commit()
                counter += 1

    ws.close()
    app = make_app()
    app.listen(8888)
    print("Service is ready!")
    tornado.ioloop.IOLoop.current().start()
