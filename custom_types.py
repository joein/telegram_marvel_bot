
from typing import TypedDict, List, Optional


# https://developer.marvel.com/documentation/images  - how to extract images
# 1493 general available amount of characters


class Item(TypedDict):
    # see examples in Event, Story, Series, Comics
    resourceURI: str
    name: str


class StoryItem(Item):
    type: str  # see example in Story


class Collection(TypedDict):
    # see examples in descendants (Event, Story, Series, Comics)
    available: int
    collectionURI: str
    returned: int


class Event(Collection):
    # available: 1
    # collectionURI: http://gateway.marvel.com/v1/public/characters/1011334/events
    # items.resourceURI: http://gateway.marvel.com/v1/public/events/269
    # items.name: "Secret Invasion"
    # returned: 1
    items: List[Item]


class Story(Collection):
    # available: 21,
    # returned: 20
    # collectionURI: http://gateway.marvel.com/v1/public/characters/1011334/stories
    # items.resourceURI: http://gateway.marvel.com/v1/public/stories/19947
    # items.name: Cover #19947
    # items.type: cover
    items: List[StoryItem]


class Series(Collection):
    # available: 3
    # collectionURI: http://gateway.marvel.com/v1/public/characters/1011334/series"
    # returned: 3
    # items.resourceURI: http://gateway.marvel.com/v1/public/series/1945
    # items.name: Avengers: The Initiative (2007 - 2010)

    items: List[Item]


class Comics(Collection):
    # available: 12,
    # collectionURI: http://gateway.marvel.com/v1/public/characters/1011334/comics,
    # returned: 12
    # items.resourceURI : http://gateway.marvel.com/v1/public/comics/21366,
    # items.name: Avengers: The Initiative (2007) #14,
    items: List[Item]


class Thumbnail(TypedDict):
    path: str  # http://i.annihil.us/u/prod/marvel/i/mg/c/e0/535fecbbb9784
    extension: str  # jpg


class UrlInfo(TypedDict):
    # №1
    # "type": detail
    # url: http://marvel.com/characters/77/aim.?utm_campaign=apiRef&utm_source=49b617fb875a6b1a9c6304774f9e2541
    # 2
    # "type": wiki
    # url: http://marvel.com/universe/A.I.M.?utm_campaign=apiRef&utm_source=49b617fb875a6b1a9c6304774f9e2541
    # 3
    # "type": comiclink
    # url: http://marvel.com/comics/characters/1009144/aim.?utm_campaign=apiRef&utm_source=49b617fb875a6b1a9c6304774f9e2541
    type: str
    url: str


class Result(TypedDict):
    id: int  # 1011334
    name: str  # 3-D Man
    description: str  # "" (empty string)
    modified: str  # 2014-04-29T14:18:17-0400
    thumbnail: Thumbnail
    resourceURI: str  # http://gateway.marvel.com/v1/public/characters/1011334
    comics: List[Comics]
    events: List[Event]
    stories: List[Story]
    series: List[Series]
    urls: List[UrlInfo]


class ComicsSeries(TypedDict):
    resourceURI: str  # http://gateway.marvel.com/v1/public/series/23665
    name: str  # Marvel Previews (2017 - Present)


class ComicsVariants(TypedDict):
    resourceURI: str  # 'http://gateway.marvel.com/v1/public/comics/82970
    name: str  # 'Marvel Previews (2017)


class ComicsDate(TypedDict):
    type: str  # onsaleDate
    date: str  # 2099-10-30T00:00:00-0500


class ComicsPrice(TypedDict):
    type: str  # printPrice
    price: int  # 0


class Creator:
    resourceURI: str  # http://gateway.marvel.com/v1/public/creators/10021
    name: str  # Jim Nausedas
    role: str  # editor


class ComicsCreator(TypedDict):
    available: int  # 1
    collectionURI: str  # http://gateway.marvel.com/v1/public/comics/82967/creators
    items: List[Creator]


class ComicsCharacter(TypedDict):
    available: int  # 0
    collectionURI: str  # http://gateway.marvel.com/v1/public/comics/82967/characters
    items: List
    returned: int  # 0


class ComicsStory(TypedDict):
    resourceURI: str  # http://gateway.marvel.com/v1/public/stories/183698
    name: str  # cover from Marvel Previews (2017)
    type: str  # cover


class ComicsStories(TypedDict):
    available: int  # 2
    collectionURI: str  # http://gateway.marvel.com/v1/public/comics/82967/stories
    items: List[ComicsStory]
    returned: int  # 2


class ComicsEvents(TypedDict):
    available: int  # 0
    collectionURI: str  # http://gateway.marvel.com/v1/public/comics/82967/events
    items: List
    returned: int  # 0


class ResultComics(TypedDict):
    id: int  # 82967
    digitalId: int  # 0
    title: str  # Marvel Previews (2017)
    issueNumber: int  # 0
    variantDescription: str  # ''
    description: Optional[str]  # None
    modified: str  # 2019-11-07T08:46-15-0500
    isbn: str  # ''
    upc: str  # 75960608839302811
    diamondCode: str  # ''
    ean: str  # ''
    issn: str  # ''
    format: str  # ''
    pageCount: int  # 112
    textObjects: List  # []
    resourceURI: str  # 'httpL//gateway.marvel.com/v1/public/comics/82967
    urls: List[UrlInfo]
    series: ComicsSeries
    variants: List[ComicsVariants]
    collections: List  # []
    collectedIssues: List  # []
    dates: List[ComicsDate]
    prices: List[ComicsPrice]
    thumbnail: Thumbnail
    images: List  # []
    creators: ComicsCreator
    returned: int  # 1
    characters: ComicsCharacter


class Data(TypedDict):
    offset: int  # 0
    limit: int  # 4
    total: int  # 1493
    count: int  # 4
    results: List[Result]


class ResponseJSON(TypedDict):
    code: int  # 200
    status: str  # Ok
    copyright: str  # © 2021 MARVEL
    attributionText: str  # Data provided by Marvel. © 2021 MARVEL
    attributionHTML: str  # <a href="http://marvel.com">Data provided by Marvel. © 2021 MARVEL</a>
    etag: str  # eb7917a0268bd1051fbe7fa5e761f9edc42b11b7
    data: Data



########################################################
# custom data types
class Collections(TypedDict):
    comics: List[Comics]
    events: List[Event]
    stories: List[Story]
    series: List[Series]


########################################################
