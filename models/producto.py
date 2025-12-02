"""Representa un producto en el inventario del supermercado.

Returns:
    class: Clase Producto
"""
from .categoria import Categoria
from .unidad import Unidad

class Producto:
    """
    Clase que representa un producto individual en el inventario.
    Utiliza composición con las clases Categoria y Unidad.
    """
    def __init__(self, codigo: str, nombre: str, precio: float, stock: float, 
                 categoria: Categoria, unidad: Unidad, stock_minimo: float = 5):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria  # Objeto de tipo Categoria
        self.unidad = unidad        # Objeto de tipo Unidad
        self.stock_minimo = stock_minimo # Umbral para alerta de stock bajo
    
    def to_dict(self) -> dict:
        """Convierte el objeto producto a un diccionario serializable para JSON."""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            # Guardamos solo el nombre de la categoría y unidad para simplificar el JSON
            'categoria': self.categoria.nombre if isinstance(self.categoria, Categoria) else self.categoria,
            'unidad': self.unidad.nombre if isinstance(self.unidad, Unidad) else self.unidad,
            'stock_minimo': self.stock_minimo
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Método de fábrica para crear una instancia de Producto desde un diccionario (JSON)."""
        unidad_data = data.get('unidad', 'unidades')
        categoria_data = data.get('categoria', 'General')
        stock = data['stock']
        stock_minimo = data.get('stock_minimo', 5)
        
        # Reconstruir objetos complejos desde strings
        unidad_obj = Unidad.from_dict(unidad_data)
        categoria_obj = Categoria.from_dict(categoria_data)
        
        # Validación y corrección de integridad de datos
        if unidad_obj.nombre == 'unidades':
            # Asegurar que productos por unidad no tengan decimales
            if isinstance(stock, float) and not stock.is_integer():
                print(f"Corrección de datos: {data['nombre']} tenía stock decimal ({stock}). Se redondeó a {round(stock)}.")
                stock = round(stock)
            
            if isinstance(stock_minimo, float) and not stock_minimo.is_integer():
                stock_minimo = round(stock_minimo)

        return Producto(
            data['codigo'],
            data['nombre'],
            data['precio'],
            stock,
            categoria_obj,
            unidad_obj,
            stock_minimo
        )
    
    def tiene_stock_bajo(self) -> bool:
        """Determina si el stock actual está por debajo del mínimo permitido."""
        return self.stock <= self.stock_minimo
    
    def __str__(self) -> str:
        """Representación en cadena del producto para logs o consola."""
        alerta = " STOCK BAJO" if self.tiene_stock_bajo() else ""
        return f"{self.codigo} | {self.nombre} | ${self.precio:,.0f} | Stock: {self.stock} {self.unidad.nombre}{alerta}"
