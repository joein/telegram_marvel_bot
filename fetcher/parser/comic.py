from fetcher.entities import Creator
from fetcher.parser.base_parser import BaseParser


class ComicParser(BaseParser):
    @classmethod
    def extract_custom_features(cls, result):
        page_count = result["pageCount"]

        json_creators = result.get("creators", {})
        creators = [
            Creator(
                json_creator.get("resourceURI"),
                json_creator.get("name"),
                json_creator.get("role"),
            )
            for json_creator in json_creators.get("items")
        ]

        return {"page_count": page_count, "creators": creators}

    @classmethod
    def add_custom_features(cls, builder, custom_features):
        builder.add_comic_meta(**custom_features)
