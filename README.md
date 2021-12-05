# WikiStatsAggregator
## Summary
A very simple Wikipedia stats aggregator for illustrative purposes written in Python with Tornado

This application makes a web socket connection to a service supplying Wikipedia updates.
The data is added to a database if it contains some 'geo_ip' data for the purpose of serving 
simple statistical aggregations for comparing relative activity levels between different countries.

    The API exposes the following endpoints:
    /start - Starts the aggregation in a worker thread
    /stop - Stop the aggregation thread
    /status - Verify if the worker thread is active and the number of records ingested in the session
    /totals - Total number of characters edited by country
    /counts - Count of edit sessions by country

## TODO
* Improve async test cases
* Create Dockerfile
* Migrate SQLite to PostgreSQL and/or redis
* Implement additional domain profiling
* Implement additional domain analytical endpoints
* Try neo4j
* Maybe migrate this to Flask 2
* ..or even better, Gorilla Mux (Golang)

## Dependencies
Python 3, Websocket-client & Tornado

## Test with pytest
python -m pytest ./tests --cov --cov-report term-missing