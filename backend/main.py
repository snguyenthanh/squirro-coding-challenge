import argparse
import logging
from math import ceil
from typing import List, Generator
from httpx import HTTPError

from dateutil.parser import parse as parse_str_to_dt
from http_client import HTTPClient
from parsers import flatten_dict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """

    MAX_LIMIT_PER_QUERY = 1000
    RESULTS_PER_PAGE = 10
    BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    def __init__(self):
        self.http_client = HTTPClient

    def connect(self, inc_column=None, max_inc_value=None):
        logger.debug("Incremental Column: %r", inc_column)
        logger.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        self.http_client.close()

    def _has_more_results(self, resp_json: dict) -> bool:
        return resp_json["response"]["meta"]["hits"] > self.MAX_LIMIT_PER_QUERY

    def _get_total_pages(self, resp_json: dict) -> int:
        return ceil(resp_json["response"]["meta"]["hits"] / self.RESULTS_PER_PAGE)

    def _articles_from_response(self, response: dict) -> List[dict]:
        """Select the articles from responses and join them into an array"""
        return response["response"]["docs"]

    def _repeat_getting_articles(self, extra_params: dict = None) -> List[dict]:
        base_params = {
            "sort": "newest",
            "api-key": self.args.api_key,
            **extra_params,
        }
        end_date = None
        while True:
            if end_date:
                params = {
                    **base_params,
                    "end_date": end_date,
                }
            else:
                params = base_params

            first_resp = self.http_client.request("GET", self.BASE_URL, params=params)
            if not first_resp:
                break

            yield first_resp

            total_pages = self._get_total_pages(first_resp)
            for resp in self.http_client.requests(
                "GET",
                url=self.BASE_URL,
                params_iter=(
                    {**base_params, "page": page_num}
                    for page_num in range(1, total_pages + 1)
                ),
            ):
                yield resp

            if not self._has_more_results(resp):
                break

            end_date_iso = resp["response"]["docs"][-1]["pub_date"]
            end_date = parse_str_to_dt(end_date_iso)

    def getDataBatch(self, batch_size: int) -> Generator[List[dict], None, None]:
        """
        Generator - Get data from source on batches.

        :returns One list for each batch. Each of those is a list of
                 dictionaries with the defined rows.
        """
        extra_params = {
            "q": self.args.query,
            "sort": "newest",
        }
        cur_batch = []
        try:
            for response in self._repeat_getting_articles(
                extra_params=extra_params,
            ):
                next_articles = self._articles_from_response(response)
                for article in next_articles:
                    cur_batch.append(flatten_dict(article))

                    if len(cur_batch) == batch_size:
                        yield cur_batch
                        cur_batch = []

        except HTTPError as exc:
            logger.error(
                "Failed to retrieve more articles. Error message: %s", str(exc)
            )
        except Exception as exc:
            logger.error("Unhandled error. Error message: %s", str(exc))

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """

        schema = [
            "title",
            "body",
            "created_at",
            "id",
            "summary",
            "abstract",
            "keywords",
        ]

        return schema


if __name__ == "__main__":
    config = {
        "api_key": "NYTIMES_API_KEY",
        "query": "Silicon Valley",
    }
    source = NYTimesSource()

    # This looks like an argparse dependency - but the Namespace class is just
    # a simple way to create an object holding attributes.
    source.args = argparse.Namespace(**config)

    for idx, batch in enumerate(source.getDataBatch(10)):
        print(f"{idx} Batch of {len(batch)} items")
        for item in batch:
            print(f"  - {item['_id']} - {item['headline.main']}")
