import abc

from fetcher.entities import EntityBuilder


class BaseParser(abc.ABC):
    @classmethod
    def parse(cls, response_json):
        results, count, total = cls.extract_data(response_json)
        entities = list()
        builder = EntityBuilder()

        for result in results:
            base_features = cls.extract_base_features(result)
            custom_features = cls.extract_custom_features(result)
            builder.add_base_features(base_features)
            cls.add_custom_features(builder, custom_features)
            entities.append(builder.finish())

        return Parsed(entities, count, total)

    @staticmethod
    def extract_data(response_json):
        data = response_json["data"]
        return data["results"], data["count"], data["total"]

    @classmethod
    def extract_public_link(cls, result, link):
        urls_info = result.get("urls", [])
        for url_info in urls_info:
            if (url_info["type"]) == link:
                url = url_info["url"]
                url = url.split("?utm")[0] if url else ""
                return url
        return ""

    @classmethod
    def extract_base_features(cls, result):
        _id = result["id"]
        name = result.get("name", result.get("title", ""))
        description = result.get("description", "")
        if not description:
            description = result.get("variantDescription", "")
        if not description:
            description = f"Sorry, I did not found description for {name} :("

        thumbnail = result.get("thumbnail", dict(path="", extension=""))
        img_link = f"{thumbnail['path']}.{thumbnail['extension']}"

        resource_uri = result.get("resourceURI", "")
        detail = cls.extract_public_link(result, "detail")
        base_features = {
            "_id": _id,
            "name": name,
            "description": description,
            "img_link": img_link,
            "detail": detail,
            "_resource_uri": resource_uri,
        }
        return base_features

    @classmethod
    @abc.abstractmethod
    def extract_custom_features(cls, result):
        pass

    @classmethod
    @abc.abstractmethod
    def add_custom_features(cls, builder, custom_features):
        pass


class Parsed:
    def __init__(self, features=None, count=0, total=0):
        self.features = features if features else []
        self.count = count
        self.total = total
