from dataclasses import dataclass
from models.owner import Owner
from models.building import Building
import datetime

@dataclass(frozen=True)
class OwnerBuilding:
    owner: Owner
    building: Building
    created_at: datetime