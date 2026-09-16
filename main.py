from entities.people.person import Person

person = Person(
    "John",
    "John Cena",
    "Can't see me",
    "50",
    ""
)

print(person.properties)

class Relation:
    def __init__(self, type, source, target):
        self.type = type
        self.source = source
        self.target = target

# common relations properties
# create nodes factory - child classes
# dictionaries/ list for storing nodes
# mvc modules
