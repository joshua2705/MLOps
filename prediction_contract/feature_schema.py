TARGET_NAME: str = "valeur_fonciere"

TYPE_LOCAL_CATEGORIES: list[str] = [
    "Appartement",
    "Maison",
    "Dépendance",
    "Local industriel. commercial ou assimilé",
]

MODEL_FEATURE_NAMES: list[str] = [
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "code_departement",
    "code_commune",
    *[f"type_local_{c}" for c in TYPE_LOCAL_CATEGORIES],
]