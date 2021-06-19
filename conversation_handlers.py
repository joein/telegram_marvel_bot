import abc

from states import States
from display import Display
from marvel_handlers import (
    CharactersHandler,
    ComicsHandler,
    EventsHandler,
    SeriesHandler,
)
from conversation_handler_builder import ConversationHandlerBuilder


class ConversationHandlerInterface(abc.ABC):
    HANDLER = None

    @classmethod
    def get(cls):
        if not cls.HANDLER:
            cls.HANDLER = cls._build()
        return cls.HANDLER

    @classmethod
    @abc.abstractmethod
    def _build(cls):
        pass


class CharactersConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_CHARACTERS.value}$": CharactersHandler.list_characters,
            f"^{States.FIND_CHARACTER_BY_NAME.value}$": CharactersHandler.find_character_by_name,
            f"^{States.FIND_CHARACTER_BY_NAME_BEGINNING.value}$": CharactersHandler.find_character_by_name_beginning,
        }
        back = {f"^{States.BACK.value}$": CharactersHandler.menu}
        send = {
            f"^(?!{States.END.value}).+$": Display.send_character,
        }
        list_characters = {
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.list_characters,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_characters,
            **send,
        }
        find_character_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_character_by_name,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_characters_from_name,
            **send,
        }
        find_character_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_character_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_characters_from_name_beginning,
            **send,
        }

        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.CHARACTERS.value}$": CharactersHandler.menu},
            {
                States.CHARACTERS.value: menu,
                States.LIST_CHARACTERS.value: list_characters,
                States.FIND_CHARACTER_BY_NAME.value: find_character_by_name,
                States.FIND_CHARACTER_BY_NAME_BEGINNING.value: find_character_by_name_beginning,
            },
            CharactersHandler.save_input,
        )


class ComicsConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):

        menu = {
            f"^{States.LIST_COMICS.value}$": ComicsHandler.list_comics,
            f"^{States.FIND_COMIC_BY_TITLE.value}$": ComicsHandler.find_comic_by_title,
            f"^{States.FIND_COMIC_BY_TITLE_BEGINNING.value}$": ComicsHandler.find_comic_by_title_beginning,
        }
        back = {
            f"^{States.BACK.value}$": ComicsHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_comic,
        }
        list_comics = {
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.list_comics,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_comics,
            **send,
        }
        find_comic_by_title = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_comic_by_title,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_comics_from_title,
            **send,
        }
        find_comic_by_title_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_comic_by_title_beginning,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_comics_from_title_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.COMICS.value}$": ComicsHandler.menu},
            {
                States.COMICS.value: menu,
                States.LIST_COMICS.value: list_comics,
                States.FIND_COMIC_BY_TITLE.value: find_comic_by_title,
                States.FIND_COMIC_BY_TITLE_BEGINNING.value: find_comic_by_title_beginning,
            },
            ComicsHandler.save_input,
        )


class EventsConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_EVENTS.value}$": EventsHandler.list_events,
            f"^{States.FIND_EVENT_BY_NAME.value}$": EventsHandler.find_event_by_name,
            f"^{States.FIND_EVENT_BY_NAME_BEGINNING.value}$": EventsHandler.find_event_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": EventsHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_event,
        }
        list_events = {
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.list_events,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_events,
            **send,
        }
        find_event_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_event_by_name,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_events_from_name,
            **send,
        }
        find_event_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_event_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_events_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.EVENTS.value}$": EventsHandler.menu},
            {
                States.EVENTS.value: menu,
                States.LIST_EVENTS.value: list_events,
                States.FIND_EVENT_BY_NAME.value: find_event_by_name,
                States.FIND_EVENT_BY_NAME_BEGINNING.value: find_event_by_name_beginning,
            },
            EventsHandler.save_input,
        )


class SeriesConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_SERIES.value}$": SeriesHandler.list_series,
            f"^{States.FIND_SERIES_BY_TITLE.value}$": SeriesHandler.find_series_by_title,
            f"^{States.FIND_SERIES_BY_TITLE_BEGINNING.value}$": SeriesHandler.find_series_by_title_beginning,
        }
        back = {
            f"^{States.BACK.value}$": SeriesHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_series,
        }
        list_series = {
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.list_series,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_series,
            **send,
        }
        find_series_by_title = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_series_by_title,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_series_from_title,
            **send,
        }
        find_series_by_title_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_series_by_title,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_series_from_title_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.SERIES.value}$": SeriesHandler.menu},
            {
                States.SERIES.value: menu,
                States.LIST_SERIES.value: list_series,
                States.FIND_SERIES_BY_TITLE.value: find_series_by_title,
                States.FIND_SERIES_BY_TITLE_BEGINNING.value: find_series_by_title_beginning,
            },
            SeriesHandler.save_input,
        )
