import enum
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


START_OVER = "START_OVER"
MSG_DELETED = "MSG_DELETED"
OFFSET = "OFFSET"
DATA = "DATA"
INPUT_FOR = "INPUT_FOR"
FETCHER = "FETCHER"
FEATURES = "FEATURES"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class States(enum.Enum):
    MENU = "MENU"
    STOPPING = "STOPPING"
    BACK = "BACK"
    NEXT_PAGE = "NEXT_PAGE"
    PREV_PAGE = "PREV_PAGE"
    ASK_FOR_INPUT = "ASK_FOR_INPUT"
    TYPING = "TYPING"
    CHARACTERS = "CHARACTERS"
    COMICS = "COMICS"
    SERIES = "SERIES"
    EVENTS = "EVENTS"
    LIST_CHARACTERS = "LIST_CHARACTERS"
    FIND_CHARACTER_BY_NAME = "FIND_CHARACTER_BY_NAME"
    FIND_CHARACTER_BY_NAME_BEGINNING = "FIND_CHARACTER_BY_NAME_BEGINNING"
    LIST_COMICS = "LIST_COMICS"
    FIND_COMIC_BY_TITLE = "FIND_COMIC_BY_TITLE"
    FIND_COMIC_BY_TITLE_BEGINNING = "FIND_COMIC_BY_TITLE_BEGINNING"
    LIST_EVENTS = "LIST_EVENTS"
    FIND_EVENT_BY_NAME = "FIND_EVENT_BY_NAME"
    FIND_EVENT_BY_NAME_BEGINNING = "FIND_EVENT_BY_NAME_BEGINNING"
    LIST_SERIES = "LIST_SERIES"
    FIND_SERIES_BY_TITLE = "FIND_SERIES_BY_TITLE"
    FIND_SERIES_BY_TITLE_BEGINNING = "FIND_SERIES_BY_TITLE_BEGINNING"
    END = str(ConversationHandler.END)


class _CustomKeyboard:

    CALLBACK_DATA_MAX_LENGTH = 64

    @staticmethod
    def main_menu():
        buttons = [
            [
                InlineKeyboardButton(
                    text="Characters", callback_data=States.CHARACTERS.value
                ),
                InlineKeyboardButton(
                    text="Comics", callback_data=States.COMICS.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Events", callback_data=States.EVENTS.value
                ),
                InlineKeyboardButton(
                    text="Series", callback_data=States.SERIES.value
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Finish", callback_data=States.END.value
                )
            ],
        ]

        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def _inner_menu(
        features, list_state, find_by_name_state, find_by_name_beginning_state
    ):
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"List {features}", callback_data=list_state,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Find by name", callback_data=find_by_name_state,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Find by name beginning",
                    callback_data=find_by_name_beginning_state,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Back", callback_data=States.END.value
                ),
                InlineKeyboardButton(
                    text="Done", callback_data=States.END.value
                ),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        return keyboard

    @classmethod
    def characters_menu(cls):
        return cls._inner_menu(
            "Characters",
            States.LIST_CHARACTERS.value,
            States.FIND_CHARACTER_BY_NAME.value,
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value,
        )

    @classmethod
    def comics_menu(cls):
        return cls._inner_menu(
            "Comics",
            States.LIST_COMICS.value,
            States.FIND_COMIC_BY_TITLE.value,
            States.FIND_COMIC_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def events_menu(cls):
        return cls._inner_menu(
            "Events",
            States.LIST_EVENTS.value,
            States.FIND_EVENT_BY_NAME.value,
            States.FIND_EVENT_BY_NAME_BEGINNING.value,
        )

    @classmethod
    def series_menu(cls):
        return cls._inner_menu(
            "Series",
            States.LIST_SERIES.value,
            States.FIND_SERIES_BY_TITLE.value,
            States.FIND_SERIES_BY_TITLE_BEGINNING.value,
        )

    @classmethod
    def keyboard_from_iterable(cls, iterable, prev_required, next_required):
        if not iterable:
            return None
        buttons = [
            [
                InlineKeyboardButton(
                    text=item,
                    callback_data=item[: cls.CALLBACK_DATA_MAX_LENGTH],
                )
            ]
            for item in iterable
        ]
        page_buttons = []
        if prev_required:
            page_buttons.append(
                InlineKeyboardButton(
                    text="Prev", callback_data=States.PREV_PAGE.value
                ),
            )
        if next_required:
            page_buttons.append(
                InlineKeyboardButton(
                    text="Next", callback_data=States.NEXT_PAGE.value
                )
            )
        buttons.append(page_buttons)
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Back", callback_data=States.BACK.value
                ),
                InlineKeyboardButton(
                    text="Done", callback_data=States.END.value
                ),
            ],
        )
        keyboard = InlineKeyboardMarkup(buttons)
        return keyboard


