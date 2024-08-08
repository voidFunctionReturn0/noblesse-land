from dataclasses import dataclass

@dataclass
class Owner:
    name: str
    position: str
    relation: str = None # 일시적으로만 nullable이고, DB에 저장할 떄는 Not null
    organization: str = None
    image_path: str = None