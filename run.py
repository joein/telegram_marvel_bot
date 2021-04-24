import os
import hashlib
import datetime
import functools

from typing import List

import requests

from dotenv import load_dotenv

import custom_types as ct


DOTENV_PATH = ".env"
env = load_dotenv(DOTENV_PATH)

PRIVATE_KEY = os.getenv("MARVEL_PRIVATE_KEY")
PUBLIC_KEY = os.getenv("MARVEL_PUBLIC_KEY")

ADDRESS = "gateway.marvel.com:443"
CHARACTER_ROUTE = "characters"
COMICS_ROUTE = "comics"
EVENTS_ROUTE = "events"
SERIES_ROUTE = "series"


class Character:
    def __init__(
        self,
        _id,
        name,
        description,
        img_link,
        collections,
        detail,
        wiki,
        comic,
        resource_uri,
    ):
        self._id = _id
        self.name = name
        self.description = description
        self.img_link = img_link
        self.detail: ct.UrlInfo = detail
        self.wiki: ct.UrlInfo = wiki
        self.comic: ct.UrlInfo = comic
        self.collections: ct.Collections = collections

        self._resource_uri = resource_uri

    def __repr__(self):
        return f"Character(name: {self.name}, _id: {self._id}, _resource_uri: {self._resource_uri})"


class Comic:
    def __init__(
        self,
        _id,
        # title,
        # description,
        # img_link,
        # collections,
        # detail,
        # wiki,
        # comic,
        # resource_uri,
    ):
        self._id = _id
        # self.name = title
        # self.description = description
        # self.img_link = img_link
        # self.detail: UrlInfo = detail
        # self.wiki: UrlInfo = wiki
        # self.comic: UrlInfo = comic
        # self.collections: Collections = collections
        #
        # self._resource_uri = resource_uri

    def __repr__(self):
        return f"Comic()"


class Event:
    def __init__(self):
        pass

    def __repr__(self):
        return f"Event()"


class Series_:
    def __init__(self):
        pass

    def __repr__(self):
        return f"Series()"


filters = dict(
    name="", nameStartsWith="", comics="", series="", events="", stories=""
)


def make_request(address, route, private_key, public_key, **kwargs):
    ts = int(datetime.datetime.now().timestamp())
    digest = hashlib.md5(
        f"{ts}{private_key}{public_key}".encode("utf-8")
    ).hexdigest()
    params = dict(ts=ts, apikey=public_key, hash=digest)

    query = f"https://{address}/v1/public/{route}"

    params.update(kwargs)
    response = requests.get(query, params=params)
    return response


prepared_request = functools.partial(
    make_request,
    address=ADDRESS,
    private_key=PRIVATE_KEY,
    public_key=PUBLIC_KEY,
)


def list_features(route, parser, **kwargs):
    response = prepared_request(route, **kwargs)
    features = []
    if response.status_code == 20:
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


def get_feature_by_name(
    route, parser, name="", name_starts_with="",
):
    params = dict()
    if name:
        params["name"] = name
    elif name_starts_with:
        params["nameStartsWith"] = name_starts_with
    else:
        raise Exception("name OR name_starts_with params should be set")

    features = list_features(route, parser, **params)
    return features


def get_feature_by_title(
    route, parser, title="", title_starts_with="",
):
    params = dict()
    if title:
        params["title"] = title
    elif title_starts_with:
        params["titleStartsWith"] = title_starts_with
    else:
        raise Exception("title OR title_starts_with params should be set")

    features = list_features(route, parser, **params)
    return features


def get_event_by_name(
    address,
    events_route,
    private_key,
    public_key,
    name="",
    name_starts_with="",
    limit=1,
    offset=0,
):
    params = dict(limit=limit, offset=offset)
    if name:
        params["name"] = name
    elif name_starts_with:
        params["nameStartsWith"] = name_starts_with

    if params:
        events = list_events(
            address, events_route, private_key, public_key, **params
        )
        return events
    else:
        raise Exception("title or title_starts_with must be set")


