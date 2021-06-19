from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from fetcher import Route
from states import States
from display import Display
from custom_keyboard import CustomKeyboard
from handlers.base_handlers import BaseHandler
from handlers.conversation_handler_builder import ConversationHandlerBuilder, ConversationHandlerInterface


class EventsHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.events_menu, CustomKeyboard.events_menu
        )
        return States.EVENTS.value

    @classmethod
    def select(cls, state, update: Update, context: CallbackContext):
        features_map = {
            States.FIND_EVENT_BY_NAME.value: cls.find_by_name,
            States.FIND_EVENT_BY_NAME_BEGINNING.value: cls.find_by_name_beginning,
        }
        return features_map[state](update, context)

    @classmethod
    def list_(cls, update: Update, context: CallbackContext):
        ok = cls._list_(update, context, Route.EVENTS)
        return States.LIST_EVENTS.value if ok else States.END.value

    @classmethod
    def list_previous(cls, update: Update, context: CallbackContext):
        cls._list_previous(context)
        return cls.list_(update, context)

    @classmethod
    def find_by_name(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.EVENTS,
            "name",
            CustomKeyboard.events_menu,
            Text.comics_menu,
            States.FIND_EVENT_BY_NAME.value,
        )

    @classmethod
    def find_by_name_beginning(cls, update: Update, context: CallbackContext):
        return cls._find_by_name(
            update,
            context,
            Route.EVENTS,
            "nameStartsWith",
            CustomKeyboard.events_menu,
            Text.comics_menu,
            States.FIND_EVENT_BY_NAME_BEGINNING.value,
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


class EventsConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_EVENTS.value}$": EventsHandler.list_,
            f"^{States.FIND_EVENT_BY_NAME.value}$": EventsHandler.find_by_name,
            f"^{States.FIND_EVENT_BY_NAME_BEGINNING.value}$": EventsHandler.find_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": EventsHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_event,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.list_,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous,
            **send,
        }
        find_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_from_name,
            **send,
        }
        find_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.EVENTS.value}$": EventsHandler.menu},
            {
                States.EVENTS.value: menu,
                States.LIST_EVENTS.value: list_,
                States.FIND_EVENT_BY_NAME.value: find_by_name,
                States.FIND_EVENT_BY_NAME_BEGINNING.value: find_by_name_beginning,
            },
            EventsHandler.save_input,
        )
