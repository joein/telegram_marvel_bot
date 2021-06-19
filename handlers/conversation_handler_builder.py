import abc

from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
)

from states import States
from handlers.base_handlers import MiscHandler


class ConversationHandlerBuilder:
    @classmethod
    def build_inner_conversation_handler(
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
            map_to_parent={States.END.value: States.MENU.value,},
        )
        return handler

    @staticmethod
    def _handlers_from_dict(pattern_handler_map):
        return [
            CallbackQueryHandler(handler, pattern=pattern)
            for pattern, handler in pattern_handler_map.items()
        ]


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
