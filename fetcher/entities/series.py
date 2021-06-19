class Series:
    def __init__(
        self,
        _id,
        name,
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
        self.name = name
        self.description = description
        self.img_link = img_link
        self.detail = detail["url"].split("?utm")[0] if detail else ""
        self.resource_uri = resource_uri
        self.start_year = start_year
        self.end_year = end_year
        self.next_series = next_series
        self.previous_series = previous_series
        self.creators = creators

    def __repr__(self):
        return f"Series(_id: {self._id}, title: {self.name}, resource_uri: {self.resource_uri})"
