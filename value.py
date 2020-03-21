from dataclasses import  dataclass

@dataclass
class Value:
    def __init__(self, el_id, value):
        self.el_id= el_id
        self.value =value