class CustomKeyboard(_CustomKeyboard):
    main_menu = _CustomKeyboard.main_menu()
    characters_menu = _CustomKeyboard.characters_menu()
    comics_menu = _CustomKeyboard.comics_menu()
    events_menu = _CustomKeyboard.events_menu()
    series_menu = _CustomKeyboard.series_menu()


class _Text:
    greetings = (
        "Hi, I'm Marvel Bot and I'm here to help you gather "
        "information about Marvel Universe."
    )

    stop = "Okay, bye."
    end = "See you around!"
    ask_for_input = "Okay, tell me."

    @staticmethod
    def menu():
        return (
            "You may search information about characters, comics, series, "
            "events and etc.To abort, simply type /stop."
        )

    @staticmethod
    def _inner_menu(features, criterion):
        text = f"You may request list of {features} (in alphabetical order), try to find {features} by exact {criterion} or by its beginning"
        return text

    @classmethod
    def characters_menu(cls):
        return cls._inner_menu("characters", "name")

    @classmethod
    def comics_menu(cls):
        return cls._inner_menu("comics", "title")

    @classmethod
    def events_menu(cls):
        return cls._inner_menu("events", "name")

    @classmethod
    def series_menu(cls):
        return cls._inner_menu("series", "title")

    @staticmethod
    def not_found_by_name(name):
        return f"Sorry, I didn't found anything for {name}."

    @staticmethod
    def from_container(container, sep="\n"):
        return sep.join(container)


class Text(_Text):
    menu = _Text.menu()
    characters_menu = _Text.characters_menu()
    comics_menu = _Text.comics_menu()
    events_menu = _Text.events_menu()
    series_menu = _Text.series_menu()


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
        return characters_menu(update, context)

    @classmethod
    def send_comic(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.comic_content)
        return comics_menu(update, context)

    @classmethod
    def send_event(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.event_content)
        return events_menu(update, context)

    @classmethod
    def send_series(cls, update: Update, context: CallbackContext):
        cls.send_feature(update, context, cls.series_content)
        return series_menu(update, context)


def start(update: Update, context: CallbackContext):
    text = Text.menu

    if context.chat_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text, reply_markup=CustomKeyboard.main_menu
        )
    else:
        update.message.reply_text(Text.greetings)
        update.message.reply_text(
            text=text, reply_markup=CustomKeyboard.main_menu
        )
    context.chat_data[START_OVER] = False
    return States.MENU.value


def _inner_menu(update: Update, context: CallbackContext, text, keyboard):
    context.chat_data[OFFSET] = 0

    if context.chat_data.get(DATA):
        del context.chat_data[DATA]

    if context.chat_data.get(MSG_DELETED):
        del context.chat_data[MSG_DELETED]

        context.bot.send_message(
            update.callback_query.message.chat_id,
            text=text,
            reply_markup=keyboard,
        )
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )


def characters_menu(update: Update, context: CallbackContext) -> str:
    _inner_menu(
        update, context, Text.characters_menu, CustomKeyboard.characters_menu
    )
    return States.CHARACTERS.value


def comics_menu(update: Update, context: CallbackContext) -> str:
    _inner_menu(update, context, Text.comics_menu, CustomKeyboard.comics_menu)
    return States.COMICS.value


def events_menu(update: Update, context: CallbackContext) -> str:
    _inner_menu(update, context, Text.events_menu, CustomKeyboard.events_menu)
    return States.EVENTS.value


def series_menu(update: Update, context: CallbackContext) -> str:
    _inner_menu(update, context, Text.series_menu, CustomKeyboard.series_menu)
    return States.SERIES.value


def _list_features(update: Update, context: CallbackContext, route):
    text, keyboard = _request_features(context, route)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


