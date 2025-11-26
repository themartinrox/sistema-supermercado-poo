import os
import json
from typing import List, Dict, Optional
from models import Producto, Venta, Usuario

class SupermercadoController:
    """Clase que gestiona la lógica del supermercado"""
    
    def __init__(self, archivo_productos: str = 'data/productos.json', 
                 archivo_ventas: str = 'data/ventas.json',
                 archivo_usuarios: str = 'data/usuarios.json'):
        self.productos: Dict[str, Producto] = {}
        self.ventas: List[dict] = []
        self.usuarios: Dict[str, Usuario] = {}
        self.archivo_productos = archivo_productos
        self.archivo_ventas = archivo_ventas
        self.archivo_usuarios = archivo_usuarios
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos desde los archivos JSON separados"""
        # Cargar productos
        if os.path.exists(self.archivo_productos):
            try:
                with open(self.archivo_productos, 'r', encoding='utf-8') as f:
                    productos_data = json.load(f)
                self.productos = {p['codigo']: Producto.from_dict(p) for p in productos_data}
                print(f"✓ Productos cargados: {len(self.productos)}")
            except Exception as e:
                print(f"⚠️ Error al cargar productos: {e}")
                self._crear_productos_ejemplo()
        else:
            print("⚠️ No se encontró archivo de productos. Creando productos de ejemplo.")
            self._crear_productos_ejemplo()
        
        # Cargar ventas
        if os.path.exists(self.archivo_ventas):
            try:
                with open(self.archivo_ventas, 'r', encoding='utf-8') as f:
                    self.ventas = json.load(f)
                print(f"✓ Ventas cargadas: {len(self.ventas)}")
            except Exception as e:
                print(f"⚠️ Error al cargar ventas: {e}")
                self.ventas = []
        else:
            print("⚠️ No se encontró archivo de ventas. Iniciando sin ventas.")
            self.ventas = []
            self.guardar_ventas()
        
        # Cargar usuarios
        if os.path.exists(self.archivo_usuarios):
            try:
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                    usuarios_data = json.load(f)
                self.usuarios = {u['username']: Usuario.from_dict(u) for u in usuarios_data}
                print(f"✓ Usuarios cargados: {len(self.usuarios)}")
            except Exception as e:
                print(f"⚠️ Error al cargar usuarios: {e}")
                self._crear_usuarios_ejemplo()
        else:
            print("⚠️ No se encontró archivo de usuarios. Creando usuario admin.")
            self._crear_usuarios_ejemplo()
    
    def guardar_productos(self):
        """Guarda solo los productos en productos.json"""
        try:
            productos_list = [p.to_dict() for p in self.productos.values()]
            with open(self.archivo_productos, 'w', encoding='utf-8') as f:
                json.dump(productos_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar productos: {e}")
    
    def guardar_ventas(self):
        """Guarda solo las ventas en ventas.json"""
        try:
            with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
                json.dump(self.ventas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar ventas: {e}")
    
    def guardar_usuarios(self):
        """Guarda solo los usuarios en usuarios.json"""
        try:
            usuarios_list = [u.to_dict() for u in self.usuarios.values()]
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar usuarios: {e}")
    
    def guardar_datos(self):
        """Guarda todos los datos en sus respectivos archivos"""
        self.guardar_productos()
        self.guardar_ventas()
        self.guardar_usuarios()
        print("✓ Datos guardados exitosamente")

    def _crear_usuarios_ejemplo(self):
        """Crea usuario admin por defecto"""
        if "admin" not in self.usuarios:
            admin = Usuario("admin", "admin123", "admin")
            self.usuarios[admin.username] = admin
            print("✓ Usuario admin creado (user: admin, pass: admin123)")

    def registrar_usuario(self, username, password, role='comprador') -> bool:
        """Registra un nuevo usuario"""
        if username in self.usuarios:
            return False
        
        nuevo_usuario = Usuario(username, password, role)
        self.usuarios[username] = nuevo_usuario
        self.guardar_datos()
        return True

    def autenticar_usuario(self, username, password) -> Optional[Usuario]:
        """Verifica credenciales y retorna el usuario si es válido"""
        usuario = self.usuarios.get(username)
        if usuario and usuario.password == password:
            return usuario
        return None
    
    def _crear_productos_ejemplo(self):
        """Crea productos de ejemplo para demostración"""
        productos_ejemplo = [
            Producto("001", "Arroz", 1500, 50, "Abarrotes", "kilos", 10),
            Producto("002", "Leche", 1200, 30, "Lácteos", "unidades", 5),
            Producto("003", "Pan", 800, 100, "Panadería", "unidades", 20),
            Producto("004", "Manzanas", 2500, 4, "Frutas", "kilos", 5),
            Producto("005", "Pollo", 5000, 15, "Carnes", "kilos", 5),
        ]
        for producto in productos_ejemplo:
            self.productos[producto.codigo] = producto
        print("✓ Productos de ejemplo creados")
    
    def agregar_producto(self, producto: Producto) -> bool:
        """Agrega un nuevo producto al inventario"""
        if producto.codigo in self.productos:
            print(f"❌ Ya existe un producto con el código {producto.codigo}")
            return False
        
        self.productos[producto.codigo] = producto
        self.guardar_datos()
        print(f"✓ Producto '{producto.nombre}' agregado exitosamente")
        return True
    
    def actualizar_stock(self, codigo: str, cantidad: float, operacion: str = 'agregar') -> bool:
        """Actualiza el stock de un producto"""
        producto = self.productos.get(codigo)
        if not producto:
            print(f"❌ Producto con código {codigo} no encontrado")
            return False
        
        if operacion == 'agregar':
            producto.stock += cantidad
        elif operacion == 'restar':
            if producto.stock < cantidad:
                print(f"❌ Stock insuficiente. Disponible: {producto.stock} {producto.unidad}")
                return False
            producto.stock -= cantidad
        
        print(f"✓ Stock actualizado: {producto.nombre} ahora tiene {producto.stock} {producto.unidad}")
        if producto.tiene_stock_bajo():
            print(f"⚠️ ALERTA: {producto.nombre} tiene stock bajo ({producto.stock} {producto.unidad})")
        
        self.guardar_datos()
        return True
    
    def buscar_producto(self, termino: str) -> List[Producto]:
        """Busca productos por código, nombre o categoría"""
        termino = termino.lower()
        return [p for p in self.productos.values() if 
                termino in p.codigo.lower() or 
                termino in p.nombre.lower() or 
                termino in p.categoria.lower()]
    
    def obtener_productos_disponibles(self) -> List[Producto]:
        """Retorna solo productos con stock disponible"""
        return [p for p in self.productos.values() if p.stock > 0]
    
    def obtener_productos_stock_bajo(self) -> List[Producto]:
        """Retorna productos con stock bajo o sin stock"""
        return [p for p in self.productos.values() if p.tiene_stock_bajo() or p.stock == 0]
    
    def realizar_venta(self, items: List[tuple]) -> Optional[Venta]:
        """
        Realiza una venta.
        items: lista de tuplas (codigo_producto, cantidad)
        """
        venta = Venta()
        
        # Validar stock antes de procesar
        for codigo, cantidad in items:
            producto = self.productos.get(codigo)
            if not producto or producto.stock < cantidad:
                print(f"❌ Stock insuficiente para {producto.nombre if producto else 'producto desconocido'}.")
                return None
        
        # Procesar la venta
        for codigo, cantidad in items:
            producto = self.productos[codigo]
            venta.agregar_item(producto, cantidad)
            self.actualizar_stock(codigo, cantidad, 'restar')
        
        self.ventas.append(venta.to_dict())
        self.guardar_datos()
        
        return venta
    
    def obtener_estadisticas(self) -> dict:
        """Calcula estadísticas del supermercado"""
        total_productos = len(self.productos)
        total_ventas = len(self.ventas)
        ingresos_totales = sum(v['total'] for v in self.ventas)
        valor_inventario = sum(p.precio * p.stock for p in self.productos.values())
        
        return {
            'total_productos': total_productos,
            'total_ventas': total_ventas,
            'ingresos_totales': ingresos_totales,
            'valor_inventario': valor_inventario,
        }
    
    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto del inventario"""
        if codigo not in self.productos:
            print(f"❌ Producto con código {codigo} no encontrado")
            return False
        
        producto = self.productos[codigo]
        del self.productos[codigo]
        self.guardar_datos()
        print(f"✓ Producto '{producto.nombre}' eliminado exitosamente")
        return True
    
    def reiniciar_productos(self) -> bool:
        """Reinicia los productos a los valores por defecto, manteniendo ventas y usuarios"""
        try:
            self.productos.clear()
            self._crear_productos_ejemplo()
            self.guardar_datos()
            print("✓ Productos reiniciados a valores por defecto")
            return True
        except Exception as e:
            print(f"❌ Error al reiniciar productos: {e}")
            return False
