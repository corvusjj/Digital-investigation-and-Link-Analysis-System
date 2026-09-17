from entities.base.entity import Entity

class Person(Entity):
    def __init__(
            self,
            label,
            full_name,
            alias,
            age,
            occupation
    ):
        super().__init__("PERSON", label)
        
        self.properties = {
            "full_name": full_name,
            "alias": alias,
            "age": age,
            "occupation": occupation
        }

class Organization(Entity):
    def __init__(
            self,
            label,
            name,
            organization_type,
            location
    ):
        super().__init__("ORGANIZATION", label)
        
        self.properties = {
            "name": name,
            "organization_type": organization_type,
            "location": location
        }

class Group(Entity):
    def __init__(
            self,
            label,
            name,
            group_type,
            known_alias,
            location
    ):
        super().__init__("GROUP", label)
        
        self.properties = {
            "name": name,
            "group_type": group_type,
            "known_alias": known_alias,
            "location": location
        }