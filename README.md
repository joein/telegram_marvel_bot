# [Marvel bot](https://t.me/marvel_wiki_bot)
Telegram Marvel bot is a final project at HSE MLDS Python course.

Bot allows to gather information about Marvel Universe, about its characters, comics, events and series. </br>
Interaction with bot is carried out by commands `/start` and `/stop` and by inline keyboards.
These keyboards let user choose whether he wants to list available items or to find it by </br>
the beginning of a name or by a precise value.

To collect required information bot utilizes [Marvel API](https://developer.marvel.com/).</br>
[AWS](https://aws.amazon.com/) were used to deploy the app.


Project structure:
- `bot.py` is an entrypoint for the bot. There are top-level conversation handler constructing and launching of the bot.
- `base_handlers.py` contains two classes, `BaseHandler` and `MiscHandler`, 
the former one is a parent class for entity (comics,</br> events, etc.) related conversation handlers and the latter contains handlers for bot management like start, stop, and etc.
- `conv_handler_builder.py` provides `ConversationHandlerBuilder` which builds nested conversation handlers (describes transitions and match callbacks)
- `marvel_handlers.py` contains entity related conversation handlers, such as `CharactersHandler`, `ComicsHandler`, `EventsHandler`, `SeriesHandler`.
- `states.py` has `States` class which provides convenient interface for possible bot states.
- `custom_keyboard.py` contains keyboards for different menus and allows to generate custom keyboards from iterables.
- `display.py` is required to render info about chosen entity.
- `text.py` store some text constants in `Text` class which also can be used for generating custom text from entities.
- `fetcher.py` contains class which intercepts with Marvel API.
- `parser.py` and its class `ResponseJSONParser` parsing result of request to Marvel API.
- `entities.py` describes entities structures.
