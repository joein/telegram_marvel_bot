from states import States
from display import Display
from handlers.entity_handlers import SeriesHandler
from handlers.conversation_handlers.conversation_handler_builder import (
    ConversationHandlerBuilder,
    ConversationHandlerInterface,
)


class SeriesConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_SERIES.value}$": SeriesHandler.list_,
            f"^{States.FIND_SERIES_BY_TITLE.value}$": SeriesHandler.find_by_name,
            f"^{States.FIND_SERIES_BY_TITLE_BEGINNING.value}$": SeriesHandler.find_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": SeriesHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send_series,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.list_,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous,
            **send,
        }
        find_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_from_name,
            **send,
        }
        find_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": SeriesHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": SeriesHandler.list_previous_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.SERIES.value}$": SeriesHandler.menu},
            {
                States.SERIES.value: menu,
                States.LIST_SERIES.value: list_,
                States.FIND_SERIES_BY_TITLE.value: find_by_name,
                States.FIND_SERIES_BY_TITLE_BEGINNING.value: find_by_name_beginning,
            },
            SeriesHandler.save_input,
        )
