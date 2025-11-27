"""
Modelo que representa una unidad de medida.
Define cómo se cuantifica un producto (kg, litros, unidades, etc.).
"""

class Unidad:
    """
    Clase que define una unidad de medida.
    Atributos:
        nombre (str): Nombre completo de la unidad (ej. "Kilogramo").
        abreviatura (str): Abreviatura común (ej. "kg").
    """
    def __init__(self, nombre: str, abreviatura: str = ""):
        self.nombre = nombre
        self.abreviatura = abreviatura

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            "nombre": self.nombre,
            "abreviatura": self.abreviatura
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Crea una instancia de Unidad desde un diccionario o string.
        Maneja compatibilidad con versiones anteriores donde unidad era solo un string.
        """
        # Soporte para cuando la unidad era solo un string
        if isinstance(data, str):
            return Unidad(data)
        return Unidad(data['nombre'], data.get('abreviatura', ''))

    def __str__(self):
        return self.nombre
