"""Representa una venta realizada.

Returns:
    class: Clase Venta
"""
from datetime import datetime
from .producto import Producto

class Venta:
    def __init__(self, id_venta: int = None):
        self.id = id_venta
        self.items = []
        self.fecha = datetime.now()
        self.total = 0.0
    
    def agregar_item(self, producto: Producto, cantidad: float):
        """Agrega un item a la venta"""
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
        """Convierte la venta a diccionario"""
        return {
            'id': self.id,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'items': self.items,
            'total': self.total
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Crea una venta desde un diccionario"""
        venta = Venta(data.get('id'))
        venta.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
        venta.items = data['items']
        venta.total = data['total']
        return venta
