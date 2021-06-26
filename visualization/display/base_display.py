import abc

from telegram import Update
from telegram.ext import CallbackContext

from constants import FEATURES, OFFSET, MSG_DELETED


class BaseDisplay(abc.ABC):
    CALLBACK_DATA_MAX_LENGTH = 64
    CAPTION_MAX_LENGTH = 1024

    @classmethod
    def extract_entity(cls, update, context):
        entity = None
        for entity_ in context.chat_data[FEATURES]:
            length_limited_name = entity_.name[
                : cls.CALLBACK_DATA_MAX_LENGTH
            ]
            if length_limited_name == update.callback_query.data:
                entity = entity_
                break
        return entity

    @classmethod
    def send_entity(cls, update, context):
        context.chat_data[OFFSET] = 0

        entity = cls.extract_entity(update, context)
        if entity:
            caption = cls.extract_content(entity)
            context.bot.send_photo(
                update.callback_query.message.chat_id,
                entity.img_link,
                caption=caption,
            )

        update.callback_query.delete_message()
        context.chat_data[MSG_DELETED] = True

    @classmethod
    @abc.abstractmethod
    def extract_content(cls, entity):
        pass

    @classmethod
    @abc.abstractmethod
    def send(cls, update: Update, context: CallbackContext):
        pass
