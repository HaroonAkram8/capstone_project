class Object():
    def __init__(self, name: str, confidence: float, location: dict):
        self.name = name
        self.confidence = confidence
        self.attributes = []

        self.location = location
    
    def __str__(self,):
        str_val = "Object("
        str_val += f"\n\tName: {self.name}"
        str_val += f"\n\tConfidence: {self.confidence}"
        str_val += f"\n\tAttributes: {self.attributes}"
        str_val += f"\n\tLocation: {self.location}"
        str_val += f"\n)"

        return str_val