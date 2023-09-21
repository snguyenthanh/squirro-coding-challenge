# Squirro Backend Challenge

## Requirements

* Python 3.11
* An `API_KEY` for NYTimes

## Implementation details

### main.py

The main script to run the data loader for NYTimes.

The data loader retrieves the articles until all found articles with the query are returned. It does this by going through all `page` (with a limit of 10) for the query, then use the last article's `pub_date` as the `end_date` for the subsequent requests, until no more articles are returned or a rate-limit error is thrown (after exhausting all retries).

### parsers.py

This file only has one function `flatten_dict`, which works with both nested lists and dictionaries.

### http_client.py

A wrapper for HTTPX client to handle retries, logging and batch requests.
