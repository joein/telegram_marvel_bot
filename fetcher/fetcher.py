import hashlib
import datetime

from enum import IntEnum

import requests

from fetcher.parser import ResponseJsonParser
from fetcher.exceptions import FetcherException


class Route(IntEnum):
    CHARACTERS = 0
    COMICS = 1
    EVENTS = 2
    SERIES = 3


class Fetcher:
    ADDRESS = "gateway.marvel.com:443"
    ROUTES = {
        Route.CHARACTERS: "characters",
        Route.COMICS: "comics",
        Route.EVENTS: "events",
        Route.SERIES: "series",
    }
    LIST_PARSERS = {
        Route.CHARACTERS: ResponseJsonParser.parse_list_characters,
        Route.COMICS: ResponseJsonParser.parse_list_comics,
        Route.EVENTS: ResponseJsonParser.parse_list_events,
        Route.SERIES: ResponseJsonParser.parse_list_series,
    }

    def __init__(self, config):
        self._config = config

    @staticmethod
    def make_request_(address, route, private_key, public_key, **kwargs):
        ts = int(datetime.datetime.now().timestamp())
        digest = hashlib.md5(
            f"{ts}{private_key}{public_key}".encode("utf-8")
        ).hexdigest()
        params = {"ts": ts, "apikey": public_key, "hash": digest}

        query = f"https://{address}/v1/public/{route}"

        params.update(kwargs)
        response = requests.get(query, params=params)
        return response

    def make_request(self, route, **kwargs):
        return self.make_request_(
            self.ADDRESS,
            self.ROUTES[route],
            self._config.private_key,
            self._config.public_key,
            **kwargs,
        )

    def list_features(self, route, **kwargs):
        parser = self.LIST_PARSERS[route]

        response = self.make_request(route, **kwargs)
        if response.status_code == 200:
            r_json = response.json()
            parsed = parser(r_json)
        else:
            raise FetcherException(response.status_code, response.text)

        return parsed
