# [Marvel bot](https://t.me/marvel_wiki_bot)
Telegram Marvel bot is a final project at HSE MLDS Python course.

Bot allows to gather information about Marvel Universe, about its characters, comics, events and series. </br>
Interaction with bot is carried out by commands `/start` and `/stop` and by inline keyboards.
These keyboards let user choose whether he wants to list available items or to find it by </br>
the beginning of a name or by a precise value.

To collect required information bot utilizes [Marvel API](https://developer.marvel.com/).</br>
[AWS](https://aws.amazon.com/) were used to deploy the app (currently turned off).


Project structure:
- `bot.py` is an entrypoint for the bot. There are top-level conversation handler constructing and launching of the bot.
- `states.py` has `States` class which provides convenient interface for possible bot states.
- `text.py` store some text constants in `Text` class which also can be used for generating custom text from entities.
- `config.py` manages tokens and keys.
- `handlers` contains conversation handlers and entities handlers, the former responsible for state machine and the 
latter required to connect telegram related features with app logic features.    
- `visualisation` contains custom keyboards and classes required to render info about chosen entity.
- `fetcher` contains Marvel API interceptors.

