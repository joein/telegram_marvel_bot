from telegram import Update
from telegram.ext import CallbackContext

from handlers.entity_handlers import CharactersHandler
from visualization.display.base_display import BaseDisplay


class CharactersDisplay(BaseDisplay):
    @classmethod
    def content(cls, character):
        ch_name = character.name
        description = character.description
        wiki = f"wiki link: {character.wiki}"
        detail = f"comics link: {character.detail}"
        caption = "\n\n".join((ch_name, description, wiki, detail))
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def send(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.content)
        return CharactersHandler.menu(update, context)
