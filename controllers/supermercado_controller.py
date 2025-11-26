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
    Mantiene la compatibilidad con el código existente que espera un único controlador.
    """
    
    def __init__(self, archivo_productos: str = 'data/productos.json', 
                 archivo_ventas: str = 'data/ventas.json',
                 archivo_usuarios: str = 'data/usuarios.json'):
        
        self.producto_controller = ProductoController(archivo_productos)
        self.usuario_controller = UsuarioController(archivo_usuarios)
        self.venta_controller = VentaController(self.producto_controller, archivo_ventas)

    # Delegación de propiedades para mantener compatibilidad
    @property
    def productos(self):
        return self.producto_controller.productos
    
    @property
    def ventas(self):
        return self.venta_controller.ventas
    
    @property
    def usuarios(self):
        return self.usuario_controller.usuarios

    # Delegación de métodos
    def cargar_datos(self):
        self.producto_controller.cargar_productos()
        self.usuario_controller.cargar_usuarios()
        self.venta_controller.cargar_ventas()

    def guardar_datos(self):
        self.producto_controller.guardar_productos()
        self.usuario_controller.guardar_usuarios()
        self.venta_controller.guardar_ventas()

    # Métodos de Producto
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
        return self.producto_controller.reiniciar_productos()

    # Métodos de Usuario
    def registrar_usuario(self, username, password, role='comprador'):
        return self.usuario_controller.registrar_usuario(username, password, role)

    def autenticar_usuario(self, username, password):
        return self.usuario_controller.autenticar_usuario(username, password)

    # Métodos de Venta
    def realizar_venta(self, items):
        return self.venta_controller.realizar_venta(items)

    def obtener_estadisticas(self):
        return self.venta_controller.obtener_estadisticas()

