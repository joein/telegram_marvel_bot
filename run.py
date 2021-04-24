from config import Config
from fetcher import Fetcher, Route
from parser import ResponseJsonParser

if __name__ == "__main__":
    config = Config()
    fetcher = Fetcher(config)
    #
    # characters = fetcher.list_features(
    #     Route.CHARACTERS, ResponseJsonParser.parse_list_characters, limit=4
    # )
    # fetcher.list_features(
    #     Route.COMICS, ResponseJsonParser.parse_list_comics, limit=4
    # )
    # fetcher.list_features(
    #     Route.EVENTS, ResponseJsonParser.parse_list_events, limit=4
    # )
    fetcher.list_features(
        Route.SERIES, ResponseJsonParser.parse_list_series, limit=4
    )
