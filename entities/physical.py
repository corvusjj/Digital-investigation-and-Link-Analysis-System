from entities.base.entity import Entity

class Vehicle(Entity):
    def __init__(
            self,
            label,
            model,
            year,
            color,
            vehicle_type,
            plate_number,
            registration_status
    ):
        super().__init__("VEHICLE", label)
        
        self.properties = {
            "model": model,
            "year": year,
            "color": color,
            "vehicle_type": vehicle_type,
            "plate_number": plate_number,
            "registration_status": registration_status
        }

from entities.base.entity import Entity

class LicensePLate(Entity):
    def __init__(
            self,
            label,
            plate_number,
            plate_type,
            country,
            registration_status,
            expiration_date
    ):
        super().__init__("LICENSE PLATE", label)
        
        self.properties = {
            "plate_number": plate_number,
            "plate_type": plate_type,
            "country": country,
            "registration_status": registration_status,
            "expiration_date": expiration_date
        }

class Property(Entity):
    def __init__(
            self,
            label,
            property_type,
            address,
            owner,
            registration_number,
            description
    ):
        super().__init__("PROPERTY", label)
        
        self.properties = {
            "property_type": property_type,
            "address": address,
            "owner": owner,
            "registration_number": registration_number,
            "description": description
        }

class PhysicalObject(Entity):
    def __init__(
            self,
            label,
            object_type,
            description,
            serial_number,
            model,
            condition
    ):
        super().__init__("PHYSICAL OBJECT", label)
        
        self.properties = {
            "object_type": object_type,
            "description": description,
            "serial_number": serial_number,
            "model": model,
            "condition": condition
        }
