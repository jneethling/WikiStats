# WikiStatsAggregator
A very simple Wikipedia stats aggregator for illustrative purposes

This application makes a web socket connection to a service supplying Wikipedia updates.
The data is added to a database if it contains some 'geo_ip' data for the purpose of serving 
simple statistical aggregations for comparing relative activity levels between different countries.

    The API exposes the following endpoints:
    /start - Starts the aggregation in a worker thread
    /stop - Stop the aggregation thread
    /status - Verify if the worker thread is active and the number of records ingested in the session
    /totals - Total number of characters edited by country
    /counts - Count of edit sessions by country

Dependencies
------------
Python 3, Websocket-client & Tornado

Test with pytest
----------------
python -m pytest ./tests --cov --cov-report term-missing