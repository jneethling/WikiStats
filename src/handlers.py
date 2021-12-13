import json
import sqlite3
import threading
from websocket import create_connection

class CustomHandler:

    def __init__(self):

        self.db = sqlite3.connect('./data/wiki_statsDB', check_same_thread=False)
        self.cursor = self.db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stats(\
            id INTEGER PRIMARY KEY,\
            country_name TEXT,\
            change_size INTEGER)''')
        self.db.commit()

        self.ws = None
        self.setStatus(True, 'Function handler on standby')
        self.working = False
        self.counter = 0

    def worker(self, stop_event):
 
        while not stop_event.is_set():
            result = self.ws.recv()
            country = None
            if "geo_ip" in result:
                j_dict = json.loads(result)
                geo = j_dict.get("geo_ip")
                country = geo.get("country_name")
                change = j_dict.get("change_size")
                if change is None:
                    change = 0

            if country is not None:
                self.cursor.execute('''INSERT INTO stats(country_name, change_size) VALUES(?,?)''', (country, change))
                self.db.commit()
                self.counter += 1

    def setStatus(self, status, msg):

        self.status = status
        self.message = msg

    def getStatus(self):
        
        msg = {"Status": self.status, "Message": self.message, "Working in background": self.working, "Records in session": self.counter}
        return msg

    def getTotals(self):

        data = {}
        self.cursor.execute('''SELECT country_name, SUM(change_size) FROM stats GROUP BY country_name''')
        for row in self.cursor:
            data[row[0]] = row[1]
        msg = json.dumps(data)
        return msg

    def getCounts(self):

        data = {}
        self.cursor.execute('''SELECT country_name, COUNT(country_name) FROM stats GROUP BY country_name''')
        for row in self.cursor:
            data[row[0]] = row[1]
        msg = json.dumps(data)
        return msg

    def stopWork(self):

        self.ws.close
        self.working = False
        self.kill_switch.set()
        self.t.join()
        self.setStatus(True, 'Function handler on standby')
        msg = 'Function handler background work stopped'
        return {'message': msg}

    def startWork(self):

        if self.working:
            msg = 'Function handler already working in background, ignoring request'
            return {"message": msg}

        else:
            self.ws = create_connection("ws://wikimon.hatnote.com:9000")
            self.working = True
            self.setStatus(True, 'Function handler working in background')
            self.kill_switch = threading.Event()
            self.t = threading.Thread(target=self.worker, args=(self.kill_switch,))
            self.t.start()

        msg = {"Number of records ingested in this session": self.counter}
        return msg