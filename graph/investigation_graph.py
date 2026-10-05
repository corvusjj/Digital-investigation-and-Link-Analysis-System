import networkx as nx

class InvestigationGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity):
        self.graph.add_node(
            entity["entity_id"],
            label=entity["label"],
            entity_type=entity["entity_type"],
            category=entity["category"],
            properties=entity["properties"],
            date_created=entity["date_created"]
        )

    def add_relation(self, relation):
        self.graph.add_edge(
            relation["source_id"],
            relation["target_id"],
            relation_id=relation["relation_id"],
            relation_type=relation["relation_type"]
        )

    def build(self, entities, relations):
        self.graph.clear()

        for entity in entities:
            self.add_entity(entity)

        for relation in relations:
            self.add_relation(relation)

    def get_graph(self):
        return self.graph

    def get_nodes(self):
        return self.graph.nodes(data=True)

    def get_edges(self):
        return self.graph.edges(data=True)
