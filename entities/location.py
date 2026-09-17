from entities.base.entity import Entity

class Location(Entity):
    def __init__(
            self,
            label,
            latitude,
            longitude,
            location_type,
            description
    ):
        super().__init__("LOCATION", label)
        
        self.properties = {
            "latitude": latitude,
            "longitude": longitude,
            "location_type": location_type,
            "description": description
        }

from entities.base.entity import Entity

class Address(Entity):
    def __init__(
            self,
            label,
            street,
            barangay,
            city,
            province,
            country,
            postal_code
    ):
        super().__init__("ADDRESS", label)
        
        self.properties = {
            "street": street,
            "barangay": barangay,
            "city": city,
            "province": province,
            "country": country,
            "postal_code": postal_code
        }
    