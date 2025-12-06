"""Controlador principal del supermercado (Fachada).

Returns:
    class: Clase SupermercadoController
"""

from .producto_controller import ProductoController
from .usuario_controller import UsuarioController
from .venta_controller import VentaController

class SupermercadoController:
    """
    Fachada que agrupa los controladores específicos del supermercado.
    Actúa como punto único de acceso para la interfaz gráfica, delegando
    las operaciones a los controladores especializados.
    """
    
    def __init__(self, archivo_productos: str = 'data/productos.json', 
                 archivo_ventas: str = 'data/ventas.json',
                 archivo_usuarios: str = 'data/usuarios.json'):
        
        # Inicialización de sub-controladores
        # Cada controlador maneja un aspecto específico del dominio
        self.producto_controller = ProductoController(archivo_productos)
        self.usuario_controller = UsuarioController(archivo_usuarios)
        # El controlador de ventas necesita acceso a productos para validar stock
        self.venta_controller = VentaController(self.producto_controller, archivo_ventas)

    # Delegación de propiedades para mantener compatibilidad con la vista
    # Esto permite que la GUI acceda a 'controller.productos' directamente
    @property
    def productos(self):
        """Acceso directo al diccionario de productos."""
        return self.producto_controller.productos
    
    @property
    def ventas(self):
        """Acceso directo a la lista de ventas."""
        return self.venta_controller.ventas
    
    @property
    def usuarios(self):
        """Acceso directo al diccionario de usuarios."""
        return self.usuario_controller.usuarios

    # Delegación de métodos de gestión de datos
    def cargar_datos(self):
        """Recarga todos los datos desde los archivos JSON."""
        self.producto_controller.cargar_productos()
        self.usuario_controller.cargar_usuarios()
        self.venta_controller.cargar_ventas()

    def guardar_datos(self):
        """Guarda todos los datos actuales en los archivos JSON."""
        self.producto_controller.guardar_productos()
        self.usuario_controller.guardar_usuarios()
        self.venta_controller.guardar_ventas()

    # Métodos de Producto (Delegación)
    # Estos métodos redirigen las llamadas al controlador de productos
    def agregar_producto(self, producto):
        return self.producto_controller.agregar_producto(producto)

    def actualizar_stock(self, codigo, cantidad, operacion='agregar'):
        return self.producto_controller.actualizar_stock(codigo, cantidad, operacion)

    def buscar_producto(self, termino):
        return self.producto_controller.buscar_producto(termino)

    def obtener_productos_disponibles(self):
        return self.producto_controller.obtener_productos_disponibles()

    def obtener_productos_stock_bajo(self):
        return self.producto_controller.obtener_productos_stock_bajo()

    def eliminar_producto(self, codigo):
        return self.producto_controller.eliminar_producto(codigo)

    def reiniciar_productos(self):
        # Método opcional para resetear datos (si existe en el controlador)
        if hasattr(self.producto_controller, 'reiniciar_productos'):
            return self.producto_controller.reiniciar_productos()

    def exportar_inventario_csv(self, ruta):
        return self.producto_controller.exportar_a_csv(ruta)

    # Métodos de Usuario (Delegación)
    def registrar_usuario(self, username, password, role='comprador'):
        return self.usuario_controller.registrar_usuario(username, password, role)

    def autenticar_usuario(self, username, password):
        return self.usuario_controller.autenticar_usuario(username, password)

    def cambiar_password(self, username, old_pass, new_pass):
        return self.usuario_controller.cambiar_password(username, old_pass, new_pass)

    # Métodos de Venta (Delegación)
    def realizar_venta(self, items, descuento=0.0):
        return self.venta_controller.realizar_venta(items, descuento)

    def obtener_estadisticas(self):
        # Si el controlador de ventas tiene estadísticas, las retorna
        if hasattr(self.venta_controller, 'obtener_estadisticas'):
            return self.venta_controller.obtener_estadisticas()
        return {}


