import logging

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
)
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
ASK_FOR_INPUT = "ASK_FOR_INPUT"
TYPING = "TYPING"
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
        [InlineKeyboardButton(text="Finish", callback_data=END)],
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
    if "data" in context.user_data:
        del context.user_data["data"]

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
                callback_data=FIND_CHARACTER_BY_NAME
            ),
            InlineKeyboardButton(
                text="Find character by name beginning",
                callback_data=FIND_CHARACTER_BY_NAME_BEGINNING
            ),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=END),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    logger.info("characters")
    if context.user_data.get("MSG_DELETED"):
        del context.user_data["MSG_DELETED"]
        logger.info(context.user_data.get("MSG_DELETED"))
        context.bot.send_message(
            update.callback_query.message.chat_id,
            text=text,
            reply_markup=keyboard,
        )
    else:
        update.callback_query.answer()
        logger.info(
            f"update callbackquery mesage text {update.callback_query.message.text}"
        )
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    logger.info("returning characters")
    return CHARACTERS


def comics_menu(update: Update, context: CallbackContext) -> str:
    if "data" in context.user_data:
        del context.user_data["data"]

    context.bot_data["list_comics_offset"] = 0

    text = (
        "You may request list of comics (in alphabetical order), "
        "try to find comic by exact title or by its beginning."
    )
    buttons = [
        [InlineKeyboardButton(text="List Comics", callback_data=LIST_COMICS),],
        [
            InlineKeyboardButton(
                text="Find comic by title", callback_data=FIND_COMIC_BY_TITLE
            ),
            InlineKeyboardButton(
                text="Find comic by title beginning",
                callback_data=FIND_COMIC_BY_TITLE_BEGINNING
            ),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=END),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    logger.info("comics")
    if context.user_data.get("MSG_DELETED"):
        del context.user_data["MSG_DELETED"]
        logger.info(context.user_data.get("MSG_DELETED"))
        context.bot.send_message(
            update.callback_query.message.chat_id,
            text=text,
            reply_markup=keyboard,
        )
    else:
        update.callback_query.answer()
        logger.info(
            f"update callbackquery message text {update.callback_query.message.text}"
        )
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
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
                text="Find event by name", callback_data=FIND_EVENT_BY_NAME
            ),
            InlineKeyboardButton(
                text="Find event by name beginning",
                callback_data=FIND_EVENT_BY_NAME_BEGINNING
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
                callback_data=FIND_SERIES_BY_TITLE
            ),
            InlineKeyboardButton(
                text="Find series by title beginning",
                callback_data=FIND_SERIES_BY_TITLE_BEGINNING
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
    context.user_data["characters"] = characters
    chars = sorted([character.name for character in characters])
    buttons = [
        [InlineKeyboardButton(text=char_, callback_data=char_)]
        for char_ in chars
    ]
    page_buttons = []
    if offset:
        page_buttons.append(
            InlineKeyboardButton(text="Prev", callback_data=PREV_PAGE),
        )
    if has_more_pages:
        page_buttons.append(
            InlineKeyboardButton(text="Next", callback_data=NEXT_PAGE)
        )
    buttons.append(page_buttons)
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK),
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


def show_character(update: Update, context: CallbackContext):
    character = None
    for ch in context.user_data["characters"]:
        if ch.name == update.callback_query.data:
            character = ch
            break
    if character:
        ch_name = character.name
        description = character.description
        wiki = f"wiki link: {character.wiki['url'].split('?utm')[0]}"
        detail = f"comics link: {character.detail['url'].split('?utm')[0]}"

        caption = "\n\n".join((ch_name, description, wiki, detail))
        context.bot.send_photo(
            update.callback_query.message.chat_id,
            character.img_link,
            caption=caption,
        )

    logger.info(update.callback_query.message)
    update.callback_query.delete_message()
    context.user_data["MSG_DELETED"] = True

    return characters_menu(update, context)


def show_comic(update: Update, context: CallbackContext):
    comic = None
    for comic_ in context.user_data["comics"]:

        if comic_.title[:64] == update.callback_query.data:
            comic = comic_
            break

    if comic:
        logger.info(
            f"comic page count {comic.page_count} and type {comic.page_count}"
        )
        page_count = f"Page count: {comic.page_count if comic.page_count else 'Unknown'}"
        detail = f"detail link: {comic.detail['url'].split('?utm')[0]}"
        caption = "\n\n".join(
            (
                comic.title,
                comic.description,
                page_count,
                detail,
                "Creators: " + "\n".join((str(creator) for creator in comic.creators)),
            )
        )
        context.bot.send_photo(
            update.callback_query.message.chat_id,
            comic.img_link,
            caption=caption,
        )

    logger.info(update.callback_query.message)
    update.callback_query.delete_message()
    context.user_data["MSG_DELETED"] = True

    return comics_menu(update, context)


