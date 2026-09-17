from entities.base.entity import Entity

class Weapon(Entity):
    def __init__(
            self,
            label,
            weapon_type,
            manufacturer,
            model,
            serial_number,
            condition
    ):
        super().__init__("WEAPON", label)
        
        self.properties = {
            "weapon_type": weapon_type,
            "manufacturer": manufacturer,
            "model": model,
            "serial_number": serial_number,
            "condition": condition
        }

class Substance(Entity):
    def __init__(
            self,
            label,
            substance_name,
            substance_type,
            quantity,
            unit,
            description
    ):
        super().__init__("SUBSTANCE", label)
        
        self.properties = {
            "substance_name": substance_name,
            "substance_type": substance_type,
            "quantity": quantity,
            "unit": unit,
            "description": description
        }

class Fingerprint(Entity):
    def __init__(
            self,
            label,
            fingerprint_id,
            finger,
            hand,
            source,
            location_found,
            quality
    ):
        super().__init__("FINGERPRINT", label)
        
        self.properties = {
            "fingerprint_id": fingerprint_id,
            "finger": finger,
            "hand": hand,
            "source": source,
            "location_found": location_found,
            "quality": quality
        }

class DNASample(Entity):
    def __init__(
            self,
            label,
            sample_type,
            source,
            collection_date,
            location_found,
    ):
        super().__init__("DNA SAMPLE", label)
        
        self.properties = {
            "sample_type": sample_type,
            "source": source,
            "collection_date": collection_date,
            "location_found": location_found
        }

class Document(Entity):
    def __init__(
            self,
            label,
            document_type,
            title,
            author,
            creation_date,
            file_format,
            description
    ):
        super().__init__("DOCUMENT", label)
        
        self.properties = {
            "document_type": document_type,
            "title": title,
            "author": author,
            "creation_date": creation_date,
            "file_format": file_format,
            "description": description
        }
