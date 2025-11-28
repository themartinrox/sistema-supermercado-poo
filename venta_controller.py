"""Controlador para la gestión de ventas.

Este controlador maneja:
- Registro de transacciones con detalles de pago (efectivo/tarjeta)
- Validación de stock antes de procesar ventas
- Cálculo de totales y descuento de inventario
- Historial y estadísticas de ventas
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
        # Ruta donde se guardan las ventas en JSON
        self.archivo_ventas = archivo_ventas
        # Referencia al controlador de productos (necesario para validar y descontar stock)
        self.producto_controller = producto_controller
        # Lista en memoria con todas las ventas (cada venta es un diccionario serializado)
        self.ventas: List[dict] = []
        # Cargar ventas existentes desde archivo al iniciar
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
                # Si hay error, iniciar con lista vacía
                self.ventas = []
        else:
            print("No se encontró archivo de ventas. Iniciando sin ventas.")
            # Si el archivo no existe, crear una lista vacía
            self.ventas = []
            # Guardar el archivo vacío para crear la estructura
            self.guardar_ventas()

    def guardar_ventas(self):
        """Persiste el historial de ventas actualizado al archivo JSON."""
        try:
            # Asegurar que el directorio exista antes de escribir
            dirpath = os.path.dirname(self.archivo_ventas)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # Guardar lista de ventas como JSON formateado
            with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
                json.dump(self.ventas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar ventas: {e}")

    def limpiar_ventas(self) -> bool:
        """
        Limpia completamente el historial de ventas (borra archivo y memoria).
        
        Esta acción elimina TODA la historia de transacciones.
        Úsese con cuidado ya que no puede revertirse fácilmente.
        
        Retorna:
            False si hay error al escribir el archivo
            True si se limpió exitosamente
        """
        try:
            # Vaciar la lista de ventas en memoria
            self.ventas = []
            # Asegurar que el directorio existe
            dirpath = os.path.dirname(self.archivo_ventas)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # Guardar lista vacía en JSON
            with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
                json.dump(self.ventas, f, indent=2, ensure_ascii=False)
            print("Archivo de ventas limpiado")
            return True
        except Exception as e:
            print(f"Error al limpiar ventas: {e}")
            return False

    def obtener_siguiente_id(self) -> int:
        """
        Genera un ID autoincremental (único) para la próxima venta.
        
        Busca el ID más alto en el historial existente y le suma 1.
        Ejemplo: si hay ventas con IDs 1,2,3 devuelve 4.
        
        Retorna:
            int: el próximo ID disponible (mínimo 1)
        """
        if not self.ventas:
            # Si no hay ventas, comenzar con ID 1
            return 1
        
        # Buscar el ID máximo actual. Asumimos que las ventas tienen 'id'.
        # Si hay ventas antiguas sin ID, las ignoramos y asumimos que su id es 0.
        max_id = 0
        for v in self.ventas:
            v_id = v.get('id')  # Obtener el 'id' del diccionario de venta
            if isinstance(v_id, int) and v_id > max_id:
                max_id = v_id
        return max_id + 1

    def realizar_venta(self, items: List[tuple], metodo_pago: Optional[str] = None, tarjeta: Optional[dict] = None) -> Optional[Venta]:
        """
        Procesa una nueva venta completa (venta y actualización de stock).
        
        Proceso:
        1. Valida que hay stock suficiente para TODOS los items
        2. Si la validación falla, cancela toda la venta (transaccionalidad)
        3. Si es válida, crea la venta y descuenta stock de cada producto
        4. Registra información de pago (método y datos de tarjeta si aplica)
        5. Guarda todo en JSON y retorna la venta procesada
        
        Parámetros:
            items: lista de tuplas (codigo_producto, cantidad) a comprar
            metodo_pago: "efectivo" o "tarjeta" (opcional, default None)
            tarjeta: diccionario con "numero_enmascarado" y "pin" (solo si metodo_pago == "tarjeta")
        
        Retorna:
            Objeto Venta si se procesó exitosamente
            None si falla la validación de stock
        """
        # Generar ID único para esta venta
        nuevo_id = self.obtener_siguiente_id()
        venta = Venta(id_venta=nuevo_id)
        # Guardar información de pago en el objeto venta
        venta.metodo_pago = metodo_pago
        venta.tarjeta = tarjeta
        
        # VALIDAR STOCK: verificar que hay suficiente stock para TODOS los items ANTES de procesar
        # (transaccionalidad básica: todo o nada)
        for codigo, cantidad in items:
            producto = self.producto_controller.productos.get(codigo)
            if not producto or producto.stock < cantidad:
                # Si falta stock, no procesar ningún item
                print(f"Stock insuficiente para {producto.nombre if producto else 'producto desconocido'}.")
                return None
        
        # PROCESAR VENTA: ahora que sabemos que hay stock, descontar y registrar
        for codigo, cantidad in items:
            producto = self.producto_controller.productos[codigo]
            # Agregar item a la venta (suma total)
            venta.agregar_item(producto, cantidad)
            # Descontar stock del producto (actualizar inventario)
            self.producto_controller.actualizar_stock(codigo, cantidad, 'restar')
        
        # Guardar la venta en memoria (como diccionario serializable a JSON)
        self.ventas.append(venta.to_dict())
        # Persistir cambios a archivo JSON
        self.guardar_ventas()
        
        return venta

    def obtener_estadisticas(self) -> dict:
        """
        Genera un resumen estadístico completo del negocio.
        
        Calcula:
        - total_productos: cantidad de códigos de producto en el inventario
        - total_ventas: cantidad de transacciones registradas
        - ingresos_totales: suma de todos los totales de ventas (en dinero)
        - valor_inventario: valor total del stock actual en dinero
        
        Retorna:
            Diccionario con los 4 indicadores clave del negocio
        """
        # Contar cantidad de productos diferentes en el inventario
        total_productos = len(self.producto_controller.productos)
        # Contar cantidad de ventas registradas
        total_ventas = len(self.ventas)
        # Sumar todos los montos de las ventas
        ingresos_totales = sum(v['total'] for v in self.ventas)
        # Calcular valor total del inventario = Σ(precio × stock) para cada producto
        valor_inventario = sum(p.precio * p.stock for p in self.producto_controller.productos.values())
        
        return {
            'total_productos': total_productos,
            'total_ventas': total_ventas,
            'ingresos_totales': ingresos_totales,
            'valor_inventario': valor_inventario,
        }