def list_previous_characters(update: Update, context: CallbackContext):
    limit = 10
    current_offset = context.bot_data["list_characters_offset"]
    subtract_value = limit + (current_offset % 10 or limit)

    context.bot_data["list_characters_offset"] -= subtract_value
    return list_characters(update, context)


def list_previous_characters_from_name_beginning(
    update: Update, context: CallbackContext
):
    limit = 10
    current_offset = context.bot_data["list_characters_offset"]
    subtract_value = limit + (current_offset % 10 or limit)

    context.bot_data["list_characters_offset"] -= subtract_value
    return find_character_by_name_beginning(update, context)


def find_character_by_name(update: Update, context: CallbackContext):
    logger.info("Find character by name")
    if (name := context.user_data.get("data")) :

        logger.info(f"name is {name}")
        fetcher = context.bot_data["fetcher"]

        fetched_data = fetcher.list_features(Route.CHARACTERS, name=name)
        characters = fetched_data["features"]

        if characters:
            ch = characters[0]
            ch_name = ch.name
            description = ch.description
            wiki = f"wiki link: {ch.wiki['url'].split('?utm')[0]}"
            detail = f"comics link {ch.detail['url'].split('?utm')[0]}"

            caption = "\n\n".join((ch_name, description, wiki, detail))
            update.message.reply_photo(ch.img_link, caption=caption)

        else:
            text = f"Sorry, I didn't found anything for {name}. Maybe you should try find character by name beginning"
            update.message.reply_text(text=text)
        buttons = [
            [
                InlineKeyboardButton(
                    text="List Characters", callback_data=LIST_CHARACTERS
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Find character by name",
                    callback_data=FIND_CHARACTER_BY_NAME
                ),
                InlineKeyboardButton(
                    text="Find character by name beginning",
                    callback_data=FIND_CHARACTER_BY_NAME_BEGINNING
                ),
            ],
            [
                InlineKeyboardButton(text="Back", callback_data=END),
                InlineKeyboardButton(text="Done", callback_data=END),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        text = (
            "You may search information about characters, comics, series, "
            "events and etc.To abort, simply type /stop."
        )
        update.message.reply_text(text=text, reply_markup=keyboard)
        if "data" in context.user_data:
            del context.user_data["data"]
    else:
        context.user_data["input_for"] = FIND_CHARACTER_BY_NAME
        return ask_for_input(update, context)

    return FIND_CHARACTER_BY_NAME


def find_character_by_name_beginning(update: Update, context: CallbackContext):
    logger.info("Find character by name beginning")

    if (name_beginning := context.user_data.get("data")) :
        logger.info(f"name beginning is {name_beginning}")
        limit = 10
        offset = context.bot_data.get("list_characters_offset", 0)

        fetcher = context.bot_data["fetcher"]
        fetched_data = fetcher.list_features(
            Route.CHARACTERS,
            nameStartsWith=name_beginning,
            limit=limit,
            offset=offset,
        )
        logger.info(f"{limit + offset} and total {fetched_data['total']}")
        has_more_pages = limit + offset < fetched_data["total"]

        characters = fetched_data["features"]
        context.user_data["characters"] = characters

        chars = sorted([character.name for character in characters])
        buttons = [
            [InlineKeyboardButton(text=char_, callback_data=char_)]
            for char_ in chars
        ]
        page_buttons = []
        if offset:
            page_buttons.append(
                InlineKeyboardButton(text="Prev", callback_data=PREV_PAGE)
            )
        if has_more_pages:
            page_buttons.append(
                InlineKeyboardButton(text="Next", callback_data=NEXT_PAGE)
            )
        buttons.append(page_buttons)
        buttons.append(
            [
                InlineKeyboardButton(text="Back", callback_data=BACK),
                InlineKeyboardButton(text="Done", callback_data=END),
            ],
        )
        context.bot_data["list_characters_offset"] = offset + min(
            limit, fetched_data["count"]
        )
        keyboard = InlineKeyboardMarkup(buttons)
        text = (
            " ".join(chars)
            if chars
            else f"Sorry, I didn't found anything for {name_beginning}."
        )

        if update.message:

            update.message.reply_text(text=text, reply_markup=keyboard)
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text, reply_markup=keyboard
            )
    else:
        context.user_data["input_for"] = FIND_CHARACTER_BY_NAME_BEGINNING
        return ask_for_input(update, context)
    return FIND_CHARACTER_BY_NAME_BEGINNING


def list_comics(update: Update, context: CallbackContext):
    logger.info("List comics command")
    limit = 10
    fetcher = context.bot_data["fetcher"]
    offset = context.bot_data.get("list_comics_offset", 0)
    fetched_data = fetcher.list_features(
        Route.COMICS, limit=limit, offset=offset
    )
    logger.info(f"{limit + offset} and total {fetched_data['total']}")
    has_more_pages = limit + offset < fetched_data["total"]

    comics = fetched_data["features"]
    context.user_data["comics"] = comics
    sorted_comics = sorted([comic.title for comic in comics])


    buttons = [
        [InlineKeyboardButton(text=comic, callback_data=comic[:64])]
        for comic in sorted_comics
    ]
    page_buttons = []
    if offset:
        page_buttons.append(
            InlineKeyboardButton(text="Prev", callback_data=PREV_PAGE)
        )
    if has_more_pages:
        page_buttons.append(
            InlineKeyboardButton(text="Next", callback_data=NEXT_PAGE)
        )
    buttons.append(page_buttons)
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    )

    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text="\n".join(sorted_comics), reply_markup=keyboard
    )
    context.bot_data["list_comics_offset"] = offset + min(
        limit, fetched_data["count"]
    )
    return LIST_COMICS


