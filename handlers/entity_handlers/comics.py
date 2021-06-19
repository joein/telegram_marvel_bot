from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from fetcher import Route
from states import States
from display import Display
from custom_keyboard import CustomKeyboard
from handlers.base_handlers import BaseHandler
from handlers.conversation_handler_builder import ConversationHandlerBuilder, ConversationHandlerInterface


class ComicsHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.comics_menu, CustomKeyboard.comics_menu
        )
        return States.COMICS.value

    @classmethod
    def select(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_COMIC_BY_TITLE.value: cls.find_by_name,
            States.FIND_COMIC_BY_TITLE_BEGINNING.value: cls.find_by_name_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_(cls, update: Update, context: CallbackContext):
        ok = cls._list_(update, context, Route.COMICS)
        return States.LIST_COMICS.value if ok else States.END.value

    @classmethod
    def list_previous(cls, update: Update, context: CallbackContext):
        cls._list_previous(context)
        return cls.list_(update, context)

    @classmethod
    def find_by_name(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.COMICS,
            "title",
            CustomKeyboard.comics_menu,
            Text.comics_menu,
            States.FIND_COMIC_BY_TITLE.value,
        )

    @classmethod
    def find_by_name_beginning(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.COMICS,
            "titleStartsWith",
            CustomKeyboard.comics_menu,
            Text.comics_menu,
            States.FIND_COMIC_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def list_previous_from_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous(context)
        return cls.find_by_name_beginning(update, context)

    @classmethod
    def list_previous_from_name(cls, update: Update, context: CallbackContext):
        cls._list_previous(context)
        return cls.find_by_name(update, context)


class ComicsConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):

        menu = {
            f"^{States.LIST_COMICS.value}$": ComicsHandler.list_,
            f"^{States.FIND_COMIC_BY_TITLE.value}$": ComicsHandler.find_by_name,
            f"^{States.FIND_COMIC_BY_TITLE_BEGINNING.value}$": ComicsHandler.find_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": ComicsHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_comic,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.list_,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous,
            **send,
        }
        find_by_title = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_from_name,
            **send,
        }
        find_by_title_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.COMICS.value}$": ComicsHandler.menu},
            {
                States.COMICS.value: menu,
                States.LIST_COMICS.value: list_,
                States.FIND_COMIC_BY_TITLE.value: find_by_title,
                States.FIND_COMIC_BY_TITLE_BEGINNING.value: find_by_title_beginning,
            },
            ComicsHandler.save_input,
        )