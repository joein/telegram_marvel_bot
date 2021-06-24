from fetcher.parser.base_parser import BaseParser


class CharacterParser(BaseParser):
    @classmethod
    def extract_custom_features(cls, result):
        return {"wiki": cls.extract_public_link(result, {})}

    @classmethod
    def add_custom_features(cls, builder, custom_features):
        builder.add_wiki(custom_features.get("wiki", ""))
