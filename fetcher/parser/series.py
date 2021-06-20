from fetcher.parser.base_parser import BaseParser


class SeriesParser(BaseParser):
    @classmethod
    def extract_custom_features(cls, result):
        return {
            "start": result["startYear"],
            "end": result["endYear"],
            "next_": result["next"],
            "previous": result["previous"],
        }

    @classmethod
    def add_custom_features(cls, builder, custom_features):
        builder.add_date_borders(
            custom_features.get("start", ""), custom_features.get("end", "")
        )
        builder.add_surrounding_entities(
            custom_features.get("next_", ""),
            custom_features.get("previous", ""),
        )