def list_previous_comics(update: Update, context: CallbackContext):
    limit = 10
    current_offset = context.bot_data["list_comics_offset"]
    subtract_value = limit + (current_offset % 10 or limit)

    context.bot_data["list_comics_offset"] -= subtract_value
    return list_comics(update, context)

def find_comic_by_title(update: Update, context: CallbackContext):
    logger.info("Find comic by title ")

    if (title := context.user_data.get("data")):
        logger.info(f"title is {title}")
        limit = 10
        offset = context.bot_data.get("list_comics_offset", 0)

        fetcher = context.bot_data["fetcher"]
        fetched_data = fetcher.list_features(
            Route.COMICS,
            title=title,
            limit=limit,
            offset=offset,
        )
        logger.info(f"{limit + offset} and total {fetched_data['total']}")
        has_more_pages = limit + offset < fetched_data["total"]

        comics = fetched_data["features"]
        context.user_data["comics"] = comics

        sorted_comics = sorted([comic.title for comic in comics])
        buttons = [
            [InlineKeyboardButton(text=comic, callback_data=comic)]
            for comic in sorted_comics
        ]
        page_buttons = []
        if offset:
            page_buttons.append(
                InlineKeyboardButton(text="Prev", callback_data=PREV_PAGE),
            )
        if has_more_pages:
            page_buttons.append(
                InlineKeyboardButton(text="Next",
                                      callback_data=NEXT_PAGE)
            )
        if page_buttons:
            buttons.append(page_buttons)
        if not buttons:
            buttons = [
                [
                    InlineKeyboardButton(
                        text="List Comics", callback_data=LIST_COMICS
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Find comic by title",
                        callback_data=FIND_COMIC_BY_TITLE
                    ),
                    InlineKeyboardButton(
                        text="Find title by title beginning",
                        callback_data=FIND_COMIC_BY_TITLE_BEGINNING
                    ),
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=END),
                    InlineKeyboardButton(text="Done", callback_data=END),
                ],
            ]
            if "data" in context.user_data:
                del context.user_data["data"]
            text = f"Sorry, I didn't found anything for {title}. Maybe you should try find comic by title beginning"
            update.message.reply_text(text=text)
            text = (
                "You may request list of comics (in alphabetical order), "
                "try to find comic by exact title or by its beginning."
            )
        else:
            text = (
                " ".join(sorted_comics)
                if comics
                else f"Sorry, I didn't found anything for {title} "
                     f"Maybe you should try find comic by title beginning."
            )
            buttons.append(
                [
                    InlineKeyboardButton(text="Back", callback_data=BACK),
                    InlineKeyboardButton(text="Done", callback_data=END),
                ],
            )
        context.bot_data["list_comics_offset"] = offset + min(
            limit, fetched_data["count"]
        )
        keyboard = InlineKeyboardMarkup(buttons)


        if update.message:
            update.message.reply_text(text=text, reply_markup=keyboard)
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text, reply_markup=keyboard
            )
    else:
        context.user_data["input_for"] = FIND_COMIC_BY_TITLE
        return ask_for_input(update, context)
    return FIND_COMIC_BY_TITLE


