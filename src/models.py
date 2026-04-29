from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Ingredient:
    category: str
    material_name: str
    amount: Optional[float]
    unit: str
    position: int
    solids_pct: Optional[float] = None


@dataclass
class Formulation:
    project_name: str
    product_type: str
    version: str
    author: str
    notes: str
    measured_viscosity: Optional[float]
    measured_ph: Optional[float]
    measured_density: Optional[float]
    measured_solids: Optional[float]
    ingredients: List[Ingredient] = field(default_factory=list)