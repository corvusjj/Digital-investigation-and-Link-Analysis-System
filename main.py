from factories.entity_factory import EntityFactory
from factories.relation_factory import RelationFactory
from graph.investigation_graph import InvestigationGraph

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

person3 = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "BRUCE",
    {"full_name": "Bruce Dela Cruz",
      "alias": "dark night",
      "age": 42,
      "occupation": "police officer"}
)

relation1 = RelationFactory.create(
    "IS ASSOCIATED",
    person1.entity_id,
    person2.entity_id
)

investigation_graph = InvestigationGraph()

investigation_graph.add_entity(person1)
investigation_graph.add_entity(person2)
investigation_graph.add_relation(relation1)

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
