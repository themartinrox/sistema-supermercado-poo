"""Controlador para la gestión de productos.

Returns:
    class: Clase ProductoController
"""

import os
import json
from typing import Dict, List
from models.producto import Producto
from models.categoria import Categoria
from models.unidad import Unidad

class ProductoController:
    """Controlador encargado de la gestión de productos."""
    
    def __init__(self, archivo_productos: str = 'data/productos.json'):
        self.archivo_productos = archivo_productos
        self.productos: Dict[str, Producto] = {}
        self.cargar_productos()

    def cargar_productos(self):
        """Carga los productos desde el archivo JSON."""
        if os.path.exists(self.archivo_productos):
            try:
                with open(self.archivo_productos, 'r', encoding='utf-8') as f:
                    productos_data = json.load(f)
                self.productos = {p['codigo']: Producto.from_dict(p) for p in productos_data}
                print(f"Productos cargados: {len(self.productos)}")
            except Exception as e:
                print(f"Error al cargar productos: {e}")
                self._crear_productos_ejemplo()
        else:
            print("No se encontró archivo de productos. Creando productos de ejemplo.")
            self._crear_productos_ejemplo()

    def guardar_productos(self):
        """Guarda los productos en el archivo JSON."""
        try:
            productos_list = [p.to_dict() for p in self.productos.values()]
            with open(self.archivo_productos, 'w', encoding='utf-8') as f:
                json.dump(productos_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar productos: {e}")

    def _crear_productos_ejemplo(self):
        """Crea productos de ejemplo si no existen datos."""
        productos_ejemplo = [
            Producto("001", "Arroz", 1500, 50, Categoria("Abarrotes"), Unidad("kilos"), 10),
            Producto("002", "Leche", 1200, 30, Categoria("Lácteos"), Unidad("unidades"), 5),
            Producto("003", "Pan", 800, 100, Categoria("Panadería"), Unidad("unidades"), 20),
            Producto("004", "Manzanas", 2500, 4, Categoria("Frutas"), Unidad("kilos"), 5),
            Producto("005", "Pollo", 5000, 15, Categoria("Carnes"), Unidad("kilos"), 5),
        ]
        for producto in productos_ejemplo:
            self.productos[producto.codigo] = producto
        self.guardar_productos()
        print("Productos de ejemplo creados")

    def agregar_producto(self, producto: Producto) -> bool:
        """Agrega un nuevo producto al inventario."""
        if producto.codigo in self.productos:
            print(f"Ya existe un producto con el código {producto.codigo}")
            return False
        
        self.productos[producto.codigo] = producto
        self.guardar_productos()
        print(f"Producto '{producto.nombre}' agregado exitosamente")
        return True

    def actualizar_stock(self, codigo: str, cantidad: float, operacion: str = 'agregar') -> bool:
        """Actualiza el stock de un producto."""
        producto = self.productos.get(codigo)
        if not producto:
            print(f"Producto con código {codigo} no encontrado")
            return False
        
        if operacion == 'agregar':
            producto.stock += cantidad
        elif operacion == 'restar':
            if producto.stock < cantidad:
                print(f"Stock insuficiente. Disponible: {producto.stock} {producto.unidad.nombre}")
                return False
            producto.stock -= cantidad
        
        print(f"Stock actualizado: {producto.nombre} ahora tiene {producto.stock} {producto.unidad.nombre}")
        if producto.tiene_stock_bajo():
            print(f"ALERTA: {producto.nombre} tiene stock bajo ({producto.stock} {producto.unidad.nombre})")
        
        self.guardar_productos()
        return True

    def buscar_producto(self, termino: str) -> List[Producto]:
        """Busca productos por código, nombre o categoría."""
        termino = termino.lower()
        return [p for p in self.productos.values() if 
                termino in p.codigo.lower() or 
                termino in p.nombre.lower() or 
                termino in p.categoria.nombre.lower()]

    def obtener_productos_disponibles(self) -> List[Producto]:
        """Retorna solo productos con stock disponible."""
        return [p for p in self.productos.values() if p.stock > 0]

    def obtener_productos_stock_bajo(self) -> List[Producto]:
        """Retorna productos con stock bajo o sin stock."""
        return [p for p in self.productos.values() if p.tiene_stock_bajo() or p.stock == 0]

    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto del inventario."""
        if codigo not in self.productos:
            print(f"Producto con código {codigo} no encontrado")
            return False
        
        producto = self.productos[codigo]
        del self.productos[codigo]
        self.guardar_productos()
        print(f"Producto '{producto.nombre}' eliminado exitosamente")
        return True

    def reiniciar_productos(self) -> bool:
        """Reinicia los productos a los valores por defecto."""
        try:
            self.productos.clear()
            self._crear_productos_ejemplo()
            return True
        except Exception as e:
            print(f"Error al reiniciar productos: {e}")
            return False
