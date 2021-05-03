from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from fetcher import Route
from states import States
from base_handlers import BaseHandler
from custom_keyboard import CustomKeyboard


class CharactersHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update,
            context,
            Text.characters_menu,
            CustomKeyboard.characters_menu,
        )
        return States.CHARACTERS.value

    @classmethod
    def select_feature(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_CHARACTER_BY_NAME.value: cls.find_character_by_name,
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value: cls.find_character_by_name_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_characters(cls, update: Update, context: CallbackContext):
        ok = cls._list_features(update, context, Route.CHARACTERS)
        return States.LIST_CHARACTERS.value if ok else States.END.value

    @classmethod
    def list_previous_characters(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.list_characters(update, context)

    @classmethod
    def list_previous_characters_from_name(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_character_by_name(update, context)

    @classmethod
    def list_previous_characters_from_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_character_by_name_beginning(update, context)

    @classmethod
    def find_character_by_name(cls, update: Update, context: CallbackContext):
        return cls._find_feature_by_name(
            update,
            context,
            Route.CHARACTERS,
            "name",
            CustomKeyboard.characters_menu,
            Text.characters_menu,
            States.FIND_CHARACTER_BY_NAME.value,
        )

    @classmethod
    def find_character_by_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        return cls._find_feature_by_name(
            update,
            context,
            Route.CHARACTERS,
            "nameStartsWith",
            CustomKeyboard.characters_menu,
            Text.characters_menu,
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value,
        )


class ComicsHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.comics_menu, CustomKeyboard.comics_menu
        )
        return States.COMICS.value

    @classmethod
    def select_feature(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_COMIC_BY_TITLE.value: cls.find_comic_by_title,
            States.FIND_COMIC_BY_TITLE_BEGINNING.value: cls.find_comic_by_title_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_comics(cls, update: Update, context: CallbackContext):
        ok = cls._list_features(update, context, Route.COMICS)
        return States.LIST_COMICS.value if ok else States.END.value

    @classmethod
    def list_previous_comics(cls, update: Update, context: CallbackContext):
        cls._list_previous_features(context)
        return cls.list_comics(update, context)

    @classmethod
    def find_comic_by_title(cls, update: Update, context: CallbackContext):
        return cls._find_feature_by_name(
            update,
            context,
            Route.COMICS,
            "title",
            CustomKeyboard.comics_menu,
            Text.comics_menu,
            States.FIND_COMIC_BY_TITLE.value,
        )

    @classmethod
    def find_comic_by_title_beginning(
        cls, update: Update, context: CallbackContext
    ):
        return cls._find_feature_by_name(
            update,
            context,
            Route.COMICS,
            "titleStartsWith",
            CustomKeyboard.comics_menu,
            Text.comics_menu,
            States.FIND_COMIC_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def list_previous_comics_from_title_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_comic_by_title_beginning(update, context)

    @classmethod
    def list_previous_comics_from_title(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_comic_by_title(update, context)


class EventsHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.events_menu, CustomKeyboard.events_menu
        )
        return States.EVENTS.value

    @classmethod
    def select_feature(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_EVENT_BY_NAME.value: cls.find_event_by_name,
            States.FIND_EVENT_BY_NAME_BEGINNING.value: cls.find_event_by_name_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_events(cls, update: Update, context: CallbackContext):
        ok = cls._list_features(update, context, Route.EVENTS)
        return States.LIST_EVENTS.value if ok else States.END.value

    @classmethod
    def list_previous_events(cls, update: Update, context: CallbackContext):
        cls._list_previous_features(context)
        return cls.list_events(update, context)

    @classmethod
    def find_event_by_name(cls, update: Update, context: CallbackContext):
        return cls._find_feature_by_name(
            update,
            context,
            Route.EVENTS,
            "name",
            CustomKeyboard.events_menu,
            Text.comics_menu,
            States.FIND_EVENT_BY_NAME.value,
        )

    @classmethod
    def find_event_by_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        return cls._find_feature_by_name(
            update,
            context,
            Route.EVENTS,
            "nameStartsWith",
            CustomKeyboard.events_menu,
            Text.comics_menu,
            States.FIND_EVENT_BY_NAME_BEGINNING.value,
        )

    @classmethod
    def list_previous_events_from_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_event_by_name_beginning(update, context)

    @classmethod
    def list_previous_events_from_name(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_event_by_name(update, context)


class SeriesHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.series_menu, CustomKeyboard.series_menu
        )
        return States.SERIES.value

    @classmethod
    def select_feature(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_SERIES_BY_TITLE.value: cls.find_series_by_title,
            States.FIND_SERIES_BY_TITLE_BEGINNING.value: cls.find_series_by_title_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_series(cls, update: Update, context: CallbackContext):
        ok = cls._list_features(update, context, Route.SERIES)
        return States.LIST_SERIES.value if ok else States.END.value

    @classmethod
    def list_previous_series(cls, update: Update, context: CallbackContext):
        cls._list_previous_features(context)
        return cls.list_series(update, context)

    @classmethod
    def find_series_by_title(cls, update: Update, context: CallbackContext):

        return cls._find_feature_by_name(
            update,
            context,
            Route.SERIES,
            "title",
            CustomKeyboard.series_menu,
            Text.series_menu,
            States.FIND_SERIES_BY_TITLE.value,
        )

    @classmethod
    def find_series_by_title_beginning(
        cls, update: Update, context: CallbackContext
    ):
        return cls._find_feature_by_name(
            update,
            context,
            Route.SERIES,
            "titleStartsWith",
            CustomKeyboard.series_menu,
            Text.series_menu,
            States.FIND_SERIES_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def list_previous_series_from_title_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_series_by_title_beginning(update, context)

    @classmethod
    def list_previous_series_from_title(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous_features(context)
        return cls.find_series_by_title_beginning(update, context)
