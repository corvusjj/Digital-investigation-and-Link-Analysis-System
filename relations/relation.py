import uuid

class Relation:
    def __init__(
        self,
        relation_type,
        source_id,
        target_id, 
    ):
        self.relation_id = str(uuid.uuid4())
        self.relation_type = relation_type
        self.source_id = source_id
        self.target_id = target_id
