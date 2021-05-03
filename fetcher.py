import hashlib
import datetime

from enum import IntEnum

import requests

from parser import ResponseJsonParser, Parsed


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

    FILTERS_TEMPLATE = dict(
        name="", nameStartsWith="", comics="", series="", events="", stories=""
    )

    def __init__(self, config):
        self._config = config

    @staticmethod
    def make_request_(address, route, private_key, public_key, **kwargs):
        ts = int(datetime.datetime.now().timestamp())
        digest = hashlib.md5(
            f"{ts}{private_key}{public_key}".encode("utf-8")
        ).hexdigest()
        params = dict(ts=ts, apikey=public_key, hash=digest)

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
            raise Exception(
                f"""
Response ended with status code {response.status_code},
response.text is {response.text}
"""
            )
        return parsed

    def get_feature_by_name(self, route, name, limit=100, offset=0):
        return self.list_features(route, name=name, limit=limit, offset=offset)

    def get_feature_by_name_starts_with(
        self, route, name_starts_with, limit=100, offset=0
    ):
        return self.list_features(
            route, nameStartsWith=name_starts_with, limit=limit, offset=offset,
        )

    def get_feature_by_title(self, route, title, limit=100, offset=0):
        return self.list_features(
            route, title=title, limit=limit, offset=offset
        )

    def get_feature_by_title_starts_with(
        self, route, title_starts_with, limit=100, offset=0
    ):
        return self.list_features(
            route,
            titleStartsWith=title_starts_with,
            limit=limit,
            offset=offset,
        )

    def get_feature_from_year(self, route, start_year, limit=100, offset=0):
        return self.list_features(
            route, startYear=start_year, limit=limit, offset=offset,
        )
