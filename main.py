from factories.entity_factory import EntityFactory

person = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "JOHN",
    {"full_name": "John Corbet",
      "alias": "programmer",
      "age": 3,
      "occupation": "student"}
)

print(person.properties)

class Relation:
    def __init__(self, type, source, target):
        self.type = type
        self.source = source
        self.target = target

# common relations properties
# dictionaries/ list for storing nodes
# mvc modules
