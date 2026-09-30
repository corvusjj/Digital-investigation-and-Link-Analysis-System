import networkx as nx

class InvestigationGraph:
    
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entity(self, entity):
        self.graph.add_node(entity)

    def add_relation(self, relation):
        self.graph.add_edge(
            relation.source_id,
            relation.target_id,
            relation_type = relation.relation_type
        )