def list_series(address, series_route, private_key, public_key, **kwargs):
    response = make_request(
        address, series_route, private_key, public_key, **kwargs
    )
    series = []
    if response.status_code == 200:
        r_json: ct.ResponseJSON = response.json()
        series = ResponseJsonParser.parse_list_series(r_json)
        for ser in series:
            print(ser)
    else:
        print(
            f"Response ended with status code {response.status_code}, response.text is {response.text}"
        )
    return series


def get_series_by_title(
    address,
    series_route,
    private_key,
    public_key,
    title="",
    title_starts_with="",
    limit=1,
    offset=0,
):
    params = dict(limit=limit, offset=offset)
    if title:
        params["title"] = title
    elif title_starts_with:
        params["titleStartsWith"] = title_starts_with

    if params:
        series = list_comics(
            address, series_route, private_key, public_key, **params
        )
        return series
    else:
        raise Exception("title or title_starts_with must be set")


def get_series_from_year(
    address,
    series_route,
    private_key,
    public_key,
    start_year,
    title="",
    title_starts_with="",
    limit=1,
    offset=0,
):
    params = dict(startYear=start_year, limit=limit, offset=offset)
    if title:
        params["title"] = title
    elif title_starts_with:
        params["titleStartsWith"] = title_starts_with

    comics = list_comics(
        address, series_route, private_key, public_key, **params
    )
    return comics


class ResponseJsonParser:
    @staticmethod
    def parse_list_characters(response_json) -> List[Character]:
        data: ct.Data = response_json["data"]
        characters = list()

        for result in data["results"]:
            _id = result["id"]
            name = result["name"]
            description = result.get("description", "")
            thumbnail: ct.Thumbnail = result.get(
                "thumbnail", ct.Thumbnail(path="", extension="")
            )
            print(result)
            resource_uri = result.get("resourceURI", "")

            comics: List[ct.Comics] = result.get("comics", [])
            events: List[ct.Event] = result.get("events", [])
            stories: List[ct.Story] = result.get("stories", [])
            series: List[ct.Series] = result.get("series", [])

            detail = ct.UrlInfo(type="", url="")
            wiki = ct.UrlInfo(type="", url="")
            comic = ct.UrlInfo(type="", url="")
            public_links = dict(detail=detail, wiki=wiki, comiclink=comic)
            for url_info in result.get("urls", []):
                _type = url_info["type"]
                url = url_info["url"]
                public_link = public_links[_type]
                public_link["type"] = _type
                public_link["url"] = url

            collections = ct.Collections(
                comics=comics, events=events, stories=stories, series=series
            )

            img_link = f"{thumbnail['path']}{thumbnail['extension']}"

            characters.append(
                Character(
                    _id,
                    name,
                    description,
                    img_link,
                    collections,
                    detail,
                    wiki,
                    comic,
                    resource_uri,
                )
            )
        return characters

    @staticmethod
    def parse_list_comics(response_json) -> List[Comic]:
        comics = []
        print(response_json)
        return comics

    @staticmethod
    def parse_list_events(response_json) -> List[Event]:
        events = []
        print(response_json)
        return events

    @staticmethod
    def parse_list_series(response_json) -> List[Series]:
        series = []
        print(response_json)
        return series


# list_characters(ADDRESS, CHARACTER_ROUTE, PRIVATE_KEY, PUBLIC_KEY, limit=4)
# list_comics(ADDRESS, COMICS_ROUTE, PRIVATE_KEY, PUBLIC_KEY, limit=2)
list_events(ADDRESS, COMICS_ROUTE, PRIVATE_KEY, PUBLIC_KEY, limit=2)
# list_series(ADDRESS, COMICS_ROUTE, PRIVATE_KEY, PUBLIC_KEY, limit=2)
