"""Modelo que representa una categoría de productos.

Returns:
    class: Clase Categoria
"""

class Categoria:
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    @staticmethod
    def from_dict(data: dict):
        # Soporte para cuando la categoría era solo un string en versiones anteriores
        if isinstance(data, str):
            return Categoria(data)
        return Categoria(data['nombre'], data.get('descripcion', ''))

    def __str__(self):
        return self.nombre
