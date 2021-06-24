from states import States
from handlers.entity_handlers import EventsHandler
from visualization.display import EventsDisplay as Display
from handlers.conversation_handlers.conversation_handler_builder import (
    ConversationHandlerBuilder,
    ConversationHandlerInterface,
)


class EventsConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_EVENTS.value}$": EventsHandler.list_,
            f"^{States.FIND_EVENT_BY_NAME.value}$": EventsHandler.find_by_name,
            f"^{States.FIND_EVENT_BY_NAME_BEGINNING.value}$": EventsHandler.find_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": EventsHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.list_,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous,
            **send,
        }
        find_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_from_name,
            **send,
        }
        find_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": EventsHandler.find_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": EventsHandler.list_previous_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.EVENTS.value}$": EventsHandler.menu},
            {
                States.EVENTS.value: menu,
                States.LIST_EVENTS.value: list_,
                States.FIND_EVENT_BY_NAME.value: find_by_name,
                States.FIND_EVENT_BY_NAME_BEGINNING.value: find_by_name_beginning,
            },
            EventsHandler.save_input,
        )
