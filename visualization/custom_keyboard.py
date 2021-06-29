from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import States


class _CustomKeyboard:

    CALLBACK_DATA_MAX_LENGTH = 64

    @staticmethod
    def main_menu():
        buttons = [
            [
                InlineKeyboardButton(
                    text="Characters", callback_data=States.CHARACTERS.value
                ),
                InlineKeyboardButton(
                    text="Comics", callback_data=States.COMICS.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Events", callback_data=States.EVENTS.value
                ),
                InlineKeyboardButton(
                    text="Series", callback_data=States.SERIES.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Finish", callback_data=States.END.value
                )
            ],
        ]

        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def _inner_menu(
        entities, list_state, find_by_name_state, find_by_name_beginning_state
    ):
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"List {entities}", callback_data=list_state,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Find by name", callback_data=find_by_name_state,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Find by name beginning",
                    callback_data=find_by_name_beginning_state,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Back", callback_data=States.END.value
                ),
                InlineKeyboardButton(
                    text="Done", callback_data=States.END.value
                ),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        return keyboard

    @classmethod
    def characters_menu(cls):
        return cls._inner_menu(
            "Characters",
            States.LIST_CHARACTERS.value,
            States.FIND_CHARACTER_BY_NAME.value,
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value,
        )

    @classmethod
    def comics_menu(cls):
        return cls._inner_menu(
            "Comics",
            States.LIST_COMICS.value,
            States.FIND_COMIC_BY_TITLE.value,
            States.FIND_COMIC_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def events_menu(cls):
        return cls._inner_menu(
            "Events",
            States.LIST_EVENTS.value,
            States.FIND_EVENT_BY_NAME.value,
            States.FIND_EVENT_BY_NAME_BEGINNING.value,
        )

    @classmethod
    def series_menu(cls):
        return cls._inner_menu(
            "Series",
            States.LIST_SERIES.value,
            States.FIND_SERIES_BY_TITLE.value,
            States.FIND_SERIES_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def keyboard_from_iterable(cls, iterable, prev_required, next_required):
        if not iterable:
            return None
        buttons = [
            [
                InlineKeyboardButton(
                    text=item,
                    callback_data=item[: cls.CALLBACK_DATA_MAX_LENGTH],
                )
            ]
            for item in iterable
        ]
        page_buttons = []
        if prev_required:
            page_buttons.append(
                InlineKeyboardButton(
                    text="Prev", callback_data=States.PREV_PAGE.value
                ),
            )
        if next_required:
            page_buttons.append(
                InlineKeyboardButton(
                    text="Next", callback_data=States.NEXT_PAGE.value
                )
            )
        buttons.append(page_buttons)
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Back", callback_data=States.BACK.value
                ),
                InlineKeyboardButton(
                    text="Done", callback_data=States.END.value
                ),
            ],
        )
        keyboard = InlineKeyboardMarkup(buttons)
        return keyboard


class CustomKeyboard(_CustomKeyboard):
    main_menu = _CustomKeyboard.main_menu()
    characters_menu = _CustomKeyboard.characters_menu()
    comics_menu = _CustomKeyboard.comics_menu()
    events_menu = _CustomKeyboard.events_menu()
    series_menu = _CustomKeyboard.series_menu()
