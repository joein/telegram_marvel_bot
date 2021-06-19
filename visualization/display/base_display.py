import abc

from telegram import Update
from telegram.ext import CallbackContext

from constants import FEATURES, OFFSET, MSG_DELETED


class BaseDisplay(abc.ABC):
    CALLBACK_DATA_MAX_LENGTH = 64
    CAPTION_MAX_LENGTH = 1024

    @classmethod
    def extract_feature(cls, update, context):
        feature = None
        for feature_ in context.chat_data[FEATURES]:
            field_name = "name" if hasattr(feature_, "name") else "title"
            value = getattr(feature_, field_name)
            length_limited_value = value[: cls.CALLBACK_DATA_MAX_LENGTH]
            if length_limited_value == update.callback_query.data:
                feature = feature_
                break
        return feature

    @classmethod
    def send_feature(cls, update, context, content_extractor):
        context.chat_data[OFFSET] = 0

        feature = cls.extract_feature(update, context)
        if feature:
            caption = content_extractor(feature)
            context.bot.send_photo(
                update.callback_query.message.chat_id,
                feature.img_link,
                caption=caption,
            )

        update.callback_query.delete_message()
        context.chat_data[MSG_DELETED] = True

    @classmethod
    @abc.abstractmethod
    def content(cls, feature):
        pass

    @classmethod
    @abc.abstractmethod
    def send(cls, update: Update, context: CallbackContext):
        pass
