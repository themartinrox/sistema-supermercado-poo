"""
Modelo que representa una categoría de productos.
Permite agrupar productos bajo una clasificación común.
"""

class Categoria:
    """
    Clase que define una categoría de producto.
    Atributos:
        nombre (str): El nombre de la categoría (ej. "Lácteos").
        descripcion (str): Una breve descripción de la categoría.
    """
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Crea una instancia de Categoria desde un diccionario o string.
        Maneja compatibilidad con versiones anteriores donde categoria era solo un string.
        """
        # Soporte para cuando la categoría era solo un string en versiones anteriores
        if isinstance(data, str):
            return Categoria(data)
        return Categoria(data['nombre'], data.get('descripcion', ''))

    def __str__(self):
        return self.nombre
