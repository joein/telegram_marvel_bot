from typing import List

import custom_types as ct

from entities import Creator, Character, Comic, Event, Series


class ResponseJsonParser:
    @staticmethod
    def parse_list_characters(response_json):
        data: ct.Data = response_json["data"]
        count = response_json["data"]["count"]
        total = response_json["data"]["total"]
        characters = list()

        for result in data["results"]:
            _id = result["id"]
            name = result["name"]
            description = (
                desc
                if (desc := result.get("description"))
                else f"Sorry, I did not find description for {name} :("
            )
            thumbnail: ct.Thumbnail = result.get(
                "thumbnail", ct.Thumbnail(path="", extension="")
            )
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
                if _type in public_links:
                    public_link = public_links[_type]
                    public_link["type"] = _type
                    public_link["url"] = url
                else:
                    print(f"CHARACTERS: {_type} not in public_links")

            collections = ct.Collections(
                comics=comics, events=events, stories=stories, series=series
            )

            img_link = f"{thumbnail['path']}.{thumbnail['extension']}"

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
        return Parsed(characters, count, total)

    @staticmethod
    def parse_list_comics(response_json):
        data = response_json["data"]
        count = response_json["data"]["count"]
        total = response_json["data"]["total"]
        comics = list()

        for result in data["results"]:
            _id = result["id"]
            title = result["title"]
            description = result.get("description", "")
            if not description:
                description = result.get("variantDescription", "")
            if not description:
                description = (
                    f"Sorry, I did not found description for {title} :("
                )
            page_count = result["pageCount"]
            thumbnail: ct.Thumbnail = result.get(
                "thumbnail", ct.Thumbnail(path="", extension="")
            )
            resource_uri = result.get("resourceURI", "")

            detail = ct.UrlInfo(type="", url="")
            public_links = dict(detail=detail)
            for url_info in result.get("urls", []):
                _type = url_info["type"]
                url = url_info["url"]
                if _type in public_links:
                    public_link = public_links[_type]
                    public_link["type"] = _type
                    public_link["url"] = url
                else:
                    print(f"COMICS {_type} not in public_links")
            img_link = f"{thumbnail['path']}.{thumbnail['extension']}"

            creators = []
            json_creators = result.get("creators", {})
            for json_creator in json_creators.get("items"):
                creators.append(
                    Creator(
                        json_creator.get("resourceURI"),
                        json_creator.get("name"),
                        json_creator.get("role"),
                    )
                )

            comics.append(
                Comic(
                    _id,
                    title,
                    description,
                    img_link,
                    page_count,
                    detail,
                    resource_uri,
                    creators,
                )
            )
        return Parsed(comics, count, total)

    @staticmethod
    def parse_list_events(response_json):
        data = response_json["data"]
        count = response_json["data"]["count"]
        total = response_json["data"]["total"]
        events = list()

        for result in data["results"]:
            _id = result["id"]
            name = result["title"]
            description = result.get("description", "")
            if not description:
                description = result.get("variantDescription", "")
            if not description:
                description = f"Sorry, I did not found description for {name}"
            thumbnail: ct.Thumbnail = result.get(
                "thumbnail", ct.Thumbnail(path="", extension="")
            )
            resource_uri = result.get("resourceURI", "")

            detail = ct.UrlInfo(type="", url="")
            wiki = ct.UrlInfo(type="", url="")
            public_links = dict(detail=detail, wiki=wiki)
            for url_info in result.get("urls", []):
                _type = url_info["type"]
                url = url_info["url"]
                if _type in public_links:
                    public_link = public_links[_type]
                    public_link["type"] = _type
                    public_link["url"] = url
                else:
                    print(f"EVENTS {_type} not in public_links")
            img_link = f"{thumbnail['path']}.{thumbnail['extension']}"

            start = result["start"]
            end = result["end"]
            next_event = result["next"]
            previous_event = result["previous"]
            events.append(
                Event(
                    _id,
                    name,
                    description,
                    img_link,
                    detail,
                    wiki,
                    resource_uri,
                    start,
                    end,
                    next_event,
                    previous_event,
                )
            )
        return Parsed(events, count, total)

    @staticmethod
    def parse_list_series(response_json):
        data = response_json["data"]
        count = response_json["data"]["count"]
        total = response_json["data"]["total"]
        series = list()

        for result in data["results"]:
            _id = result["id"]
            title = result["title"]
            description = (
                desc
                if (desc := result.get("description"))
                else f"Sorry, I did not find description for {title} :("
            )
            thumbnail: ct.Thumbnail = result.get(
                "thumbnail", ct.Thumbnail(path="", extension="")
            )
            resource_uri = result.get("resourceURI", "")

            detail = ct.UrlInfo(type="", url="")
            public_links = dict(detail=detail)
            for url_info in result.get("urls", []):
                _type = url_info["type"]
                url = url_info["url"]
                if _type in public_links:
                    public_link = public_links[_type]
                    public_link["type"] = _type
                    public_link["url"] = url
                else:
                    print(f"SERIES {_type} not in public_links")
            img_link = f"{thumbnail['path']}.{thumbnail['extension']}"

            creators = []
            json_creators = result.get("creators", {})
            for json_creator in json_creators.get("items"):
                creators.append(
                    Creator(
                        json_creator.get("resourceURI"),
                        json_creator.get("name"),
                        json_creator.get("role"),
                    )
                )
            start_year = result["startYear"]
            end_year = result["endYear"]
            next_series = result["next"]
            previous_series = result["previous"]
            series.append(
                Series(
                    _id,
                    title,
                    description,
                    img_link,
                    detail,
                    resource_uri,
                    start_year,
                    end_year,
                    next_series,
                    previous_series,
                    creators,
                )
            )
        return Parsed(series, count, total)


class Parsed:
    def __init__(self, features=None, count=0, total=0):
        self.features = features if features else []
        self.count = count
        self.total = total
