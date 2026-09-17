from relations.relation import Relation

class RelationFactory:
    @staticmethod
    def create(
        relation_type,
        source_id,
        target_id,
    ):
        return Relation(
            relation_type = relation_type,
            source_id = source_id,
            target_id = target_id
        )