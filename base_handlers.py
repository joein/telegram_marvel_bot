import abc

from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from states import States
from custom_keyboard import CustomKeyboard
from constants import (
    DATA,
    INPUT_FOR,
    FETCHER,
    OFFSET,
    FEATURES,
    LIMIT,
    START_OVER,
    MSG_DELETED,
)


class BaseHandler(abc.ABC):
    @staticmethod
    def _inner_menu(update: Update, context: CallbackContext, text, keyboard):
        context.chat_data[OFFSET] = 0

        if context.chat_data.get(DATA):
            del context.chat_data[DATA]

        if context.chat_data.get(MSG_DELETED):
            del context.chat_data[MSG_DELETED]

            context.bot.send_message(
                update.callback_query.message.chat_id,
                text=text,
                reply_markup=keyboard,
            )
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text, reply_markup=keyboard
            )

    @classmethod
    def _list_features(cls, update: Update, context: CallbackContext, route):
        text, keyboard = cls._request_features(context, route, LIMIT)
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )

    @classmethod
    def _list_previous_features(cls, context: CallbackContext):
        current_offset = context.chat_data[OFFSET]
        subtract_value = LIMIT + (current_offset % 10 or LIMIT)
        context.chat_data[OFFSET] -= subtract_value

    @classmethod
    def _find_feature_by_name(
        cls,
        update: Update,
        context: CallbackContext,
        route,
        filter_key,
        menu_keyboard,
        menu_text,
        return_state,
    ):
        if not (value := context.chat_data.get(DATA)):
            context.chat_data[INPUT_FOR] = return_state
            return cls.ask_for_input(update, context)

        text, keyboard = cls._request_features(
            context, route, LIMIT, **{filter_key: value}
        )

        if not keyboard:
            keyboard = menu_keyboard

            if DATA in context.chat_data:
                del context.chat_data[DATA]
            text = Text.not_found_by_name(value)
            update.message.reply_text(text=text)
            text = menu_text

        if update.message:
            update.message.reply_text(text=text, reply_markup=keyboard)
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text, reply_markup=keyboard
            )

        return return_state

    @classmethod
    def _request_features(cls, context, route, limit, **kwargs):

        fetcher_ = context.bot_data[FETCHER]
        offset = context.chat_data.get(OFFSET, 0)
        fetched_data = fetcher_.list_features(
            route, limit=limit, offset=offset, **kwargs
        )

        has_more_pages = limit + offset < fetched_data.total

        features = fetched_data.features
        context.chat_data[FEATURES] = features

        sorted_features = sorted(
            [
                getattr(feature, "name", getattr(feature, "title", ""))
                for feature in features
            ]
        )
        keyboard = CustomKeyboard.keyboard_from_iterable(
            sorted_features, bool(offset), has_more_pages
        )
        text = Text.from_container(sorted_features)
        context.chat_data[OFFSET] = offset + min(limit, fetched_data.count)

        return text, keyboard

    @classmethod
    def save_input(cls, update: Update, context: CallbackContext) -> str:
        context.chat_data[DATA] = update.message.text
        return cls.select_feature(
            context.chat_data[INPUT_FOR], update, context
        )

    @staticmethod
    def ask_for_input(update: Update, context: CallbackContext) -> str:
        context.chat_data[DATA] = update.callback_query.data
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=Text.ask_for_input)
        return States.ASK_FOR_INPUT.value

    @classmethod
    @abc.abstractmethod
    def select_feature(cls, state, update: Update, context: CallbackContext):
        pass


class MiscHandler:
    @classmethod
    def start(cls, update: Update, context: CallbackContext):
        text = Text.menu

        if context.chat_data.get(START_OVER):
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text, reply_markup=CustomKeyboard.main_menu
            )
        else:
            update.message.reply_text(Text.greetings)
            update.message.reply_text(
                text=text, reply_markup=CustomKeyboard.main_menu
            )
        context.chat_data[START_OVER] = False
        return States.MENU.value

    @classmethod
    def end_second_level(cls, update: Update, context: CallbackContext):
        context.chat_data[OFFSET] = 0
        context.chat_data[START_OVER] = True
        cls.start(update, context)
        return States.END.value

    @classmethod
    def stop(cls, update: Update, _: CallbackContext):
        update.message.reply_text(Text.stop)
        return States.END.value

    @classmethod
    def end(cls, update: Update, _: CallbackContext):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=Text.end)
        return States.END.value