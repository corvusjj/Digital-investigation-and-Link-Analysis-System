from factories.entity_factory import EntityFactory
from factories.relation_factory import RelationFactory

person1 = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "JOHN",
    {"full_name": "John Corbet",
      "alias": "programmer",
      "age": 3,
      "occupation": "student"}
)

person2 = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "PETER",
    {"full_name": "Peter Parker",
      "alias": "spidey",
      "age": 24,
      "occupation": "actor"}
)

relation = RelationFactory.create(
    relation_type="IS ASSOCIATED",
    source_id = person1.entity_id,
    target_id = person2.entity_id
)

print(relation)

# common relations properties
# dictionaries/ list for storing nodes
# mvc modules

# relation confidence
# properties={
#         "date": "2026-09-15",
#         "source": "Vehicle Registry",
#         "confidence": "HIGH",
#         "notes": "Registered owner"
#     }
