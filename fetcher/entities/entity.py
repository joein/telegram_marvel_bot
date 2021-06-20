class BaseEntity:
    __slots__ = (
        "_id",
        "name",
        "description",
        "img_link",
        "detail",
        "_resource_uri",
    )


class Entity(BaseEntity):
    __slots__ = (
        "wiki",  # character, event

        "page_count",  # comic
        "creators",  # comic

        "start",  # event, series
        "end",  # event, series
        "next_",  # event, series
        "previous",  # event, series
    )


class EntityBuilder:

    def __init__(self):
        self.entity = None
        self.reset()

    def reset(self):
        self.entity = Entity()

    def add_base_features(self, base_features):
        for feature, value in base_features.items():
            setattr(self.entity, feature, value)

    def add_date_borders(self, start, end):
        setattr(self.entity, "start", start)
        setattr(self.entity, "end", end)

    def add_surrounding_entities(self, next_, previous):
        setattr(self.entity, "next_", next_)
        setattr(self.entity, "previous", previous)

    def add_wiki(self, wiki):
        setattr(self.entity, "wiki", wiki)

    def add_comic_meta(self, page_count, creators):
        setattr(self.entity, "page_count", page_count)
        setattr(self.entity, "creators", creators)

    def finish(self):
        entity = self.entity
        self.reset()
        return entity