def _find_feature_by_name(
    update: Update,
    context: CallbackContext,
    route,
    filter_key,
    menu_keyboard,
    menu_text,
    return_state,
):
    if not (value := context.chat_data.get(DATA)):
        context.chat_data[INPUT_FOR] = return_state
        return ask_for_input(update, context)

    text, keyboard = _request_features(context, route, **{filter_key: value})

    if not keyboard:
        keyboard = menu_keyboard

        if DATA in context.chat_data:
            del context.chat_data[DATA]
        text = Text.not_found_by_name(value)
        update.message.reply_text(text=text)
        text = menu_text

    if update.message:
        update.message.reply_text(text=text, reply_markup=keyboard)
    else:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )

    return return_state


def _request_features(context, route, **kwargs):
    limit = 10

    fetcher_ = context.bot_data[FETCHER]
    offset = context.chat_data.get(OFFSET, 0)
    fetched_data = fetcher_.list_features(
        route, limit=limit, offset=offset, **kwargs
    )
    logger.info(f"{limit + offset} and total {fetched_data.total}")

    has_more_pages = limit + offset < fetched_data.total

    features = fetched_data.features
    context.chat_data[FEATURES] = features

    sorted_features = sorted(
        [
            getattr(feature, "name", getattr(feature, "title", ""))
            for feature in features
        ]
    )
    keyboard = CustomKeyboard.keyboard_from_iterable(
        sorted_features, bool(offset), has_more_pages
    )
    text = Text.from_container(sorted_features)
    context.chat_data[OFFSET] = offset + min(limit, fetched_data.count)

    return text, keyboard


def list_characters(update: Update, context: CallbackContext):
    logger.info("List characters command")
    _list_features(update, context, Route.CHARACTERS)
    return States.LIST_CHARACTERS.value


def _list_previous_features(context: CallbackContext):
    limit = 10
    current_offset = context.chat_data[OFFSET]
    subtract_value = limit + (current_offset % 10 or limit)
    context.chat_data[OFFSET] -= subtract_value