def find_comic_by_title_beginning(update: Update, context: CallbackContext):
    logger.info("Find comic by title beginning")

    if (title_beginning := context.user_data.get("data")) :
        logger.info(f"title beginning is {title_beginning}")
        limit = 10
        offset = context.bot_data.get("list_comics_offset", 0)

        fetcher = context.bot_data["fetcher"]
        fetched_data = fetcher.list_features(
            Route.COMICS,
            titleStartsWith=title_beginning,
            limit=limit,
            offset=offset,
        )
        logger.info(f"{limit + offset} and total {fetched_data['total']}")
        has_more_pages = limit + offset < fetched_data["total"]

        comics = fetched_data["features"]
        context.user_data["comics"] = comics

        sorted_comics = sorted([comic.title for comic in comics])
        buttons = [
            [InlineKeyboardButton(text=comic, callback_data=comic)]
            for comic in sorted_comics
        ]
        page_buttons = []
        if offset:
            page_buttons.append(
                InlineKeyboardButton(text="Prev", callback_data=PREV_PAGE),
            )
        if has_more_pages:
            page_buttons.append(
                InlineKeyboardButton(text="Next", callback_data=NEXT_PAGE)
            )
        if page_buttons:
            buttons.append(page_buttons)
        if not buttons:
            if "data" in context.user_data:
                del context.user_data["data"]
            buttons = [
                [
                    InlineKeyboardButton(
                        text="List Comics", callback_data=LIST_COMICS
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Find comic by title",
                        callback_data=FIND_COMIC_BY_TITLE
                    ),
                    InlineKeyboardButton(
                        text="Find title by title beginning",
                        callback_data=FIND_COMIC_BY_TITLE_BEGINNING
                    ),
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=END),
                    InlineKeyboardButton(text="Done", callback_data=END),
                ],
            ]
            text = f"Sorry, I didn't found anything for {title_beginning}"
            if update.message:
                update.message.reply_text(text=text)
            else:
                update.callback_query.answer()
                update.callback_query.edit_message_text(
                    text=text
                )
            text = (
                "You may request list of comics (in alphabetical order), "
                "try to find comic by exact title or by its beginning."
            )
        else:
            text = (
                " ".join(sorted_comics)
                if comics
                else f"Sorry, I didn't found anything for {title_beginning} "
            )
            buttons.append(
                [
                    InlineKeyboardButton(text="Back", callback_data=BACK),
                    InlineKeyboardButton(text="Done", callback_data=END),
                ],
            )
        context.bot_data["list_comics_offset"] = offset + min(
            limit, fetched_data["count"]
        )
        keyboard = InlineKeyboardMarkup(buttons)


        if update.message:

            update.message.reply_text(text=text, reply_markup=keyboard)
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text, reply_markup=keyboard
            )
    else:
        context.user_data["input_for"] = FIND_COMIC_BY_TITLE_BEGINNING
        return ask_for_input(update, context)
    return FIND_COMIC_BY_TITLE_BEGINNING


def list_previous_comics_from_title_beginning(
    update: Update, context: CallbackContext
):
    limit = 10
    current_offset = context.bot_data["list_comics_offset"]
    subtract_value = limit + (current_offset % 10 or limit)

    context.bot_data["list_comics_offset"] -= subtract_value
    return find_comic_by_title_beginning(update, context)

