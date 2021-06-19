from states import States
from handlers.entity_handlers import CharactersHandler
from visualization.display import CharactersDisplay as Display
from handlers.conversation_handlers.conversation_handler_builder import (
    ConversationHandlerBuilder,
    ConversationHandlerInterface,
)


class CharactersConversationHandler(ConversationHandlerInterface):
    @classmethod
    def _build(cls):
        menu = {
            f"^{States.LIST_CHARACTERS.value}$": CharactersHandler.list_,
            f"^{States.FIND_CHARACTER_BY_NAME.value}$": CharactersHandler.find_by_name,
            f"^{States.FIND_CHARACTER_BY_NAME_BEGINNING.value}$": CharactersHandler.find_by_name_beginning,
        }
        back = {f"^{States.BACK.value}$": CharactersHandler.menu}
        send = {
            f"^(?!{States.END.value}).+$": Display.send,
        }
        list_ = {
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.list_,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous,
            **send,
        }
        find_by_name = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_by_name,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_from_name,
            **send,
        }
        find_by_name_beginning = {
            **menu,
            **back,
            f"^{States.NEXT_PAGE.value}$": CharactersHandler.find_by_name_beginning,
            f"^{States.PREV_PAGE.value}$": CharactersHandler.list_previous_from_name_beginning,
            **send,
        }

        return ConversationHandlerBuilder.build_inner_conversation_handler(
            {f"^{States.CHARACTERS.value}$": CharactersHandler.menu},
            {
                States.CHARACTERS.value: menu,
                States.LIST_CHARACTERS.value: list_,
                States.FIND_CHARACTER_BY_NAME.value: find_by_name,
                States.FIND_CHARACTER_BY_NAME_BEGINNING.value: find_by_name_beginning,
            },
            CharactersHandler.save_input,
        )
