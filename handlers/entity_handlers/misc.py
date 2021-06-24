from telegram import Update
from telegram.ext import CallbackContext

from text import Text
from states import States
from constants import OFFSET, START_OVER
from visualization.custom_keyboard import CustomKeyboard


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
