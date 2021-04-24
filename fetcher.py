import hashlib
import datetime

from enum import IntEnum

import requests

import custom_types as ct


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

    def list_features(self, route, parser, **kwargs):
        response = self.make_request(route, **kwargs)
        features = []
        if response.status_code == 200:
            r_json: ct.ResponseJSON = response.json()
            features = parser(r_json)
            for feature in features:
                print(feature)
        else:
            print(
                f"""
    Response ended with status code {response.status_code},
    response.text is {response.text}
    """
            )
        return features

    def get_feature_by_name(self, route, parser, name, limit=100, offset=0):
        return self.list_features(
            route, parser, name=name, limit=limit, offset=offset
        )

    def get_feature_by_name_starts_with(
        self, route, parser, name_starts_with, limit=100, offset=0
    ):
        return self.list_features(
            route,
            parser,
            nameStartsWith=name_starts_with,
            limit=limit,
            offset=offset,
        )

    def get_feature_by_title(self, route, parser, title, limit=100, offset=0):
        return self.list_features(
            route, parser, title=title, limit=limit, offset=offset
        )

    def get_feature_by_title_starts_with(
        self, route, parser, title_starts_with, limit=100, offset=0
    ):
        return self.list_features(
            route,
            parser,
            titleStartsWith=title_starts_with,
            limit=limit,
            offset=offset,
        )

    def get_feature_from_year(
        self, route, parser, start_year, limit=100, offset=0
    ):
        return self.list_features(
            route, parser, startYear=start_year, limit=limit, offset=offset,
        )
