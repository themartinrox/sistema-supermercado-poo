"""Controlador principal del supermercado (Patrón Facade).

Este es el controlador central que actúa como intermediario entre:
- La interfaz gráfica (GUI)
- Los controladores especializados (Usuario, Producto, Venta)

El patrón Facade simplifica la API: la GUI solo necesita llamar a este controlador,
que delega internamente a los controladores específicos.
"""

from .producto_controller import ProductoController
from .usuario_controller import UsuarioController
from .venta_controller import VentaController

class SupermercadoController:
    """
    Fachada (Facade) que agrupa y coordina todos los controladores del supermercado.
    
    Beneficios de este patrón:
    - Interfaz simple para la GUI
    - Aislamiento: cambios internos no afectan la GUI
    - Delegación transparente a controladores especializados
    - Punto único de acceso a todas las operaciones
    """
    
    def __init__(self, archivo_productos: str = 'data/productos.json', 
                 archivo_ventas: str = 'data/ventas.json',
                 archivo_usuarios: str = 'data/usuarios.json'):
        """
        Inicializa el controlador del supermercado con los tres sub-controladores.
        
        Parámetros:
            archivo_productos: ruta al JSON de productos
            archivo_ventas: ruta al JSON de ventas
            archivo_usuarios: ruta al JSON de usuarios
        """
        
        # Inicialización en orden correcto: primero productos, porque venta_controller lo necesita
        self.producto_controller = ProductoController(archivo_productos)
        self.usuario_controller = UsuarioController(archivo_usuarios)
        # VentaController necesita acceso a ProductoController para validar stock
        self.venta_controller = VentaController(self.producto_controller, archivo_ventas)

    # ==================== PROPIEDADES DELEGADAS ====================
    # Estas propiedades permiten acceso directo a los datos desde la GUI
    # sin exponer los controladores internos
    
    @property
    def productos(self):
        """Acceso directo al diccionario de productos (código -> Producto)."""
        return self.producto_controller.productos
    
    @property
    def ventas(self):
        """Acceso directo a la lista de ventas (todas las transacciones registradas)."""
        return self.venta_controller.ventas
    
    @property
    def usuarios(self):
        """Acceso directo al diccionario de usuarios (RUT -> Usuario)."""
        return self.usuario_controller.usuarios

    # ==================== MÉTODOS DE CARGA/GUARDADO ====================
    
    def cargar_datos(self):
        """Recarga TODOS los datos desde los archivos JSON.
        
        Útil cuando los archivos han sido modificados externamente
        o se necesita refrescar el estado.
        """
        self.producto_controller.cargar_productos()
        self.usuario_controller.cargar_usuarios()
        self.venta_controller.cargar_ventas()

    def guardar_datos(self):
        """Guarda el estado actual de TODOS los datos a los archivos JSON.
        
        Llama al método guardar_* de cada controlador para persistir cambios.
        """
        self.producto_controller.guardar_productos()
        self.usuario_controller.guardar_usuarios()
        self.venta_controller.guardar_ventas()

    # ==================== MÉTODOS DE PRODUCTO (Delegación) ====================
    
    def agregar_producto(self, producto):
        """Delega a ProductoController: registra un nuevo producto."""
        return self.producto_controller.agregar_producto(producto)

    def actualizar_stock(self, codigo, cantidad, operacion='agregar'):
        """Delega a ProductoController: modifica stock de un producto."""
        return self.producto_controller.actualizar_stock(codigo, cantidad, operacion)

    def buscar_producto(self, termino):
        """Delega a ProductoController: busca productos por término."""
        return self.producto_controller.buscar_producto(termino)

    def obtener_productos_disponibles(self):
        """Delega a ProductoController: obtiene productos con stock > 0."""
        return self.producto_controller.obtener_productos_disponibles()

    def obtener_productos_stock_bajo(self):
        """Delega a ProductoController: obtiene productos que necesitan reabastecimiento."""
        return self.producto_controller.obtener_productos_stock_bajo()

    def eliminar_producto(self, codigo):
        """Delega a ProductoController: elimina un producto del sistema."""
        return self.producto_controller.eliminar_producto(codigo)

    def reiniciar_productos(self):
        """Delega a ProductoController: borra inventario y restaura ejemplos."""
        return self.producto_controller.reiniciar_productos()

    def limpiar_productos(self):
        """Delega a ProductoController: vacía completamente el inventario."""
        return self.producto_controller.limpiar_productos()

    def resetear_inventario_cero(self):
        """Delega a ProductoController: pone stock de todos los productos a 0."""
        return self.producto_controller.resetear_inventario_cero()

    # ==================== MÉTODOS DE USUARIO (Delegación) ====================
    
    def registrar_usuario(self, rut, password, nombre: str = '', role='comprador'):
        """Delega a UsuarioController: crea un nuevo usuario.
        
        Parámetros:
            rut: identificador del usuario (formato: 7-8 dígitos + "-" + verificador)
            password: contraseña del usuario
            nombre: nombre completo (obligatorio, solo letras y espacios)
            role: "admin" o "comprador" (default: "comprador")
        """
        return self.usuario_controller.registrar_usuario(rut, password, nombre, role)

    def autenticar_usuario(self, rut, password):
        """Delega a UsuarioController: valida credenciales para login.
        
        Parámetros:
            rut: identificador del usuario
            password: contraseña a validar
        
        Retorna:
            Objeto Usuario si credenciales son correctas
            None si no se encuentra o contraseña es incorrecta
        """
        return self.usuario_controller.autenticar_usuario(rut, password)

    def limpiar_usuarios(self, keep_admin: bool = True):
        """Delega a UsuarioController: elimina todos los usuarios.
        
        Parámetro keep_admin: si True, recrea el admin por defecto después.
        """
        return self.usuario_controller.limpiar_usuarios(keep_admin)

    def limpiar_ventas(self):
        """Delega a VentaController: borra todo el historial de ventas."""
        return self.venta_controller.limpiar_ventas()

    # ==================== MÉTODOS DE VENTA (Delegación) ====================
    
    def realizar_venta(self, items, metodo_pago=None, tarjeta=None):
        """Delega a VentaController: procesa una nueva venta.
        
        Parámetros:
            items: lista de tuplas (codigo_producto, cantidad)
            metodo_pago: "efectivo" o "tarjeta" (opcional)
            tarjeta: diccionario con numero_enmascarado y pin (solo si metodo_pago == "tarjeta")
        
        Retorna:
            Objeto Venta si se procesó exitosamente
            None si falta stock
        """
        return self.venta_controller.realizar_venta(items, metodo_pago=metodo_pago, tarjeta=tarjeta)

    def obtener_estadisticas(self):
        """Delega a VentaController: genera resumen de negocio.
        
        Retorna diccionario con:
        - total_productos: cantidad de códigos en inventario
        - total_ventas: cantidad de transacciones
        - ingresos_totales: dinero total recaudado
        - valor_inventario: valor del stock actual
        """
        return self.venta_controller.obtener_estadisticas()

