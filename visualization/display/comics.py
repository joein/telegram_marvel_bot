from telegram import Update
from telegram.ext import CallbackContext

from handlers.entity_handlers import ComicsHandler
from visualization.display.base_display import BaseDisplay


class ComicsDisplay(BaseDisplay):
    @classmethod
    def extract_content(cls, comic):
        page_count = f"Page count: {comic.page_count if comic.page_count else 'Unknown'}"
        detail = f"detail link: {comic.detail}"
        caption = "\n\n".join(
            (
                comic.name,
                comic.description,
                page_count,
                detail,
                "Creators: "
                + "\n".join((str(creator) for creator in comic.creators)),
            )
        )
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def send(cls, update: Update, context: CallbackContext):
        cls.send_entity(update, context)
        return ComicsHandler.menu(update, context)
