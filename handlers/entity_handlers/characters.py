from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from fetcher import Route
from states import States
from display import Display
from custom_keyboard import CustomKeyboard
from handlers.base_handlers import BaseHandler
from handlers.conversation_handler_builder import ConversationHandlerBuilder, ConversationHandlerInterface


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
    def select(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_CHARACTER_BY_NAME.value: cls.find_by_name,
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value: cls.find_by_name_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_(cls, update: Update, context: CallbackContext):
        ok = cls._list_(update, context, Route.CHARACTERS)
        return States.LIST_CHARACTERS.value if ok else States.END.value

    @classmethod
    def list_previous(cls, update: Update, context: CallbackContext):
        cls._list_previous(context)
        return cls.list_(update, context)

    @classmethod
    def list_previous_from_name(cls, update: Update, context: CallbackContext):
        cls._list_previous(context)
        return cls.find_by_name(update, context)

    @classmethod
    def list_previous_from_name_beginning(
        cls, update: Update, context: CallbackContext
    ):
        cls._list_previous(context)
        return cls.find_by_name_beginning(update, context)

    @classmethod
    def find_by_name(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.CHARACTERS,
            "name",
            CustomKeyboard.characters_menu,
            Text.characters_menu,
            States.FIND_CHARACTER_BY_NAME.value,
        )

    @classmethod
    def find_by_name_beginning(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.CHARACTERS,
            "nameStartsWith",
            CustomKeyboard.characters_menu,
            Text.characters_menu,
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value,
        )


class CharactersConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_CHARACTERS.value}$": CharactersHandler.list_,
            f"^{States.FIND_CHARACTER_BY_NAME.value}$": CharactersHandler.find_by_name,
            f"^{States.FIND_CHARACTER_BY_NAME_BEGINNING.value}$": CharactersHandler.find_by_name_beginning,
        }
        back = {f"^{States.BACK.value}$": CharactersHandler.menu}
        send = {
            f"^(?!{States.END.value}).+$": Display.send_character,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.list_,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous,
            **send,
        }
        find_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_from_name,
            **send,
        }
        find_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_from_name_beginning,
            **send,
        }

        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.CHARACTERS.value}$": CharactersHandler.menu},
            {
                States.CHARACTERS.value: menu,
                States.LIST_CHARACTERS.value: list_,
                States.FIND_CHARACTER_BY_NAME.value: find_by_name,
                States.FIND_CHARACTER_BY_NAME_BEGINNING.value: find_by_name_beginning,
            },
            CharactersHandler.save_input,
        )
