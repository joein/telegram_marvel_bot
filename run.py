from config import Config
from fetcher import Fetcher, Route
from parser import ResponseJsonParser

if __name__ == "__main__":
    config = Config()
    fetcher = Fetcher(config)
    #
    # characters = fetcher.list_features(
    #     Route.CHARACTERS, limit=4
    # )
    # fetcher.list_features(
    #     Route.COMICS, limit=4
    # )
    # fetcher.list_features(
    #     Route.EVENTS, limit=4
    # )
    # fetcher.list_features(
    #     Route.SERIES, limit=4
    # )
