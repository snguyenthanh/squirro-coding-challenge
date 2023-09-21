from collections.abc import Iterable
import logging
from typing import Generator, Optional

from httpx import Client, Request
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    before_sleep_log,
)


logger = logging.getLogger(__name__)


class HTTPClient:
    """
    A class method holds a HTTP connection pooling.
    """

    _HTTPX_CLIENT: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._HTTPX_CLIENT:
            return cls._HTTPX_CLIENT

        cls._HTTPX_CLIENT = Client()
        return cls._HTTPX_CLIENT

    @classmethod
    def close(cls, client) -> None:
        if cls._HTTPX_CLIENT:
            cls._HTTPX_CLIENT.close()

    @classmethod
    @retry(
        reraise=True,
        wait=wait_random_exponential(multiplier=1, min=60, max=75),
        stop=stop_after_attempt(3),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def request(
        cls,
        method: str,
        url: str,
        *args,
        **kwargs,
    ) -> Optional[dict]:
        """
        For all supported arguments: https://www.python-httpx.org/api/#request
        """
        request = Request(method=method, url=url, *args, **kwargs)
        response = cls.get_client().send(request)
        response.raise_for_status()

        return response.json()

    @classmethod
    def requests(
        cls,
        method: str,
        url: str,
        params_iter: Iterable[dict],
        *args,
        **kwargs,
    ) -> Generator:
        """
        For all supported arguments: https://www.python-httpx.org/api/#request
        """
        for params in params_iter:
            yield cls.request(method=method, url=url, params=params, *args, **kwargs)
