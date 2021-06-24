from states import States
from handlers.entity_handlers import ComicsHandler
from visualization.display import ComicsDisplay as Display
from handlers.conversation_handlers.conversation_handler_builder import (
    ConversationHandlerBuilder,
    ConversationHandlerInterface,
)


class ComicsConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):

        menu = {
            f"^{States.LIST_COMICS.value}$": ComicsHandler.list_,
            f"^{States.FIND_COMIC_BY_TITLE.value}$": ComicsHandler.find_by_name,
            f"^{States.FIND_COMIC_BY_TITLE_BEGINNING.value}$": ComicsHandler.find_by_name_beginning,
        }
        back = {
            f"^{States.BACK.value}$": ComicsHandler.menu,
        }
        send = {
            f"^(?!{States.END.value}).+$": Display.send,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.list_,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous,
            **send,
        }
        find_by_title = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_from_name,
            **send,
        }
        find_by_title_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": ComicsHandler.find_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": ComicsHandler.list_previous_from_name_beginning,
            **send,
        }
        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.COMICS.value}$": ComicsHandler.menu},
            {
                States.COMICS.value: menu,
                States.LIST_COMICS.value: list_,
                States.FIND_COMIC_BY_TITLE.value: find_by_title,
                States.FIND_COMIC_BY_TITLE_BEGINNING.value: find_by_title_beginning,
            },
            ComicsHandler.save_input,
        )
