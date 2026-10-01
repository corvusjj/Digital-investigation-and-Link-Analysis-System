from datetime import date
import uuid

class Case:
    def __init__(
        self,
        case_name,
        case_type,
        description = "",
        status = "OPEN",
        investigator = "",
        case_id = None,
        date_opened = None,
        date_closed = None,
        date_created = None
    ):
        self.case_id = case_id or str(uuid.uuid4())

        self.case_name = case_name
        self.case_type = case_type
        self.description = description

        self.date_opened = date_opened or date.today().isoformat()
        self.date_closed = date_closed

        self.status = status
        self.investigator = investigator

        self.date_created = date_created or date.today().isoformat()
        