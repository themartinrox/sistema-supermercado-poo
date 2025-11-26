"""Modelo que representa una unidad de medida.

Returns:
    class: Clase Unidad
"""
class Unidad:
    def __init__(self, nombre: str, abreviatura: str = ""):
        self.nombre = nombre
        self.abreviatura = abreviatura

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "abreviatura": self.abreviatura
        }

    @staticmethod
    def from_dict(data: dict):
        # Soporte para cuando la unidad era solo un string
        if isinstance(data, str):
            return Unidad(data)
        return Unidad(data['nombre'], data.get('abreviatura', ''))

    def __str__(self):
        return self.nombre
