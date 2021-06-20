from fetcher.parser.base_parser import BaseParser


class EventParser(BaseParser):
    @classmethod
    def extract_custom_features(cls, result):

        return {
            "start": result["start"],
            "end": result["end"],
            "next_": result["next"],
            "previous": result["previous"],
            "wiki": cls.extract_public_link(result, "wiki"),
        }

    @classmethod
    def add_custom_features(cls, builder, custom_features):
        builder.add_date_borders(
            custom_features.get("start", ""), custom_features.get("end", "")
        )
        builder.add_surrounding_entities(
            custom_features.get("next", ""),
            custom_features.get("previous", ""),
        )
        builder.add_wiki(custom_features.get("wiki", ""))
