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