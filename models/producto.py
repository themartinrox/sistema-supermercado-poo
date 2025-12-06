"""Representa un producto en el inventario del supermercado.

Returns:
    class: Clase Producto
"""
# Importamos las clases relacionadas para composición
from .categoria import Categoria
from .unidad import Unidad

class Producto:
    """
    Clase que representa un producto individual en el inventario.
    Utiliza composición con las clases Categoria y Unidad.
    """
    def __init__(self, codigo: str, nombre: str, precio: float, stock: float, 
                 categoria: Categoria, unidad: Unidad, stock_minimo: float = 5, imagen_path: str = None):
        # Identificador único del producto
        self.codigo = codigo
        # Nombre descriptivo del producto
        self.nombre = nombre
        # Precio unitario de venta
        self.precio = precio
        # Cantidad actual disponible en inventario
        self.stock = stock
        # Categoría a la que pertenece (Objeto Categoria)
        self.categoria = categoria
        # Unidad de medida (Objeto Unidad: kg, unidades, mL)
        self.unidad = unidad
        # Cantidad mínima antes de generar alerta de reabastecimiento
        self.stock_minimo = stock_minimo
        # Ruta de la imagen del producto
        self.imagen_path = imagen_path
    
    def to_dict(self) -> dict:
        """Convierte el objeto producto a un diccionario serializable para JSON."""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            # Guardamos solo el nombre de la categoría y unidad para simplificar el JSON
            # Si son objetos, extraemos el nombre; si ya son strings, los usamos directamente
            'categoria': self.categoria.nombre if isinstance(self.categoria, Categoria) else self.categoria,
            'unidad': self.unidad.nombre if isinstance(self.unidad, Unidad) else self.unidad,
            'stock_minimo': self.stock_minimo,
            'imagen_path': self.imagen_path
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Método de fábrica para crear una instancia de Producto desde un diccionario (JSON)."""
        # Extraemos datos con valores por defecto seguros
        unidad_data = data.get('unidad', 'unidades')
        categoria_data = data.get('categoria', 'General')
        stock = data['stock']
        stock_minimo = data.get('stock_minimo', 5)
        
        # Reconstruir objetos complejos (Unidad y Categoria) desde sus representaciones (strings o dicts)
        unidad_obj = Unidad.from_dict(unidad_data)
        categoria_obj = Categoria.from_dict(categoria_data)
        
        # Validación y corrección de integridad de datos
        # Si la unidad es discreta (unidades o mL), forzamos que el stock sea entero
        if unidad_obj.nombre in ['unidades', 'mL']:
            # Asegurar que productos por unidad o mL no tengan decimales
            if isinstance(stock, float) and not stock.is_integer():
                print(f"Corrección de datos: {data['nombre']} tenía stock decimal ({stock}). Se redondeó a {round(stock)}.")
                stock = round(stock)
            
            if isinstance(stock_minimo, float) and not stock_minimo.is_integer():
                stock_minimo = round(stock_minimo)

        # Retornamos una nueva instancia de Producto
        return Producto(
            data['codigo'],
            data['nombre'],
            data['precio'],
            stock,
            categoria_obj,
            unidad_obj,
            stock_minimo,
            data.get('imagen_path')
        )
    
    def tiene_stock_bajo(self) -> bool:
        """Determina si el stock actual está por debajo del mínimo permitido."""
        # Retorna True si el stock es menor o igual al umbral definido
        return self.stock <= self.stock_minimo
    
    def __str__(self) -> str:
        """Representación en cadena del producto para logs o consola."""
        # Agrega una marca visual si el stock es bajo
        alerta = " STOCK BAJO" if self.tiene_stock_bajo() else ""
        # Formatea la salida: Código | Nombre | Precio | Stock Unidad [Alerta]
        return f"{self.codigo} | {self.nombre} | ${self.precio:,.0f} | Stock: {self.stock} {self.unidad.nombre}{alerta}"
