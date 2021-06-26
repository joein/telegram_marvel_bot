from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from fetcher import Route
from states import States
from visualization.custom_keyboard import CustomKeyboard
from handlers.entity_handlers.base_handler import BaseHandler


class EventsHandler(BaseHandler):
    @classmethod
    def menu(cls, update: Update, context: CallbackContext) -> str:
        cls._inner_menu(
            update, context, Text.events_menu, CustomKeyboard.events_menu
        )
        return States.EVENTS.value

    @classmethod
    def select(cls, state, update: Update, context: CallbackContext):
        callbacks = {
            States.FIND_EVENT_BY_NAME.value: cls.find_by_name,
            States.FIND_EVENT_BY_NAME_BEGINNING.value: cls.find_by_name_beginning,
        }
        return callbacks[state](update, context)

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
