"""Representa un producto en el inventario del supermercado"""

class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: float, 
                 categoria: str, unidad: str = "unidades", stock_minimo: float = 5):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.unidad = unidad  # "unidades" o "kilos"
        self.stock_minimo = stock_minimo
    
    def to_dict(self) -> dict:
        """Convierte el producto a diccionario para guardar en JSON"""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria,
            'unidad': self.unidad,
            'stock_minimo': self.stock_minimo
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Crea un producto desde un diccionario"""
        unidad = data.get('unidad', 'unidades')
        stock = data['stock']
        stock_minimo = data.get('stock_minimo', 5)
        
        # Validación y corrección de datos corruptos/inválidos desde JSON
        if unidad == 'unidades':
            # Si es unidades pero tiene decimales, corregir
            if isinstance(stock, float) and not stock.is_integer():
                print(f"⚠️ Corrección de datos: {data['nombre']} tenía stock decimal ({stock}). Se redondeó a {round(stock)}.")
                stock = round(stock)
            
            if isinstance(stock_minimo, float) and not stock_minimo.is_integer():
                stock_minimo = round(stock_minimo)

        return Producto(
            data['codigo'],
            data['nombre'],
            data['precio'],
            stock,
            data['categoria'],
            unidad,
            stock_minimo
        )
    
    def tiene_stock_bajo(self) -> bool:
        """Verifica si el producto tiene stock bajo"""
        return self.stock <= self.stock_minimo
    
    def __str__(self) -> str:
        alerta = " ⚠️ STOCK BAJO" if self.tiene_stock_bajo() else ""
        return f"{self.codigo} | {self.nombre} | ${self.precio:,.0f} | Stock: {self.stock} {self.unidad}{alerta}"
