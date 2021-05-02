import custom_types as ct


class Creator:
    def __init__(self, resource_uri, name, role):
        self.resource_uri = resource_uri
        self.name = name
        self.role = role

    def __repr__(self):
        return f"{self.role}: {self.name}"


class Character:
    def __init__(
        self,
        _id,
        name,
        description,
        img_link,
        collections,
        detail,
        wiki,
        comic,
        resource_uri,
    ):
        self._id = _id
        self.name = name
        self.description = description
        self.img_link = img_link
        self.detail = detail['url'].split('?utm')[0] if detail else ''
        self.wiki = wiki['url'].split('?utm')[0] if wiki else ''
        self.comic = comic['url'].split('?utm')[0] if comic else ''
        self.collections: ct.Collections = collections

        self._resource_uri = resource_uri

    def __repr__(self):
        return f"Character(name: {self.name}, _id: {self._id}, _resource_uri: {self._resource_uri})"


class Comic:
    def __init__(
        self,
        _id,
        title,
        description,
        img_link,
        page_count,
        detail,
        resource_uri,
        creators,
    ):
        self._id = _id
        self.title = title
        self.description = description
        self.img_link = img_link
        self.page_count = page_count
        self.detail = detail['url'].split('?utm')[0] if detail else ''
        self.resource_uri = resource_uri
        self.creators = creators

    def __repr__(self):
        return f"Comic(_id: {self._id}, title: {self.title}, resource_uri: {self.resource_uri})"


class Event:
    def __init__(
        self,
        _id,
        name,
        description,
        img_link,
        detail,
        wiki,
        resource_uri,
        start,
        end,
        next_event,
        previous_event,
    ):
        self._id = _id
        self.name = name
        self.description = description
        self.img_link = img_link
        self.detail = detail['url'].split('?utm')[0] if detail else ''
        self.wiki = wiki['url'].split('?utm')[0] if wiki else ''
        self.resource_uri = resource_uri
        self.start = start
        self.end = end
        self.next_event = next_event
        self.previous_event = previous_event

    def __repr__(self):
        return f"Event(_id: {self._id}, title: {self.name}, resource_uri: {self.resource_uri})"


class Series:
    def __init__(
        self,
        _id,
        title,
        description,
        img_link,
        detail,
        resource_uri,
        start_year,
        end_year,
        next_series,
        previous_series,
        creators,
    ):
        self._id = _id
        self.title = title
        self.description = description
        self.img_link = img_link
        self.detail = detail['url'].split('?utm')[0] if detail else ''
        self.resource_uri = resource_uri
        self.start_year = start_year
        self.end_year = end_year
        self.next_series = next_series
        self.previous_series = previous_series
        self.creators = creators

    def __repr__(self):
        return f"Series(_id: {self._id}, title: {self.title}, resource_uri: {self.resource_uri})"
