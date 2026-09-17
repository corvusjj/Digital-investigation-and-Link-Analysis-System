from registry.entity_registry import ENTITY_REGISTRY

entity_class = ENTITY_REGISTRY["PEOPLE"]["PERSON"]
person = entity_class("John", "J Corbet", "the_guy", "16", "")

print(person.properties)

class Relation:
    def __init__(self, type, source, target):
        self.type = type
        self.source = source
        self.target = target

# create nodes factory - child classes
# common relations properties
# dictionaries/ list for storing nodes
# mvc modules
