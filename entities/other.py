from entities.base.entity import Entity

class Event(Entity):
    def __init__(
            self,
            label,
            event_name,
            event_type,
            date,
            location,
            description
    ):
        super().__init__("EVENT", label)
        
        self.properties = {
            "event_name": event_name,
            "event_type": event_type,
            "date": date,
            "location": location,
            "description": description
        }

class Case(Entity):
    def __init__(
            self,
            label,
            case_name,
            case_type,
            description,
            status,
            investigator
    ):
        super().__init__("CASE", label)
        
        self.properties = {
            "case_name": case_name,
            "case_type": case_type,
            "status": status,
            "investigator": investigator,
            "description": description
        }
