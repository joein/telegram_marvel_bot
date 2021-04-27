import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)

from config import Config
from fetcher import Fetcher, Route

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
MENU = "MENU"
STOPPING = "STOPPING"
START_OVER = "START_OVER"
BACK = "BACK"
NEXT_PAGE = "NEXT_PAGE"
PREV_PAGE = "PREV_PAGE"
CHARACTERS, COMICS, SERIES, EVENTS = "_0", "_1", "_2", "_3"
(
    LIST_CHARACTERS,
    FIND_CHARACTER_BY_NAME,
    FIND_CHARACTER_BY_NAME_BEGINNING,
) = ("_4", "_5", "_6")
LIST_COMICS, FIND_COMIC_BY_TITLE, FIND_COMIC_BY_TITLE_BEGINNING = (
    "_7",
    "_8",
    "_9",
)
LIST_EVENTS, FIND_EVENT_BY_NAME, FIND_EVENT_BY_NAME_BEGINNING = (
    "_10",
    "_11",
    "_12",
)
LIST_SERIES, FIND_SERIES_BY_TITLE, FIND_SERIES_BY_TITLE_BEGINNING = (
    "_13",
    "_14",
    "_15",
)
# Shortcut for ConversationHandler.END
END = ConversationHandler.END


# Top level conversation callbacks
def start(update: Update, context: CallbackContext):
    logger.info("start")
    text = (
        "You may search information about characters, comics, series, "
        "events and etc.To abort, simply type /stop."
    )

    buttons = [
        [
            InlineKeyboardButton(text="Characters", callback_data=CHARACTERS),
            InlineKeyboardButton(text="Comics", callback_data=COMICS),
        ],
        [
            InlineKeyboardButton(text="Events", callback_data=EVENTS),
            InlineKeyboardButton(text="Series", callback_data=SERIES),
        ],
        [InlineKeyboardButton(text="Finish", callback_data=END),],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        update.message.reply_text(
            "Hi, I'm Marvel Bot and I'm here to help you gather information "
            "about Marvel Universe."
        )
        update.message.reply_text(text=text, reply_markup=keyboard)
    context.user_data[START_OVER] = False
    logger.info("returning menu")
    return MENU


def characters_menu(update: Update, context: CallbackContext) -> str:
    logger.info("characters menu")
    logger.info(f"context bot data {context.bot_data}")
    logger.info(f"context user data {context.user_data}")
    logger.info(f"context chat data {context.chat_data}")
    logger.info(f"context match {context.match}")

    context.bot_data["list_characters_offset"] = 0

    text = (
        "You may request list of characters (in alphabetical order), "
        "try to find character by exact name or by its beginning."
    )
    buttons = [
        [
            InlineKeyboardButton(
                text="List Characters", callback_data=LIST_CHARACTERS
            ),
        ],
        [
            InlineKeyboardButton(
                text="Find character by name",
                callback_data=FIND_CHARACTER_BY_NAME,
            ),
            InlineKeyboardButton(
                text="Find character by name beginning",
                callback_data=FIND_CHARACTER_BY_NAME_BEGINNING,
            ),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=END),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    logger.info("characters")
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    logger.info("returning characters")
    return CHARACTERS


def comics_menu(update: Update, context: CallbackContext) -> str:
    logger.info("comics")
    text = (
        "You may request list of comics (in alphabetical order), "
        "try to find comic by exact title or by its beginning."
    )
    buttons = [
        [InlineKeyboardButton(text="List Comics", callback_data=LIST_COMICS),],
        [
            InlineKeyboardButton(
                text="Find comic by title", callback_data=FIND_COMIC_BY_TITLE,
            ),
            InlineKeyboardButton(
                text="Find comic by title beginning",
                callback_data=FIND_COMIC_BY_TITLE_BEGINNING,
            ),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=END),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    logger.info("comics")
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    logger.info("returning comics")
    return COMICS


def events_menu(update: Update, context: CallbackContext) -> str:
    logger.info("list events")
    text = (
        "You may request list of events (in alphabetical order), "
        "try to find event by exact name or by its beginning."
    )
    buttons = [
        [InlineKeyboardButton(text="List Events", callback_data=LIST_EVENTS),],
        [
            InlineKeyboardButton(
                text="Find event by name", callback_data=FIND_EVENT_BY_NAME,
            ),
            InlineKeyboardButton(
                text="Find event by name beginning",
                callback_data=FIND_EVENT_BY_NAME_BEGINNING,
            ),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=END),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    logger.info("events")
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    logger.info("returning events")
    return EVENTS


def series_menu(update: Update, context: CallbackContext) -> str:
    logger.info("series")
    text = (
        "You may request list of series (in alphabetical order), "
        "try to find series by exact title or by its beginning."
    )
    buttons = [
        [InlineKeyboardButton(text="List Series", callback_data=LIST_SERIES),],
        [
            InlineKeyboardButton(
                text="Find series by title",
                callback_data=FIND_SERIES_BY_TITLE,
            ),
            InlineKeyboardButton(
                text="Find series by title beginning",
                callback_data=FIND_SERIES_BY_TITLE_BEGINNING,
            ),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=END),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    logger.info("series")
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    logger.info("returning series")
    return SERIES


def stop(update: Update, _: CallbackContext) -> int:
    """End Conversation by command."""
    logger.info("stop")
    update.message.reply_text("Okay, bye.")
    logger.info("returning end")
    return END


def end(update: Update, _: CallbackContext) -> int:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = "See you around!"
    update.callback_query.edit_message_text(text=text)

    return END


# Second level conversation callbacks
def list_characters(update: Update, context: CallbackContext):
    logger.info("List characters command")
    limit = 10
    fetcher = context.bot_data["fetcher"]
    offset = context.bot_data.get("list_characters_offset", 0)
    fetched_data = fetcher.list_features(
        Route.CHARACTERS, limit=limit, offset=offset
    )
    logger.info(f"{limit + offset} and total {fetched_data['total']}")
    has_more_pages = limit + offset < fetched_data["total"]

    characters = fetched_data["features"]
    chars = sorted([character.name for character in characters])
    buttons = [
        [InlineKeyboardButton(text=char_, callback_data=LIST_CHARACTERS,)]
        for char_ in chars
    ]
    page_buttons = []
    if offset:
        page_buttons.append(
            InlineKeyboardButton(text="Prev", callback_data=PREV_PAGE),
        )
    if has_more_pages:
        buttons.append(
            [InlineKeyboardButton(text="Next", callback_data=NEXT_PAGE,),]
        )
    buttons.append(page_buttons)
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    )
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(chars), reply_markup=keyboard
    )
    context.bot_data["list_characters_offset"] = offset + min(
        limit, fetched_data["count"]
    )
    return LIST_CHARACTERS


def list_previous_characters(update: Update, context: CallbackContext):
    limit = 10
    current_offset = context.bot_data["list_characters_offset"]
    subtract_value = limit + (current_offset % 10 or limit)

    context.bot_data["list_characters_offset"] -= subtract_value
    return list_characters(update, context)


def find_character_by_name(update: Update, _: CallbackContext):
    logger.info("Find character by name")
    chars = [
        "Find Ant-Man",
        "Find Captain America",
        "Find Iron-Man",
        "Find Spider-Man",
    ]
    buttons = [
        [
            InlineKeyboardButton(
                text=char_, callback_data=FIND_CHARACTER_BY_NAME,
            )
            for char_ in chars
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(chars), reply_markup=keyboard
    )

    return FIND_CHARACTER_BY_NAME


def find_character_by_name_beginning(update: Update, _: CallbackContext):
    logger.info("Find character by name beginning")
    chars = ["Find Ant", "Find Captain", "Find Iron", "Find Spider"]
    buttons = [
        [
            InlineKeyboardButton(
                text=char_, callback_data=FIND_CHARACTER_BY_NAME_BEGINNING,
            )
            for char_ in chars
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(chars), reply_markup=keyboard
    )

    return FIND_CHARACTER_BY_NAME_BEGINNING


def list_comics(update: Update, context: CallbackContext):
    logger.info("List comics command")
    fetcher = context.bot_data["fetcher"]
    comics = sorted(
        [
            comic.title
            for comic in fetcher.list_features(
                Route.COMICS, limit=10, offset=0
            )
        ]
    )
    buttons = [
        [InlineKeyboardButton(text=comic, callback_data=LIST_COMICS,)]
        for comic in comics
    ]
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    )

    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(comics), reply_markup=keyboard
    )

    return LIST_COMICS


def find_comic_by_title(update: Update, _: CallbackContext):
    logger.info("Find comic by title")
    comics = [
        "Find Ant-Man comic",
        "Find Captain America comic",
        "Find Iron-Man comic",
        "Find Spider-Man comic",
    ]
    buttons = [
        [
            InlineKeyboardButton(
                text=comic, callback_data=FIND_COMIC_BY_TITLE,
            )
            for comic in comics
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(comics), reply_markup=keyboard
    )

    return FIND_COMIC_BY_TITLE


def find_comic_by_title_beginning(update: Update, _: CallbackContext):
    logger.info("Find comic by title beginning")
    comics = [
        "Find Ant comic",
        "Find Captain comic",
        "Find Iron comic",
        "Find Spider comic",
    ]
    buttons = [
        [
            InlineKeyboardButton(
                text=comic, callback_data=FIND_COMIC_BY_TITLE_BEGINNING,
            )
            for comic in comics
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(comics), reply_markup=keyboard
    )

    return FIND_COMIC_BY_TITLE_BEGINNING


def list_events(update: Update, context: CallbackContext):
    logger.info("List events command")
    fetcher = context.bot_data["fetcher"]
    events = sorted(
        [
            event.name
            for event in fetcher.list_features(
                Route.EVENTS, limit=10, offset=0
            )
        ]
    )
    buttons = [
        [InlineKeyboardButton(text=event, callback_data=LIST_EVENTS,)]
        for event in events
    ]
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    )

    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(events), reply_markup=keyboard
    )

    return LIST_EVENTS


def find_event_by_name(update: Update, _: CallbackContext):
    logger.info("Find event by name")
    events = [
        "Find Event Ant-Man",
        "Find Event Captain America",
        "Find Event Iron-Man",
        "Find EventSpider-Man",
    ]
    buttons = [
        [
            InlineKeyboardButton(text=event, callback_data=FIND_EVENT_BY_NAME,)
            for event in events
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(events), reply_markup=keyboard
    )

    return FIND_EVENT_BY_NAME


def find_event_by_name_beginning(update: Update, _: CallbackContext):
    logger.info("Find event by name beginning")
    events = [
        "Find Event Ant",
        "Find Event Captain",
        "Find Event Iron",
        "Find Event Spider",
    ]
    buttons = [
        [
            InlineKeyboardButton(
                text=event, callback_data=FIND_EVENT_BY_NAME_BEGINNING,
            )
            for event in events
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(events), reply_markup=keyboard
    )

    return FIND_EVENT_BY_NAME_BEGINNING


def list_series(update: Update, context: CallbackContext):
    logger.info("List series command")
    fetcher = context.bot_data["fetcher"]
    series = sorted(
        [
            single_series.title
            for single_series in fetcher.list_features(
                Route.SERIES, limit=10, offset=0
            )
        ]
    )
    buttons = [
        [InlineKeyboardButton(text=single_series, callback_data=LIST_SERIES,)]
        for single_series in series
    ]
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    )
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(series), reply_markup=keyboard
    )

    return LIST_SERIES


def find_series_by_title(update: Update, _: CallbackContext):
    logger.info("Find series by title")
    series = [
        "Find Ant-Man series",
        "Find Captain America series",
        "Find Iron-Man series",
        "Find Spider-Man series",
    ]
    buttons = [
        [
            InlineKeyboardButton(
                text=series_, callback_data=FIND_SERIES_BY_TITLE
            )
            for series_ in series
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(series), reply_markup=keyboard
    )

    return FIND_SERIES_BY_TITLE


def find_series_by_title_beginning(update: Update, _: CallbackContext):
    logger.info("Find series by title beginning")
    series = [
        "Find Ant series",
        "Find Captain series",
        "Find Iron series",
        "Find Spider series",
    ]
    buttons = [
        [
            InlineKeyboardButton(
                text=series_, callback_data=FIND_SERIES_BY_TITLE_BEGINNING
            )
            for series_ in series
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK,),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(series), reply_markup=keyboard
    )

    return FIND_SERIES_BY_TITLE_BEGINNING


def end_second_level(update: Update, context: CallbackContext) -> int:
    """Return to top level conversation."""
    logger.info("end second level")
    context.user_data[START_OVER] = True
    start(update, context)
    logger.info("returning end")
    return END


def main(bot_token, fetcher) -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["fetcher"] = fetcher

    characters_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                characters_menu, pattern="^" + CHARACTERS + "$"
            )
        ],
        states={
            CHARACTERS: [
                CallbackQueryHandler(
                    list_characters, pattern="^" + LIST_CHARACTERS + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + FIND_CHARACTER_BY_NAME + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^" + FIND_CHARACTER_BY_NAME_BEGINNING + "$",
                ),
            ],
            LIST_CHARACTERS: [
                CallbackQueryHandler(
                    characters_menu, pattern="^" + BACK + "$"
                ),
                CallbackQueryHandler(
                    list_characters, pattern="^" + NEXT_PAGE + "$",
                ),
                CallbackQueryHandler(
                    list_previous_characters, pattern="^" + PREV_PAGE + "$",
                ),
            ],
            FIND_CHARACTER_BY_NAME: [
                CallbackQueryHandler(characters_menu, pattern="^" + BACK + "$")
            ],
            FIND_CHARACTER_BY_NAME_BEGINNING: [
                CallbackQueryHandler(characters_menu, pattern="^" + BACK + "$")
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(END) + "$"
            ),
        ],
        map_to_parent={END: MENU, STOPPING: END,},
    )

    comics_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(comics_menu, pattern="^" + COMICS + "$")
        ],
        states={
            COMICS: [
                CallbackQueryHandler(
                    list_comics, pattern="^" + LIST_COMICS + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + FIND_COMIC_BY_TITLE + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^" + FIND_COMIC_BY_TITLE_BEGINNING + "$",
                ),
            ],
            LIST_COMICS: [
                CallbackQueryHandler(comics_menu, pattern="^" + BACK + "$")
            ],
            FIND_COMIC_BY_TITLE: [
                CallbackQueryHandler(comics_menu, pattern="^" + BACK + "$")
            ],
            FIND_COMIC_BY_TITLE_BEGINNING: [
                CallbackQueryHandler(comics_menu, pattern="^" + BACK + "$")
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(END) + "$"
            ),
        ],
        map_to_parent={END: MENU, STOPPING: END,},
    )

    events_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(events_menu, pattern="^" + EVENTS + "$")
        ],
        states={
            EVENTS: [
                CallbackQueryHandler(
                    list_events, pattern="^" + LIST_EVENTS + "$",
                ),
                CallbackQueryHandler(
                    find_event_by_name, pattern="^" + FIND_EVENT_BY_NAME + "$",
                ),
                CallbackQueryHandler(
                    find_event_by_name_beginning,
                    pattern="^" + FIND_EVENT_BY_NAME_BEGINNING + "$",
                ),
            ],
            LIST_EVENTS: [
                CallbackQueryHandler(events_menu, pattern="^" + BACK + "$")
            ],
            FIND_EVENT_BY_NAME: [
                CallbackQueryHandler(events_menu, pattern="^" + BACK + "$")
            ],
            FIND_EVENT_BY_NAME_BEGINNING: [
                CallbackQueryHandler(events_menu, pattern="^" + BACK + "$")
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(END) + "$"
            ),
        ],
        map_to_parent={END: MENU, STOPPING: END,},
    )

    series_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(series_menu, pattern="^" + SERIES + "$")
        ],
        states={
            SERIES: [
                CallbackQueryHandler(
                    list_series, pattern="^" + LIST_SERIES + "$",
                ),
                CallbackQueryHandler(
                    find_series_by_title,
                    pattern="^" + FIND_SERIES_BY_TITLE + "$",
                ),
                CallbackQueryHandler(
                    find_series_by_title_beginning,
                    pattern="^" + FIND_SERIES_BY_TITLE_BEGINNING + "$",
                ),
            ],
            LIST_SERIES: [
                CallbackQueryHandler(series_menu, pattern="^" + BACK + "$")
            ],
            FIND_SERIES_BY_TITLE: [
                CallbackQueryHandler(series_menu, pattern="^" + BACK + "$")
            ],
            FIND_SERIES_BY_TITLE_BEGINNING: [
                CallbackQueryHandler(series_menu, pattern="^" + BACK + "$")
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(END) + "$"
            ),
        ],
        map_to_parent={END: MENU, STOPPING: END,},
    )

    menu_handlers = [
        characters_conv,
        comics_conv,
        events_conv,
        series_conv,
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: menu_handlers,
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
        ],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    config = Config()
    fetcher = Fetcher(config)
    main(config.bot_token, fetcher)
