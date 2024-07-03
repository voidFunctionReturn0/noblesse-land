from dataclasses import dataclass

@dataclass
class Owner:
    name: str
    organization: str
    position: str
    image_path: str
    relation: str = None