def list_previous_characters(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return list_characters(update, context)


def list_previous_characters_from_name(
    update: Update, context: CallbackContext
):
    _list_previous_features(context)
    return find_character_by_name(update, context)


def list_previous_characters_from_name_beginning(
    update: Update, context: CallbackContext
):
    _list_previous_features(context)
    return find_character_by_name_beginning(update, context)


def find_character_by_name(update: Update, context: CallbackContext):
    logger.info("Find character by name")
    return _find_feature_by_name(
        update,
        context,
        Route.CHARACTERS,
        "name",
        CustomKeyboard.characters_menu,
        Text.characters_menu,
        States.FIND_CHARACTER_BY_NAME.value,
    )


def find_character_by_name_beginning(update: Update, context: CallbackContext):
    logger.info("Find character by name beginning")
    return _find_feature_by_name(
        update,
        context,
        Route.CHARACTERS,
        "nameStartsWith",
        CustomKeyboard.characters_menu,
        Text.characters_menu,
        States.FIND_CHARACTER_BY_NAME_BEGINNING.value,
    )


def list_comics(update: Update, context: CallbackContext):
    logger.info("List comics command")
    _list_features(update, context, Route.COMICS)
    return States.LIST_COMICS.value


def list_previous_comics(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return list_comics(update, context)


def find_comic_by_title(update: Update, context: CallbackContext):
    logger.info("Find comic by title")
    return _find_feature_by_name(
        update,
        context,
        Route.COMICS,
        "title",
        CustomKeyboard.comics_menu,
        Text.comics_menu,
        States.FIND_COMIC_BY_TITLE.value,
    )


def find_comic_by_title_beginning(update: Update, context: CallbackContext):
    logger.info("Find comic by title beginning")
    return _find_feature_by_name(
        update,
        context,
        Route.COMICS,
        "titleStartsWith",
        CustomKeyboard.comics_menu,
        Text.comics_menu,
        States.FIND_COMIC_BY_TITLE_BEGINNING.value,
    )


def list_previous_comics_from_title_beginning(
    update: Update, context: CallbackContext
):
    _list_previous_features(context)
    return find_comic_by_title_beginning(update, context)


def list_previous_comics_from_title(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return find_comic_by_title(update, context)


def list_events(update: Update, context: CallbackContext):
    logger.info("List events command")
    _list_features(update, context, Route.EVENTS)
    return States.LIST_EVENTS.value


def list_previous_events(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return list_events(update, context)


def find_event_by_name(update: Update, context: CallbackContext):
    logger.info("Find event by name")
    return _find_feature_by_name(
        update,
        context,
        Route.EVENTS,
        "name",
        CustomKeyboard.events_menu,
        Text.comics_menu,
        States.FIND_EVENT_BY_NAME.value,
    )


def find_event_by_name_beginning(update: Update, context: CallbackContext):
    logger.info("Find character by name beginning")
    return _find_feature_by_name(
        update,
        context,
        Route.EVENTS,
        "nameStartsWith",
        CustomKeyboard.events_menu,
        Text.comics_menu,
        States.FIND_EVENT_BY_NAME_BEGINNING.value,
    )


def list_previous_events_from_name_beginning(
    update: Update, context: CallbackContext
):
    _list_previous_features(context)
    return find_event_by_name_beginning(update, context)


def list_previous_events_from_name(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return find_event_by_name(update, context)


def list_series(update: Update, context: CallbackContext):
    logger.info("List series command")
    _list_features(update, context, Route.SERIES)
    return States.LIST_SERIES.value


def list_previous_series(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return list_series(update, context)


def find_series_by_title(update: Update, context: CallbackContext):
    logger.info("Find series by title")
    return _find_feature_by_name(
        update,
        context,
        Route.SERIES,
        "title",
        CustomKeyboard.series_menu,
        Text.series_menu,
        States.FIND_SERIES_BY_TITLE.value,
    )


def find_series_by_title_beginning(update: Update, context: CallbackContext):
    logger.info("Find series by title beginning")
    return _find_feature_by_name(
        update,
        context,
        Route.SERIES,
        "titleStartsWith",
        CustomKeyboard.series_menu,
        Text.series_menu,
        States.FIND_SERIES_BY_TITLE_BEGINNING.value,
    )


def list_previous_series_from_title_beginning(
    update: Update, context: CallbackContext
):
    _list_previous_features(context)
    return find_series_by_title_beginning(update, context)


def list_previous_series_from_title(update: Update, context: CallbackContext):
    _list_previous_features(context)
    return find_series_by_title_beginning(update, context)


def select_feature(feature, update: Update, context: CallbackContext):
    features = {
        States.FIND_CHARACTER_BY_NAME.value: find_character_by_name,
        States.FIND_CHARACTER_BY_NAME_BEGINNING.value: find_character_by_name_beginning,
        States.FIND_COMIC_BY_TITLE.value: find_comic_by_title,
        States.FIND_COMIC_BY_TITLE_BEGINNING.value: find_comic_by_title_beginning,
        States.FIND_EVENT_BY_NAME.value: find_event_by_name,
        States.FIND_EVENT_BY_NAME_BEGINNING.value: find_event_by_name_beginning,
        States.FIND_SERIES_BY_TITLE.value: find_series_by_title,
        States.FIND_SERIES_BY_TITLE_BEGINNING.value: find_series_by_title_beginning,
    }
    logger.info(f"selected feature is {feature}")
    return features[feature](update, context)


def save_input(update: Update, context: CallbackContext) -> str:
    logger.info("save input")
    """Save input for feature and return to feature selection."""
    context.chat_data[DATA] = update.message.text

    logger.info("return select feature")
    logger.info(f"input for {context.chat_data[INPUT_FOR]}")
    return select_feature(context.chat_data[INPUT_FOR], update, context)


def ask_for_input(update: Update, context: CallbackContext) -> str:
    logger.info("ask for input")
    """Prompt user to input data for selected feature."""
    context.chat_data[DATA] = update.callback_query.data
    text = Text.ask_for_input
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    logger.info("return typing")
    return States.ASK_FOR_INPUT.value


def end_second_level(update: Update, context: CallbackContext):
    context.chat_data[OFFSET] = 0
    context.chat_data[START_OVER] = True
    start(update, context)
    return States.END.value


def stop(update: Update, _: CallbackContext):
    update.message.reply_text(Text.stop)
    return States.END.value


def end(update: Update, _: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=Text.end)
    return States.END.value


def main(bot_token, fetcher) -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data[FETCHER] = fetcher

    characters_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                characters_menu, pattern="^" + States.CHARACTERS.value + "$"
            )
        ],
        states={
            States.CHARACTERS.value: [
                CallbackQueryHandler(
                    list_characters,
                    pattern="^" + States.LIST_CHARACTERS.value + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + States.FIND_CHARACTER_BY_NAME.value + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^"
                    + States.FIND_CHARACTER_BY_NAME_BEGINNING.value
                    + "$",
                ),
            ],
            States.ASK_FOR_INPUT.value: [
                MessageHandler(Filters.text & ~Filters.command, save_input),
            ],
            States.LIST_CHARACTERS.value: [
                CallbackQueryHandler(
                    characters_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    list_characters,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_characters,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_character, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_CHARACTER_BY_NAME.value: [
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + States.FIND_CHARACTER_BY_NAME.value + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^"
                    + States.FIND_CHARACTER_BY_NAME_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_characters,
                    pattern="^" + States.LIST_CHARACTERS.value + "$",
                ),
                CallbackQueryHandler(
                    characters_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_characters_from_name,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_character, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_CHARACTER_BY_NAME_BEGINNING.value: [
                CallbackQueryHandler(
                    find_character_by_name,
                    pattern="^" + States.FIND_CHARACTER_BY_NAME.value + "$",
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^"
                    + States.FIND_CHARACTER_BY_NAME_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_characters,
                    pattern="^" + States.LIST_CHARACTERS.value + "$",
                ),
                CallbackQueryHandler(
                    characters_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_character_by_name_beginning,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_characters_from_name_beginning,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_character, pattern="^(?!-1).+$",
                ),
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(States.END.value) + "$"
            ),
        ],
        map_to_parent={
            States.END.value: States.MENU.value,
            States.STOPPING.value: States.END.value,
        },
    )

    comics_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                comics_menu, pattern="^" + States.COMICS.value + "$"
            )
        ],
        states={
            States.COMICS.value: [
                CallbackQueryHandler(
                    list_comics, pattern="^" + States.LIST_COMICS.value + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + States.FIND_COMIC_BY_TITLE.value + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^"
                    + States.FIND_COMIC_BY_TITLE_BEGINNING.value
                    + "$",
                ),
            ],
            States.ASK_FOR_INPUT.value: [
                MessageHandler(Filters.text & ~Filters.command, save_input),
            ],
            States.LIST_COMICS.value: [
                CallbackQueryHandler(
                    comics_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    list_comics, pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_comics,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_comic, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_COMIC_BY_TITLE.value: [
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + States.FIND_COMIC_BY_TITLE.value + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^"
                    + States.FIND_COMIC_BY_TITLE_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_comics, pattern="^" + States.LIST_COMICS.value + "$"
                ),
                CallbackQueryHandler(
                    comics_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_comics_from_title,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_comic, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_COMIC_BY_TITLE_BEGINNING.value: [
                CallbackQueryHandler(
                    find_comic_by_title,
                    pattern="^" + States.FIND_COMIC_BY_TITLE.value + "$",
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^"
                    + States.FIND_COMIC_BY_TITLE_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_comics, pattern="^" + States.LIST_COMICS.value + "$"
                ),
                CallbackQueryHandler(
                    comics_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_comic_by_title_beginning,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_comics_from_title_beginning,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_comic, pattern="^(?!-1).+$",
                ),
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(States.END.value) + "$"
            ),
        ],
        map_to_parent={
            States.END.value: States.MENU.value,
            States.STOPPING.value: States.END.value,
        },
    )

    events_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                events_menu, pattern="^" + States.EVENTS.value + "$"
            )
        ],
        states={
            States.EVENTS.value: [
                CallbackQueryHandler(
                    list_events, pattern="^" + States.LIST_EVENTS.value + "$",
                ),
                CallbackQueryHandler(
                    find_event_by_name,
                    pattern="^" + States.FIND_EVENT_BY_NAME.value + "$",
                ),
                CallbackQueryHandler(
                    find_event_by_name_beginning,
                    pattern="^"
                    + States.FIND_EVENT_BY_NAME_BEGINNING.value
                    + "$",
                ),
            ],
            States.ASK_FOR_INPUT.value: [
                MessageHandler(Filters.text & ~Filters.command, save_input),
            ],
            States.LIST_EVENTS.value: [
                CallbackQueryHandler(
                    events_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    list_events, pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_events,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_event, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_EVENT_BY_NAME.value: [
                CallbackQueryHandler(
                    find_event_by_name,
                    pattern="^" + States.FIND_EVENT_BY_NAME.value + "$",
                ),
                CallbackQueryHandler(
                    find_event_by_name_beginning,
                    pattern="^"
                    + States.FIND_EVENT_BY_NAME_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_events, pattern="^" + States.LIST_EVENTS.value + "$"
                ),
                CallbackQueryHandler(
                    events_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_event_by_name,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_events_from_name,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_event, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_EVENT_BY_NAME_BEGINNING.value: [
                CallbackQueryHandler(
                    find_event_by_name,
                    pattern="^" + States.FIND_EVENT_BY_NAME.value + "$",
                ),
                CallbackQueryHandler(
                    find_event_by_name_beginning,
                    pattern="^"
                    + States.FIND_EVENT_BY_NAME_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_events, pattern="^" + States.LIST_EVENTS.value + "$"
                ),
                CallbackQueryHandler(
                    events_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_event_by_name_beginning,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_events_from_name_beginning,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_event, pattern="^(?!-1).+$",
                ),
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(States.END.value) + "$"
            ),
        ],
        map_to_parent={
            States.END.value: States.MENU.value,
            States.STOPPING.value: States.END.value,
        },
    )

    series_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                series_menu, pattern="^" + States.SERIES.value + "$"
            )
        ],
        states={
            States.SERIES.value: [
                CallbackQueryHandler(
                    list_series, pattern="^" + States.LIST_SERIES.value + "$",
                ),
                CallbackQueryHandler(
                    find_series_by_title,
                    pattern="^" + States.FIND_SERIES_BY_TITLE.value + "$",
                ),
                CallbackQueryHandler(
                    find_series_by_title_beginning,
                    pattern="^"
                    + States.FIND_SERIES_BY_TITLE_BEGINNING.value
                    + "$",
                ),
            ],
            States.ASK_FOR_INPUT.value: [
                MessageHandler(Filters.text & ~Filters.command, save_input),
            ],
            States.LIST_SERIES.value: [
                CallbackQueryHandler(
                    series_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    list_series, pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_series,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_series, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_SERIES_BY_TITLE.value: [
                CallbackQueryHandler(
                    find_series_by_title,
                    pattern="^" + States.FIND_SERIES_BY_TITLE.value + "$",
                ),
                CallbackQueryHandler(
                    find_series_by_title_beginning,
                    pattern="^"
                    + States.FIND_SERIES_BY_TITLE_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_series, pattern="^" + States.LIST_SERIES.value + "$"
                ),
                CallbackQueryHandler(
                    series_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_series_by_title,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_series_from_title,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_series, pattern="^(?!-1).+$",
                ),
            ],
            States.FIND_SERIES_BY_TITLE_BEGINNING.value: [
                CallbackQueryHandler(
                    find_series_by_title,
                    pattern="^" + States.FIND_SERIES_BY_TITLE.value + "$",
                ),
                CallbackQueryHandler(
                    find_series_by_title_beginning,
                    pattern="^"
                    + States.FIND_SERIES_BY_TITLE_BEGINNING.value
                    + "$",
                ),
                CallbackQueryHandler(
                    list_series, pattern="^" + States.LIST_SERIES.value + "$"
                ),
                CallbackQueryHandler(
                    series_menu, pattern="^" + States.BACK.value + "$"
                ),
                CallbackQueryHandler(
                    find_series_by_title_beginning,
                    pattern="^" + States.NEXT_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    list_previous_series_from_title_beginning,
                    pattern="^" + States.PREV_PAGE.value + "$",
                ),
                CallbackQueryHandler(
                    Display.send_series, pattern="^(?!-1).+$",
                ),
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end_second_level, pattern="^" + str(States.END.value) + "$"
            ),
        ],
        map_to_parent={
            States.END.value: States.MENU.value,
            States.STOPPING.value: States.END.value,
        },
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
            States.MENU.value: menu_handlers,
            States.STOPPING.value: [CommandHandler("start", start)],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CallbackQueryHandler(
                end, pattern="^" + str(States.END.value) + "$"
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
