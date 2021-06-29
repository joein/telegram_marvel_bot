class _Text:
    greetings = (
        "Hi, I'm Marvel Bot and I'm here to help you gather "
        "information about Marvel Universe."
    )

    stop = "Okay, bye."
    end = "See you around!"
    ask_for_input = "Okay, tell me."
    error = "Sorry, I can't handle this now, try again later."

    @staticmethod
    def menu():
        return (
            "You may search information about characters, comics, series, "
            "events and etc.To abort, simply type /stop."
        )

    @staticmethod
    def _inner_menu(entities, criterion):
        text = (
            f"You may request list of {entities} (in alphabetical order),"
            f" try to find {entities} by exact {criterion}"
            f" or by its beginning"
        )
        return text

    @classmethod
    def characters_menu(cls):
        return cls._inner_menu("characters", "name")

    @classmethod
    def comics_menu(cls):
        return cls._inner_menu("comics", "title")

    @classmethod
    def events_menu(cls):
        return cls._inner_menu("events", "name")

    @classmethod
    def series_menu(cls):
        return cls._inner_menu("series", "title")

    @staticmethod
    def not_found_by_name(name):
        return f"Sorry, I didn't found anything for {name}."

    @staticmethod
    def from_container(container, sep="\n"):
        return sep.join(container)


class Text(_Text):
    menu = _Text.menu()
    characters_menu = _Text.characters_menu()
    comics_menu = _Text.comics_menu()
    events_menu = _Text.events_menu()
    series_menu = _Text.series_menu()
