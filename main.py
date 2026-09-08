import uuid;

class Entity:
    def __init__(self, type, name):
        self._id = uuid.uuid4()
        self.type = type
        self.name = name

    @property
    def id(self):
        return self._id

class Relation:
    def __init__(self, type, source, target):
        self.type = type
        self.source = source
        self.target = target

person1 = Entity('PERSON', 'Alex Cruz')
person2 = Entity('PERSON', 'Stacy Ferrar')

# relation1 = Relation('CONNECTED_TO', person1.id, person2.id)

print(person1.id)
