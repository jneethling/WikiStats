# WikiStatsAggregator
A very simple Wikipedia stats aggregator for illustrative purposes

This application makes a web socket connection to a service supplying
statistics relating to Wikipedia.  It continues to receive data
from the socket until it has added 10 usable records to the database.
The records of interest are the ones that contains some geo_ip data.
Once the 10 records are committed to the database the API service
is ready for use.

The app will harvest 10 samples for the database
each time it is run, meaning that the available data will grow with
each run unless the database is deleted between runs.

    The API exposes 2 endpoints:
    /totals - Total number of characters edited by country
    /counts - Count of edit sessions by country

Dependencies
------------
Python 2.7, Websocket-client & Tornado 