def list_previous_comics_from_title(
    update: Update, context: CallbackContext
):
    limit = 10
    current_offset = context.bot_data["list_comics_offset"]
    subtract_value = limit + (current_offset % 10 or limit)

    context.bot_data["list_comics_offset"] -= subtract_value
    return find_comic_by_title(update, context)

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
        [InlineKeyboardButton(text=event, callback_data=LIST_EVENTS)]
        for event in events
    ]
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK),
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
            InlineKeyboardButton(text=event, callback_data=FIND_EVENT_BY_NAME)
            for event in events
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK),
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
                text=event, callback_data=FIND_EVENT_BY_NAME_BEGINNING
            )
            for event in events
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=BACK),
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
        [InlineKeyboardButton(text=single_series, callback_data=LIST_SERIES)]
        for single_series in series
    ]
    buttons.append(
        [
            InlineKeyboardButton(text="Back", callback_data=BACK),
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
            InlineKeyboardButton(text="Back", callback_data=BACK),
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
            InlineKeyboardButton(text="Back", callback_data=BACK),
            InlineKeyboardButton(text="Done", callback_data=END),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=" ".join(series), reply_markup=keyboard
    )

    return FIND_SERIES_BY_TITLE_BEGINNING


def select_feature(feature, update: Update, context: CallbackContext):
    features = {
        FIND_CHARACTER_BY_NAME: find_character_by_name,
        FIND_CHARACTER_BY_NAME_BEGINNING: find_character_by_name_beginning,
        FIND_COMIC_BY_TITLE: find_comic_by_title,
        FIND_COMIC_BY_TITLE_BEGINNING: find_comic_by_title_beginning,
        FIND_EVENT_BY_NAME: find_event_by_name,
        FIND_EVENT_BY_NAME_BEGINNING: find_event_by_name_beginning,
        FIND_SERIES_BY_TITLE: find_series_by_title,
        FIND_SERIES_BY_TITLE_BEGINNING: find_series_by_title_beginning,
    }
    logger.info(f"selected feature is {feature}")
    return features[feature](update, context)


def save_input(update: Update, context: CallbackContext) -> str:
    logger.info("save input")
    """Save input for feature and return to feature selection."""
    context.user_data["data"] = update.message.text

    logger.info("return select feature")
    logger.info(f'input for {context.user_data["input_for"]}')
    return select_feature(context.user_data["input_for"], update, context)


def ask_for_input(update: Update, context: CallbackContext) -> str:
    logger.info("ask for input")
    """Prompt user to input data for selected feature."""
    context.user_data["data"] = update.callback_query.data
    text = "Okay, tell me."
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    logger.info("return typing")
    return ASK_FOR_INPUT


def debug(update, context):
    logger.critical("wooow")
    update.callback_query.answer(text="wooow")


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
            ASK_FOR_INPUT: [
                MessageHandler(Filters.text & ~Filters.command, save_input),
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
                CallbackQueryHandler(
                    show_character, pattern="^(?!-1).+$",
                ),
            ],
            FIND_CHARACTER_BY_NAME: [
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + FIND_CHARACTER_BY_NAME + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^" + FIND_CHARACTER_BY_NAME_BEGINNING + "$",
                ),
                CallbackQueryHandler(
                    list_characters, pattern="^" + LIST_CHARACTERS + "$"
                ),
                CallbackQueryHandler(
                    characters_menu, pattern="^" + BACK + "$"
                ),
            ],
            FIND_CHARACTER_BY_NAME_BEGINNING: [
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + FIND_CHARACTER_BY_NAME + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^" + FIND_CHARACTER_BY_NAME_BEGINNING + "$",
                ),
                CallbackQueryHandler(
                    list_characters, pattern="^" + LIST_CHARACTERS + "$"
                ),
                CallbackQueryHandler(
                    characters_menu, pattern="^" + BACK + "$"
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^" + NEXT_PAGE + "$",
                ),
                CallbackQueryHandler(
                    list_previous_characters_from_name_beginning,
                    pattern="^" + PREV_PAGE + "$",
                ),
                CallbackQueryHandler(
                    show_character, pattern="^(?!-1).+$",
                ),
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
            ASK_FOR_INPUT: [
                MessageHandler(Filters.text & ~Filters.command, save_input),
            ],
            LIST_COMICS: [
                CallbackQueryHandler(comics_menu, pattern="^" + BACK + "$"),
                CallbackQueryHandler(
                    list_comics, pattern="^" + NEXT_PAGE + "$",
                ),
                CallbackQueryHandler(
                    list_previous_comics, pattern="^" + PREV_PAGE + "$",
                ),
                CallbackQueryHandler(show_comic, pattern="^(?!-1).+$",),
            ],
            FIND_COMIC_BY_TITLE: [
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + FIND_COMIC_BY_TITLE + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^" + FIND_COMIC_BY_TITLE_BEGINNING + "$",
                ),
                CallbackQueryHandler(
                    list_comics, pattern="^" + LIST_COMICS + "$"
                ),
                CallbackQueryHandler(comics_menu, pattern="^" + BACK + "$"),
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + NEXT_PAGE + "$",
                ),
                CallbackQueryHandler(
                    list_previous_comics_from_title,
                    pattern="^" + PREV_PAGE + "$",
                ),
                CallbackQueryHandler(show_comic, pattern="^(?!-1).+$", ),
            ],
            FIND_COMIC_BY_TITLE_BEGINNING: [
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + FIND_COMIC_BY_TITLE + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^" + FIND_COMIC_BY_TITLE_BEGINNING + "$",
                ),
                CallbackQueryHandler(
                    list_comics, pattern="^" + LIST_COMICS + "$"
                ),
                CallbackQueryHandler(comics_menu, pattern="^" + BACK + "$"),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^" + NEXT_PAGE + "$",
                ),
                CallbackQueryHandler(
                    list_previous_comics_from_title_beginning,
                    pattern="^" + PREV_PAGE + "$",
                ),
                CallbackQueryHandler(show_comic, pattern="^(?!-1).+$",),
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
