from entities.base.entity import Entity

class Device(Entity):
    def __init__(
            self,
            label,
            device_type,
            manufacturer,
            model,
            serial_number,
            imei,
            purchase_date
    ):
        super().__init__("DEVICE", label)
        
        self.properties = {
            "device_type": device_type,
            "manufacturer": manufacturer,
            "model": model,
            "serial_number": serial_number,
            "imei": imei,
            "purchase_date": purchase_date 
        }

class IPAddress(Entity):
    def __init__(
            self,
            label,
            ip_address,
            ip_version,
            isp,
            country,
            city
    ):
        super().__init__("IP ADDRESS", label)
        
        self.properties = {
            "ip_address": ip_address,
            "ip_version": ip_version, 
            "isp": isp,
            "country": country,
            "city": city
        }

class MACAddress(Entity):
    def __init__(
            self,
            label,
            manufacturer,
            mac_address,
            device_type,
    ):
        super().__init__("MAC ADDRESS", label)
        
        self.properties = {
            "manufacturer": manufacturer, 
            "mac_address": mac_address,
            "device_type": device_type 
        }

class WifiNetwork(Entity):
    def __init__(
            self,
            label,
            ssid,
            bssid,
            router_model,
            isp,
            location
    ):
        super().__init__("WIFI NETWORK", label)
        
        self.properties = {
            "ssid": ssid, 
            "bssid": bssid,
            "router_model": router_model,
            "isp": isp,
            "location": location
        }

class Server(Entity):
    def __init__(
            self,
            label,
            hostname,
            server_type,
            provider,
            location,
    ):
        super().__init__("SERVER", label)
        
        self.properties = {
            "hostname": hostname,  
            "server_type": server_type, 
            "provider": provider,
            "location": location
        }

class Domain(Entity):
    def __init__(
            self,
            label,
            domain_name,
            registrar,
    ):
        super().__init__("DOMAIN", label)
        
        self.properties = {
            "domain_name": domain_name,  
            "registrar": registrar, 
        }

class Website(Entity):
    def __init__(
            self,
            label,
            name,
            domain,
            hosting_provider,
            url
    ):
        super().__init__("WEBSITE", label)
        
        self.properties = {
            "name": name,  
            "domain": domain,
            "hosting_provider": hosting_provider,
            "url": url
        }
        