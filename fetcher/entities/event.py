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
        self.detail = detail["url"].split("?utm")[0] if detail else ""
        self.wiki = wiki["url"].split("?utm")[0] if wiki else ""
        self.resource_uri = resource_uri
        self.start = start
        self.end = end
        self.next_event = next_event
        self.previous_event = previous_event

    def __repr__(self):
        return f"Event(_id: {self._id}, title: {self.name}, resource_uri: {self.resource_uri})"

