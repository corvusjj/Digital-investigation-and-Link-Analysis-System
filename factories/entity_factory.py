from registry.entity_registry import ENTITY_REGISTRY

class EntityFactory:
    @staticmethod
    def create(category, entity_type, label, properties):
        entity_class = ENTITY_REGISTRY[category][entity_type]

        return entity_class(label, **properties)