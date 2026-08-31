import uuid;

class Entity:
    id = uuid.uuid4();

    def __init__(self, type, name):
        self.type = type
        self.name = name

class Relation:
    def __init__(self, type, source, target):
        self.type = type
        self.source = source
        self.target = target

person1 = Entity('PERSON', 'Alex Cruz')
relation1 = Relation('OWNS', 'P001', 'E001')

print(person1.id)
