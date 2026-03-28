from typing import Literal

from pydantic import BaseModel, Field

TYPE_LOCAL_VALUES = Literal[
    "Appartement",
    "Maison",
    "Dépendance",
    "Local industriel. commercial ou assimilé",
]


class EstimateRequest(BaseModel):
    surface_reelle_bati: float = Field(..., ge=0)
    nombre_pieces_principales: float = Field(..., ge=0)
    code_departement: str = Field(..., min_length=2, max_length=3)
    type_local: TYPE_LOCAL_VALUES
    code_commune: str = Field(..., min_length=1)


class EstimateRequestOptionalBounds(BaseModel):
    """Optional: for future value range / confidence interval support."""
    pass