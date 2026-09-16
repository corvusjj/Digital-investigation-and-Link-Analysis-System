import uuid
from datetime import date

class Entity:
    def __init__(self, type, label):
        self.entity_id = str(uuid.uuid4())
        self.type = type
        self.label = label
        self.date_created = date.today()
        self.properties = {}
