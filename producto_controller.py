"""Controlador para la gestión de productos.

Este controlador maneja:
- Carga y guardado de productos desde/hacia JSON
- Administración de inventario (stock)
- Búsqueda y filtrado de productos
- Mantenimiento de datos (limpiar, reiniciar)
"""

import os
import json
from typing import Dict, List
from models.producto import Producto
from models.categoria import Categoria
from models.unidad import Unidad

class ProductoController:
    """
    Controlador encargado de la gestión del inventario de productos.
    Maneja la carga, guardado, actualización y búsqueda de productos.
    """
    
    def __init__(self, archivo_productos: str = 'data/productos.json'):
        # Ruta donde se guardan los productos en JSON
        self.archivo_productos = archivo_productos
        # Diccionario en memoria para acceso rápido (clave: código del producto, valor: objeto Producto)
        self.productos: Dict[str, Producto] = {}
        # Cargar productos desde JSON al iniciar
        self.cargar_productos()

    def cargar_productos(self):
        """Lee el archivo JSON de productos y reconstruye los objetos Producto en memoria."""
        if os.path.exists(self.archivo_productos):
            try:
                with open(self.archivo_productos, 'r', encoding='utf-8') as f:
                    productos_data = json.load(f)
                # Convertir cada diccionario a objeto Producto, usando código como clave única
                self.productos = {p['codigo']: Producto.from_dict(p) for p in productos_data}
                print(f"Productos cargados: {len(self.productos)}")
            except Exception as e:
                print(f"Error al cargar productos: {e}")
                # Si hay error al cargar, crear productos de ejemplo
                self._crear_productos_ejemplo()
        else:
            print("No se encontró archivo de productos. Creando productos de ejemplo.")
            # Si el archivo no existe, crear los productos iniciales
            self._crear_productos_ejemplo()

    def guardar_productos(self):
        """Serializa el estado actual de los productos en el diccionario y lo escribe en el archivo JSON."""
        try:
            # Convertir cada objeto Producto a diccionario
            productos_list = [p.to_dict() for p in self.productos.values()]
            # Asegurar que el directorio exista antes de escribir
            dirpath = os.path.dirname(self.archivo_productos)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # Guardar como JSON formateado (indent=2 para que sea legible)
            with open(self.archivo_productos, 'w', encoding='utf-8') as f:
                json.dump(productos_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar productos: {e}")

    def _crear_productos_ejemplo(self):
        """Genera un set inicial de productos para demostración del sistema."""
        productos_ejemplo = [
            Producto("001", "Arroz", 1500, 50, Categoria("Abarrotes"), Unidad("kilos"), 10),
            Producto("002", "Leche", 1200, 30, Categoria("Lácteos"), Unidad("unidades"), 5),
            Producto("003", "Pan", 800, 100, Categoria("Panadería"), Unidad("unidades"), 20),
            Producto("004", "Manzanas", 2500, 4, Categoria("Frutas"), Unidad("kilos"), 5),
            Producto("005", "Pollo", 5000, 15, Categoria("Carnes"), Unidad("kilos"), 5),
        ]
        # Agregar cada producto al diccionario
        for producto in productos_ejemplo:
            self.productos[producto.codigo] = producto
        # Guardar los productos de ejemplo en el archivo JSON
        self.guardar_productos()
        print("Productos de ejemplo creados")

    def agregar_producto(self, producto: Producto) -> bool:
        """
        Registra un nuevo producto en el sistema.
        
        Retorna:
            False si el código ya existe (no se puede duplicar)
            True si se agregó exitosamente
        """
        # Verificar que el código sea único
        if producto.codigo in self.productos:
            print(f"Ya existe un producto con el código {producto.codigo}")
            return False
        
        # Agregar producto al diccionario en memoria
        self.productos[producto.codigo] = producto
        # Persistir cambios al JSON
        self.guardar_productos()
        print(f"Producto '{producto.nombre}' agregado exitosamente")
        return True

    def actualizar_stock(self, codigo: str, cantidad: float, operacion: str = 'agregar') -> bool:
        """
        Modifica el stock de un producto existente.
        
        Parámetros:
            codigo: identificador único del producto
            cantidad: cantidad a agregar o restar (siempre positiva)
            operacion: 'agregar' para aumentar stock, 'restar' para disminuir
        
        Retorna:
            False si no hay stock suficiente o el producto no existe
            True si la operación se completó
        """
        producto = self.productos.get(codigo)
        if not producto:
            print(f"Producto con código {codigo} no encontrado")
            return False
        
        # Realizar operación según el parámetro
        if operacion == 'agregar':
            producto.stock += cantidad
        elif operacion == 'restar':
            # Validar que hay suficiente stock antes de restar
            if producto.stock < cantidad:
                print(f"Stock insuficiente. Disponible: {producto.stock} {producto.unidad.nombre}")
                return False
            producto.stock -= cantidad
        
        print(f"Stock actualizado: {producto.nombre} ahora tiene {producto.stock} {producto.unidad.nombre}")
        # Verificar si el producto tiene stock bajo (< mínimo recomendado)
        if producto.tiene_stock_bajo():
            print(f"ALERTA: {producto.nombre} tiene stock bajo ({producto.stock} {producto.unidad.nombre})")
        
        # Guardar cambios en JSON
        self.guardar_productos()
        return True

    def buscar_producto(self, termino: str) -> List[Producto]:
        """
        Filtra productos por búsqueda parcial.
        
        Busca el término en:
        - Código del producto (ej: "001")
        - Nombre (ej: "Arroz")
        - Categoría (ej: "Abarrotes")
        
        Retorna lista de productos que coincidan (búsqueda case-insensitive).
        """
        termino = termino.lower()
        return [p for p in self.productos.values() if 
                termino in p.codigo.lower() or 
                termino in p.nombre.lower() or 
                termino in p.categoria.nombre.lower()]

    def obtener_productos_disponibles(self) -> List[Producto]:
        """Retorna lista de productos que tienen stock mayor a 0 (listos para vender)."""
        return [p for p in self.productos.values() if p.stock > 0]

    def obtener_productos_stock_bajo(self) -> List[Producto]:
        """Retorna lista de productos que necesitan reabastecimiento (stock bajo o cero)."""
        return [p for p in self.productos.values() if p.tiene_stock_bajo() or p.stock == 0]

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina permanentemente un producto del sistema.
        
        Retorna:
            False si el producto no existe
            True si se eliminó exitosamente
        """
        if codigo not in self.productos:
            print(f"Producto con código {codigo} no encontrado")
            return False
        
        # Obtener nombre antes de eliminar (para el mensaje de confirmación)
        producto = self.productos[codigo]
        del self.productos[codigo]
        # Persistir cambios
        self.guardar_productos()
        print(f"Producto '{producto.nombre}' eliminado exitosamente")
        return True

    def reiniciar_productos(self) -> bool:
        """Borra todo el inventario actual y restaura los productos de ejemplo."""
        try:
            # Vaciar el diccionario de productos
            self.productos.clear()
            # Recrear los productos de ejemplo
            self._crear_productos_ejemplo()
            return True
        except Exception as e:
            print(f"Error al reiniciar productos: {e}")
            return False

    def limpiar_productos(self) -> bool:
        """
        Limpia (vacía completamente) el archivo de productos.
        
        Elimina todos los productos del diccionario en memoria y guarda un JSON vacío.
        Esta acción no puede revertirse fácilmente (requiere reinicio o reimportación).
        
        Retorna:
            False si hay error al escribir el archivo
            True si se limpió exitosamente
        """
        try:
            # Vaciar diccionario en memoria
            self.productos.clear()
            # Preparar lista vacía para guardar
            productos_list = []
            # Asegurar que el directorio existe
            dirpath = os.path.dirname(self.archivo_productos)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # Guardar JSON vacío
            with open(self.archivo_productos, 'w', encoding='utf-8') as f:
                json.dump(productos_list, f, indent=2, ensure_ascii=False)
            print("Archivo de productos limpiado")
            return True
        except Exception as e:
            print(f"Error al limpiar productos: {e}")
            return False

    def resetear_inventario_cero(self) -> bool:
        """
        Pone el stock de TODOS los productos a 0, pero NO elimina los productos.
        
        Esto es útil para:
        - Reinicio después de auditoría de inventario
        - Preparación para nuevo período de ventas
        - Mantener estructura de productos (códigos, nombres, categorías) intacta
        
        Retorna:
            False si hay error
            True si todos los productos fueron reseteados exitosamente
        """
        try:
            # Iterar por todos los productos y llevar stock a 0
            for p in self.productos.values():
                # Manejar tanto números enteros como decimales (kilos puede ser 1.5)
                p.stock = 0

            # Persistir cambios en JSON
            self.guardar_productos()
            print("Inventario reseteado a 0 para todos los productos")
            return True
        except Exception as e:
            print(f"Error al resetear inventario: {e}")
            return False
