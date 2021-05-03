from telegram import Update
from telegram.ext import CallbackContext

from constants import FEATURES, OFFSET, MSG_DELETED
from marvel_handlers import (
    CharactersHandler,
    ComicsHandler,
    EventsHandler,
    SeriesHandler,
)


class Display:
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
    def character_content(cls, character):
        ch_name = character.name
        description = character.description
        wiki = f"wiki link: {character.wiki}"
        detail = f"comics link: {character.detail}"
        caption = "\n\n".join((ch_name, description, wiki, detail))
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def comic_content(cls, comic):
        page_count = f"Page count: {comic.page_count if comic.page_count else 'Unknown'}"
        detail = f"detail link: {comic.detail}"
        caption = "\n\n".join(
            (
                comic.title,
                comic.description,
                page_count,
                detail,
                "Creators: "
                + "\n".join((str(creator) for creator in comic.creators)),
            )
        )
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def event_content(cls, event):
        ev_name = event.name
        description = event.description
        wiki = f"Wiki link: {event.wiki}"
        detail = f"Comics link: {event.detail}"
        next_event = f"Next event: {event.next_event['name'] if event.next_event else ''}"
        previous_event = f"Previous event: {event.previous_event['name'] if event.previous_event else ''}"
        caption = "\n\n".join(
            (ev_name, description, wiki, detail, next_event, previous_event,)
        )
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def series_content(cls, single_series):
        detail = f"detail link: {single_series.detail}"
        next_series = f"Next series are: {single_series.next_series['name'] if single_series.next_series else ''}"
        previous_series = f"Previous series are: {single_series.previous_series['name'] if single_series.previous_series else ''}"

        caption = "\n\n".join(
            (
                single_series.title,
                single_series.description,
                detail,
                f"Start in: {single_series.start_year}",
                f"Ends in: {single_series.end_year}",
                next_series,
                previous_series,
            )
        )
        return caption[: cls.CAPTION_MAX_LENGTH]

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
    def send_character(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.character_content)
        return CharactersHandler.menu(update, context)

    @classmethod
    def send_comic(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.comic_content)
        return ComicsHandler.menu(update, context)

    @classmethod
    def send_event(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.event_content)
        return EventsHandler.menu(update, context)

    @classmethod
    def send_series(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.series_content)
        return SeriesHandler.menu(update, context)
