[![Python application](https://github.com/jneethling/WikiStats/actions/workflows/python-app.yml/badge.svg)](https://github.com/jneethling/WikiStats/actions/workflows/python-app.yml)

# WikiStatsAggregator
## Summary
A very simple Wikipedia stats aggregator for illustrative purposes written in Python with Tornado

This application makes a web socket connection to the the Hatnote Wikipedia monitor (https://github.com/hatnote/wikimon).
The data is added to a database if it contains some 'geo_ip' data for the purpose of serving 
simple statistical aggregations for comparing relative activity levels between different countries.

    The API exposes the following endpoints:
    /start - Starts the aggregation in a worker thread
    /stop - Stop the aggregation thread
    /status - Verify if the worker thread is active and the number of records ingested in the session
    /totals - Total number of characters edited by country
    /counts - Count of edit sessions by country

## TODO
* Craceful shutdown

## Test with pytest (and pytest-cov plugin)
python -m pytest ./tests --cov --cov-report term-missing

## Build image
docker build -t wiki:latest .

## Run container with data persistance
docker container run -p 5000:5000 -v wikivol:/app/data wiki:latest