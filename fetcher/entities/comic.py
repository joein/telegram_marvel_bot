class Comic:
    def __init__(
        self,
        _id,
        name,
        description,
        img_link,
        page_count,
        detail,
        resource_uri,
        creators,
    ):
        self._id = _id
        self.name = name
        self.description = description
        self.img_link = img_link
        self.page_count = page_count
        self.detail = detail["url"].split("?utm")[0] if detail else ""
        self.resource_uri = resource_uri
        self.creators = creators

    def __repr__(self):
        return f"Comic(_id: {self._id}, title: {self.name}, resource_uri: {self.resource_uri})"
