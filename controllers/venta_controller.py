"""Controlador para la gestión de ventas.

Returns:
    class: Clase VentaController
"""

import os
import json
from typing import List, Optional
from models.venta import Venta
from .producto_controller import ProductoController

class VentaController:
    """
    Controlador encargado de procesar las ventas y generar reportes.
    Mantiene el historial de transacciones.
    """
    
    def __init__(self, producto_controller: ProductoController, archivo_ventas: str = 'data/ventas.json'):
        self.archivo_ventas = archivo_ventas
        self.producto_controller = producto_controller # Dependencia para validar stock
        self.ventas: List[dict] = []
        self.cargar_ventas()

    def cargar_ventas(self):
        """Carga el historial de ventas desde el archivo JSON."""
        if os.path.exists(self.archivo_ventas):
            try:
                with open(self.archivo_ventas, 'r', encoding='utf-8') as f:
                    self.ventas = json.load(f)
                print(f"Ventas cargadas: {len(self.ventas)}")
            except Exception as e:
                print(f"Error al cargar ventas: {e}")
                self.ventas = []
        else:
            print("No se encontró archivo de ventas. Iniciando sin ventas.")
            self.ventas = []
            self.guardar_ventas()

    def guardar_ventas(self):
        """Guarda el historial de ventas actualizado en el archivo JSON."""
        try:
            with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
                json.dump(self.ventas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar ventas: {e}")

    def obtener_siguiente_id(self) -> int:
        """
        Genera un ID autoincremental para la próxima venta.
        Busca el ID más alto existente y le suma 1.
        """
        if not self.ventas:
            return 1
        
        # Buscar el ID máximo actual. Asumimos que las ventas tienen 'id'.
        # Si hay ventas antiguas sin ID, las ignoramos o asumimos 0.
        max_id = 0
        for v in self.ventas:
            v_id = v.get('id')
            if isinstance(v_id, int) and v_id > max_id:
                max_id = v_id
        return max_id + 1

    def realizar_venta(self, items: List[tuple]) -> Optional[Venta]:
        """
        Procesa una nueva venta.
        1. Valida stock suficiente para todos los items.
        2. Descuenta stock.
        3. Registra la venta.
        items: lista de tuplas (codigo_producto, cantidad)
        """
        # Generar ID único para la venta
        nuevo_id = self.obtener_siguiente_id()
        venta = Venta(id_venta=nuevo_id)
        
        # Validar stock antes de procesar (Transaccionalidad básica)
        for codigo, cantidad in items:
            producto = self.producto_controller.productos.get(codigo)
            if not producto or producto.stock < cantidad:
                print(f"Stock insuficiente para {producto.nombre if producto else 'producto desconocido'}.")
                return None
        
        # Procesar la venta (Descontar stock y agregar items)
        for codigo, cantidad in items:
            producto = self.producto_controller.productos[codigo]
            venta.agregar_item(producto, cantidad)
            self.producto_controller.actualizar_stock(codigo, cantidad, 'restar')
        
        self.ventas.append(venta.to_dict())
        self.guardar_ventas()
        
        return venta

    def obtener_estadisticas(self) -> dict:
        """
        Genera un resumen estadístico del negocio.
        Incluye total de productos, ventas, ingresos y valor del inventario.
        """
        total_productos = len(self.producto_controller.productos)
        total_ventas = len(self.ventas)
        ingresos_totales = sum(v['total'] for v in self.ventas)
        valor_inventario = sum(p.precio * p.stock for p in self.producto_controller.productos.values())
        
        return {
            'total_productos': total_productos,
            'total_ventas': total_ventas,
            'ingresos_totales': ingresos_totales,
            'valor_inventario': valor_inventario,
        }
