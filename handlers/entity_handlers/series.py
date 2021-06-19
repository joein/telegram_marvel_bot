from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from fetcher import Route
from states import States
from display import Display
from custom_keyboard import CustomKeyboard
from handlers.base_handlers import BaseHandler
from handlers.conversation_handler_builder import (
    ConversationHandlerBuilder,
    ConversationHandlerInterface,
)


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


class SeriesConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_SERIES.value}$": SeriesHandler.list_,
            f"^{States.FIND_SERIES_BY_TITLE.value}$": SeriesHandler.find_by_name,
            f"^{States.FIND_SERIES_BY_TITLE_BEGINNING.value}$": SeriesHandler.find_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": SeriesHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_series,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.list_,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous,
            **send,
        }
        find_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_from_name,
            **send,
        }
        find_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.SERIES.value}$": SeriesHandler.menu},
            {
                States.SERIES.value: menu,
                States.LIST_SERIES.value: list_,
                States.FIND_SERIES_BY_TITLE.value: find_by_name,
                States.FIND_SERIES_BY_TITLE_BEGINNING.value: find_by_name_beginning,
            },
            SeriesHandler.save_input,
        )
