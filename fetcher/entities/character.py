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
        self.detail = detail["url"].split("?utm")[0] if detail else ""
        self.wiki = wiki["url"].split("?utm")[0] if wiki else ""
        self.comic = comic["url"].split("?utm")[0] if comic else ""
        self.collections = collections

        self._resource_uri = resource_uri

    def __repr__(self):
        return f"Character(name: {self.name}, _id: {self._id}, _resource_uri: {self._resource_uri})"
