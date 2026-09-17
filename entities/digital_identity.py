from entities.base.entity import Entity

class Email(Entity):
    def __init__(
            self,
            label,
            email_address,
            provider,
    ):
        super().__init__("EMAIL", label)
        
        self.properties = {
            "email_address": email_address,
            "provider": provider,
        }

class PhoneNumber(Entity):
    def __init__(
            self,
            label,
            phone_number,
            country_code,
            carrier
    ):
        super().__init__("PHONE NUMBER", label)
        
        self.properties = {
            "phone_number": phone_number,
            "country_code": country_code,
            "carrier": carrier
        }

class Username(Entity):
    def __init__(
            self,
            label,
            username,
            platform,
            profile_url
    ):
        super().__init__("USERNAME", label)
        
        self.properties = {
            "username": username,
            "platform": platform,
            "profile_url": profile_url
        }

class SocialMediaAccount(Entity):
    def __init__(
            self,
            label,
            platform,
            username,
            display_name,
            profile_url,
            last_active
    ):
        super().__init__("SOCIAL MEDIA ACCOUNT", label)
        
        self.properties = {
            "username": username,
            "platform": platform,
            "display_name": display_name,
            "profile_url": profile_url,
            "last_active": last_active
        }

class OnlineAccount(Entity):
    def __init__(
            self,
            label,
            service_name,
            username,
            last_login,
            profile_url,
    ):
        super().__init__("ONLINE ACCOUNT", label)
        
        self.properties = {
            "username": username,
            "service_name": service_name,
            "profile_url": profile_url,
            "last_login": last_login
        }

class CloudAccount(Entity):
    def __init__(
            self,
            label,
            provider,
            username,
            last_login,
    ):
        super().__init__("CLOUD ACCOUNT", label)
        
        self.properties = {
            "username": username,
            "provider": provider,
            "last_login": last_login
        }