"""
Modelo que representa una venta realizada.
Contiene la información de la transacción, incluyendo items, fecha y total.
"""
from datetime import datetime
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
        # ID único de la venta (asignado por el controlador)
        self.id = id_venta
        # Lista para almacenar los productos agregados a la venta
        self.items = []
        # Fecha y hora actual de creación de la venta
        self.fecha = datetime.now()
        # Acumulador del monto total de la venta
        self.total = 0.0
        # Descuento aplicado (porcentaje o monto fijo, aquí asumiremos porcentaje por simplicidad en la vista)
        self.descuento = 0.0
    
    def agregar_item(self, producto: Producto, cantidad: float):
        """
        Agrega un producto a la venta y actualiza el total.
        Calcula el subtotal basado en el precio actual del producto.
        """
        # Calcula el costo total para este item (precio * cantidad)
        subtotal = producto.precio * cantidad
        
        # Agrega el detalle del item a la lista
        # Guardamos una copia de los datos relevantes para mantener el histórico
        # incluso si el producto cambia de precio o nombre en el futuro
        self.items.append({
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'precio_unitario': producto.precio,
            'subtotal': subtotal,
            # Guardamos la unidad para saber si fue kg, unidades, etc.
            'unidad': producto.unidad.nombre if hasattr(producto.unidad, 'nombre') else producto.unidad
        })
        # Actualiza el total general de la venta
        self.total += subtotal
    
    def to_dict(self) -> dict:
        """Convierte la venta a diccionario para serialización JSON."""
        return {
            'id': self.id,
            # Convertimos la fecha a string para poder guardarla en JSON
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'items': self.items,
            'total': self.total,
            'descuento': self.descuento
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Reconstruye un objeto Venta desde un diccionario."""
        # Crea una nueva instancia de Venta
        venta = Venta(data['id'])
        # Parsea la fecha desde el string guardado
        venta.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
        # Restaura los items y el total
        venta.items = data['items']
        venta.total = data['total']
        venta.descuento = data.get('descuento', 0.0)
        return venta
