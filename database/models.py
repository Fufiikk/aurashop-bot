from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    id: int
    title: str
    description: str
    price: int
    is_active: bool
