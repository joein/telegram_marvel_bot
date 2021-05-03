import logging

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
from base_handlers import MiscHandler
from conv_handler_builder import ConversationHandlerBuilder

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main(bot_token, fetcher_) -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data[FETCHER] = fetcher_

    characters_conv = ConversationHandlerBuilder.characters()
    comics_conv = ConversationHandlerBuilder.comics()
    events_conv = ConversationHandlerBuilder.events()
    series_conv = ConversationHandlerBuilder.series()

    menu_handlers = [
        characters_conv,
        comics_conv,
        events_conv,
        series_conv,
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", MiscHandler.start)],
        states={
            States.MENU.value: menu_handlers,
            States.END.value: [CommandHandler("start", MiscHandler.start)]
        },
        fallbacks=[
            CommandHandler("stop", MiscHandler.stop),
            CallbackQueryHandler(
                MiscHandler.end, pattern=f"^{States.END.value}$"
            ),
        ],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    config = Config()
    fetcher = Fetcher(config)
    main(config.bot_token, fetcher)
