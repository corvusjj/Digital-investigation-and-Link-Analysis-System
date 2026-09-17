from entities.base.entity import Entity

class Message(Entity):
    def __init__(
            self,
            label,
            sender,
            recipient,
            content,
            platform,
            timestamp
    ):
        super().__init__("MESSAGE", label)
        
        self.properties = {
            "sender": sender,
            "recipient": recipient,
            "content": content,
            "platform": platform,
            "timestamp": timestamp
        }

class Call(Entity):
    def __init__(
            self,
            label,
            caller,
            recipient,
            duration,
            timestamp
    ):
        super().__init__("CALL", label)
        
        self.properties = {
            "caller": caller,
            "recipient": recipient,
            "duration": duration,
            "timestamp": timestamp
        }

class SocialMediaPost(Entity):
    def __init__(
            self,
            label,
            platform,
            author,
            content,
            timestamp,
            url
    ):
        super().__init__("SOCIAL MEDIA POST", label)
        
        self.properties = {
            "platform": platform,
            "author": author,
            "content": content,
            "url": url,
            "timestamp": timestamp
        }

class IPSession(Entity):
    def __init__(
            self,
            label,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            protocol,
            start_time,
            end_time
    ):
        super().__init__("IP SESSION", label)
        
        self.properties = {
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "source_port": source_port,
            "destination_port": destination_port,
            "protocol": protocol,
            "start_time": start_time,
            "end_time": end_time
        }
