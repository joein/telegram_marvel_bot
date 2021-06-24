class Creator:
    def __init__(self, resource_uri, name, role):
        self._resource_uri = resource_uri
        self.name = name
        self.role = role

    def __repr__(self):
        return f"{self.role}: {self.name}"
