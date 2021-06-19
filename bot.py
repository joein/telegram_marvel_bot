from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

from config import Config
from states import States
from fetcher import Fetcher
from constants import FETCHER
from handlers.base_handlers import MiscHandler
from handlers.entity_handlers import (
    CharactersConversationHandler,
    ComicsConversationHandler,
    EventsConversationHandler,
    SeriesConversationHandler,
)


def main(bot_token, fetcher) -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data[FETCHER] = fetcher

    characters_handler = CharactersConversationHandler.get()
    comics_handler = ComicsConversationHandler.get()
    events_handler = EventsConversationHandler.get()
    series_handler = SeriesConversationHandler.get()

    menu_handlers = [
        characters_handler,
        comics_handler,
        events_handler,
        series_handler,
    ]

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", MiscHandler.start)],
        states={
            States.MENU.value: menu_handlers,
            States.END.value: [CommandHandler("start", MiscHandler.start)],
        },
        fallbacks=[
            CommandHandler("stop", MiscHandler.stop),
            CallbackQueryHandler(
                MiscHandler.end, pattern=f"^{States.END.value}$"
            ),
        ],
    )
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    config = Config()
    fetcher_ = Fetcher(config)
    main(config.bot_token, fetcher_)
