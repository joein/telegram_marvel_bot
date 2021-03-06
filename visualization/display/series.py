from telegram import Update
from telegram.ext import CallbackContext

from handlers.entity_handlers import SeriesHandler
from visualization.display.base_display import BaseDisplay


class SeriesDisplay(BaseDisplay):
    @classmethod
    def extract_content(cls, single_series):
        detail = f"detail link: {single_series.detail}"
        next_series = f"Next series are: {single_series.next_['name'] if single_series.next_ else ''}"
        previous_series = f"Previous series are: {single_series.previous['name'] if single_series.previous else ''}"

        caption = "\n\n".join(
            (
                single_series.name,
                single_series.description,
                detail,
                f"Start in: {single_series.start}",
                f"Ends in: {single_series.end}",
                next_series,
                previous_series,
            )
        )
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def send(cls, update: Update, context: CallbackContext):
        cls.send_entity(update, context)
        return SeriesHandler.menu(update, context)
