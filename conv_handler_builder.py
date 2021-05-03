from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
)

from states import States
from display import Display
from base_handlers import MiscHandler
from marvel_handlers import (
    CharactersHandler,
    ComicsHandler,
    EventsHandler,
    SeriesHandler,
)


class ConversationHandlerBuilder:
    @classmethod
    def _build_inner_conversation_handler(
        cls, entrypoint_map, state_pattern_handler_maps, save_input
    ):
        _callback_query_handlers = {
            state: cls._handlers_from_dict(pattern_handler_map)
            for state, pattern_handler_map in state_pattern_handler_maps.items()
        }
        handler = ConversationHandler(
            entry_points=cls._handlers_from_dict(entrypoint_map),
            states={
                States.ASK_FOR_INPUT.value: [
                    MessageHandler(
                        Filters.text & ~Filters.command, save_input
                    ),
                ],
                **_callback_query_handlers,
            },
            fallbacks=[
                CommandHandler("stop", MiscHandler.stop),
                CallbackQueryHandler(
                    MiscHandler.end_second_level,
                    pattern=f"^{States.END.value}$",
                ),
            ],
            map_to_parent={
                States.END.value: States.MENU.value,
                States.STOPPING.value: States.END.value,
            },
        )
        return handler

    @staticmethod
    def _handlers_from_dict(pattern_handler_map):
        return [
            CallbackQueryHandler(handler, pattern=pattern)
            for pattern, handler in pattern_handler_map.items()
        ]

    @classmethod
    def characters(cls):
        menu_map = {
            f"^{States.LIST_CHARACTERS.value}$": CharactersHandler.list_characters,
            f"^{States.FIND_CHARACTER_BY_NAME.value}$": CharactersHandler.find_character_by_name,
            f"^{States.FIND_CHARACTER_BY_NAME_BEGINNING.value}$": CharactersHandler.find_character_by_name_beginning,
        }
        back_map = {f"^{States.BACK.value}$": CharactersHandler.menu}
        send_map = {
            f"^(?!{States.END.value}).+$": Display.send_character,
        }
        list_characters_map = {
            **back_map,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.list_characters,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_characters,
            **send_map,
        }
        find_character_by_name_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_character_by_name,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_characters_from_name,
            **send_map,
        }
        find_character_by_name_beginning_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_character_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_characters_from_name_beginning,
            **send_map,
        }

        return cls._build_inner_conversation_handler(
            {f"^{States.CHARACTERS.value}$": CharactersHandler.menu},
            {
                States.CHARACTERS.value: menu_map,
                States.LIST_CHARACTERS.value: list_characters_map,
                States.FIND_CHARACTER_BY_NAME.value: find_character_by_name_map,
                States.FIND_CHARACTER_BY_NAME_BEGINNING.value: find_character_by_name_beginning_map,
            },
            CharactersHandler.save_input,
        )

    @classmethod
    def comics(cls):
        menu_map = {
            f"^{States.LIST_COMICS.value}$": ComicsHandler.list_comics,
            f"^{States.FIND_COMIC_BY_TITLE.value}$": ComicsHandler.find_comic_by_title,
            f"^{States.FIND_COMIC_BY_TITLE_BEGINNING.value}$": ComicsHandler.find_comic_by_title_beginning,
        }
        back_map = {
            f"^{States.BACK.value}$": ComicsHandler.menu,
        }
        send_map = {
            f"^(?!{States.END.value}).+$": Display.send_comic,
        }
        list_comics_map = {
            **back_map,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.list_comics,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_comics,
            **send_map,
        }
        find_comic_by_title_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_comic_by_title,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_comics_from_title,
            **send_map,
        }
        find_comic_by_title_beginning_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_comic_by_title_beginning,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_comics_from_title_beginning,
            **send_map,
        }
        return cls._build_inner_conversation_handler(
            {f"^{States.COMICS.value}$": ComicsHandler.menu},
            {
                States.COMICS.value: menu_map,
                States.LIST_COMICS.value: list_comics_map,
                States.FIND_COMIC_BY_TITLE.value: find_comic_by_title_map,
                States.FIND_COMIC_BY_TITLE_BEGINNING.value: find_comic_by_title_beginning_map,
            },
            ComicsHandler.save_input,
        )

    @classmethod
    def events(cls):
        menu_map = {
            f"^{States.LIST_EVENTS.value}$": EventsHandler.list_events,
            f"^{States.FIND_EVENT_BY_NAME.value}$": EventsHandler.find_event_by_name,
            f"^{States.FIND_EVENT_BY_NAME_BEGINNING.value}$": EventsHandler.find_event_by_name_beginning,
        }
        back_map = {
            f"^{States.BACK.value}$": EventsHandler.menu,
        }
        send_map = {
            f"^(?!{States.END.value}).+$": Display.send_event,
        }
        list_events_map = {
            **back_map,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.list_events,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_events,
            **send_map,
        }
        find_event_by_name_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_event_by_name,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_events_from_name,
            **send_map,
        }
        find_event_by_name_beginning_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_event_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_events_from_name_beginning,
            **send_map,
        }
        return cls._build_inner_conversation_handler(
            {f"^{States.EVENTS.value}$": EventsHandler.menu},
            {
                States.EVENTS.value: menu_map,
                States.LIST_EVENTS.value: list_events_map,
                States.FIND_EVENT_BY_NAME.value: find_event_by_name_map,
                States.FIND_EVENT_BY_NAME_BEGINNING.value: find_event_by_name_beginning_map,
            },
            EventsHandler.save_input,
        )

    @classmethod
    def series(cls):
        menu_map = {
            f"^{States.LIST_SERIES.value}$": SeriesHandler.list_series,
            f"^{States.FIND_SERIES_BY_TITLE.value}$": SeriesHandler.find_series_by_title,
            f"^{States.FIND_SERIES_BY_TITLE_BEGINNING.value}$": SeriesHandler.find_series_by_title_beginning,
        }
        back_map = {
            f"^{States.BACK.value}$": SeriesHandler.menu,
        }
        send_map = {
            f"^(?!{States.END.value}).+$": Display.send_series,
        }
        list_series_map = {
            **back_map,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.list_series,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_series,
            **send_map,
        }
        find_series_by_title_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_series_by_title,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_series_from_title,
            **send_map,
        }
        find_series_by_title_beginning_map = {
            **menu_map,
            **back_map,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_series_by_title,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_series_from_title_beginning,
            **send_map,
        }
        return cls._build_inner_conversation_handler(
            {f"^{States.SERIES.value}$": SeriesHandler.menu},
            {
                States.SERIES.value: menu_map,
                States.LIST_SERIES.value: list_series_map,
                States.FIND_SERIES_BY_TITLE.value: find_series_by_title_map,
                States.FIND_SERIES_BY_TITLE_BEGINNING.value: find_series_by_title_beginning_map,
            },
            SeriesHandler.save_input,
        )
