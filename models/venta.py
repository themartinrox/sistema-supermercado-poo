"""
Modelo que representa una venta realizada.
Contiene la información de la transacción, incluyendo items, fecha y total.
"""
from datetime import datetime
from typing import List, Optional
from .producto import Producto

class Venta:
    """
    Clase que define una transacción de venta.
    Atributos:
        id (int): Identificador único de la venta.
        items (list): Lista de diccionarios con los detalles de los productos vendidos.
        fecha (datetime): Fecha y hora de la transacción.
        total (float): Monto total de la venta.
    """
    def __init__(self, id_venta: int = None):
        self.id = id_venta
        self.items = []
        self.fecha = datetime.now()
        self.total = 0.0
    
    def agregar_item(self, producto: Producto, cantidad: float):
        """
        Agrega un producto a la venta y actualiza el total.
        Calcula el subtotal basado en el precio actual del producto.
        """
        subtotal = producto.precio * cantidad
        self.items.append({
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'precio_unitario': producto.precio,
            'subtotal': subtotal,
            'unidad': producto.unidad.nombre if hasattr(producto.unidad, 'nombre') else producto.unidad
        })
        self.total += subtotal
    
    def to_dict(self) -> dict:
        """Convierte la venta a diccionario para serialización JSON."""
        return {
            'id': self.id,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'items': self.items,
            'total': self.total
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Reconstruye una venta desde un diccionario almacenado."""
        venta = Venta(data.get('id'))
        venta.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
        venta.items = data['items']
        venta.total = data['total']
        return venta
