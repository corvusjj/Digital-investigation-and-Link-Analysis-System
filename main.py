from entities.people.person import Person

person = Person(
    "John",
    "John Cena",
    "Can't see me",
    "50",
    ""
)

print(person.date_created)

class Relation:
    def __init__(self, type, source, target):
        self.type = type
        self.source = source
        self.target = target

# create nodes factory - child classes
# common relations properties
# dictionaries/ list for storing nodes
# mvc modules
