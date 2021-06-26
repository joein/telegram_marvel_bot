from telegram import Update
from telegram.ext import CallbackContext

from handlers.entity_handlers import EventsHandler
from visualization.display.base_display import BaseDisplay


class EventsDisplay(BaseDisplay):
    @classmethod
    def extract_content(cls, event):
        ev_name = event.name
        description = event.description
        wiki = f"Wiki link: {event.wiki}"
        detail = f"Comics link: {event.detail}"
        next_event = (
            f"Next event: {event.next_['name'] if event.next_ else ''}"
        )
        previous_event = f"Previous event: {event.previous['name'] if event.previous else ''}"
        caption = "\n\n".join(
            (ev_name, description, wiki, detail, next_event, previous_event,)
        )
        return caption[: cls.CAPTION_MAX_LENGTH]

    @classmethod
    def send(cls, update: Update, context: CallbackContext):
        cls.send_entity(update, context)
        return EventsHandler.menu(update, context)
