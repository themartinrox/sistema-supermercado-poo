from datetime import datetime
from .producto import Producto

"""Representa una venta realizada"""

class Venta:
    def __init__(self):
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
            'unidad': producto.unidad
        })
        self.total += subtotal
    
    def to_dict(self) -> dict:
        """Convierte la venta a diccionario"""
        return {
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'items': self.items,
            'total': self.total
        }
