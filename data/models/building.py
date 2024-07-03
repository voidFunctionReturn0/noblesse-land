from dataclasses import dataclass
from typing import Optional
from models.coordinates import Coordinates

@dataclass
class Building:
    type: str
    details: str
    price: int
    note: str
    coordinates: Optional[Coordinates] = None