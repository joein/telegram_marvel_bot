from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from states import States
from fetcher.fetcher import Route
from custom_keyboard import CustomKeyboard
from handlers.entity_handlers.base_handler import BaseHandler


class SeriesHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.series_menu, CustomKeyboard.series_menu
        )
        return States.SERIES.value

    @classmethod
    def select(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_SERIES_BY_TITLE.value: cls.find_by_name,
            States.FIND_SERIES_BY_TITLE_BEGINNING.value: cls.find_by_name_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_(cls, update: Update, context: CallbackContext):
        ok = cls._list_(update, context, Route.SERIES)
        return States.LIST_SERIES.value if ok else States.END.value

    @classmethod
    def list_previous(cls, update: Update, context: CallbackContext):
        cls._list_previous(context)
        return cls.list_(update, context)

    @classmethod
    def find_by_name(cls, update: Update, context: CallbackContext):

        return cls._find_by_name(
            update,
            context,
            Route.SERIES,
            "title",
            CustomKeyboard.series_menu,
            Text.series_menu,
            States.FIND_SERIES_BY_TITLE.value,
        )

    @classmethod
    def find_by_name_beginning(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.SERIES,
            "titleStartsWith",
            CustomKeyboard.series_menu,
            Text.series_menu,
            States.FIND_SERIES_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def list_previous_from_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous(context)
        return cls.find_by_name_beginning(update, context)

    @classmethod
    def list_previous_from_title(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous(context)
        return cls.find_by_name_beginning(update, context)
