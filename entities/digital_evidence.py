from entities.base.entity import Entity

class File(Entity):
    def __init__(
            self,
            label,
            filename,
            file_type,
            file_size,
            creation_date
    ):
        super().__init__("FILE", label)
        
        self.properties = {
            "filename": filename,
            "file_type": file_type,
            "file_size": file_size,
            "creation_date": creation_date
        }

class Image(Entity):
    def __init__(
            self,
            label,
            filename,
            format,
            resolution,
            file_size,
            creation_date
    ):
        super().__init__("IMAGE", label)
        
        self.properties = {
            "filename": filename,
            "format": format,
            "resolution": resolution,
            "file_size": file_size,
            "creation_date": creation_date
        }

class Video(Entity):
    def __init__(
            self,
            label,
            filename,
            format,
            resolution,
            file_size,
            creation_date
    ):
        super().__init__("VIDEO", label)
        
        self.properties = {
            "filename": filename,
            "format": format,
            "resolution": resolution,
            "file_size": file_size,
            "creation_date": creation_date
        }