"""Punto de entrada principal de la aplicación.

Returns:
     Inicia el bucle principal de la interfaz gráfica.
"""

# Importamos la librería tkinter para la interfaz gráfica
import tkinter as tk
# Importamos el controlador principal que maneja la lógica de negocio
from controllers.supermercado_controller import SupermercadoController
# Importamos las vistas (ventanas) de la aplicación
from views.gui import LoginWindow, SupermercadoGUI, RegistroWindow
# Importamos el modelo de Usuario para el tipado
from models.usuario import Usuario

class Application:
    """
    Clase principal de la aplicación que gestiona el flujo de ventanas.
    """
    def __init__(self, root):
        # Guardamos la referencia a la ventana raíz de Tkinter
        self.root = root
        # Establecemos el título de la ventana principal
        self.root.title("Sistema de Supermercado")
        # Definimos el tamaño inicial de la ventana
        self.root.geometry("400x350")
        
        # Inicializa el controlador principal que orquesta la lógica del negocio
        # Se le pasan las rutas de los archivos JSON donde se guardarán los datos
        self.controller = SupermercadoController(
            archivo_productos="data/productos.json",
            archivo_ventas="data/ventas.json",
            archivo_usuarios="data/usuarios.json"
        )
        # Muestra la ventana de inicio de sesión al arrancar la aplicación
        self.show_login_window()

    def show_login_window(self):
        """Muestra la ventana de login."""
        # Limpia cualquier widget existente en la ventana
        self._clear_widgets()
        # Configura el título específico para el login
        self.root.title("Inicio de Sesión - Supermercado")
        # Ajusta el tamaño de la ventana para el login
        self.root.geometry("400x350")
        # Instancia la vista de Login, pasando el controlador y los callbacks de éxito o registro
        self.login_view = LoginWindow(self.root, self.controller, self.on_login_success, self.show_registro_window)

    def show_registro_window(self):
        """Muestra la ventana de registro de nuevos usuarios."""
        # Limpia la ventana actual
        self._clear_widgets()
        # Configura título y tamaño para el registro
        self.root.title("Registro de Usuario - Supermercado")
        self.root.geometry("400x400")
        # Instancia la vista de Registro
        self.registro_view = RegistroWindow(self.root, self.controller, self.show_login_window, self.show_login_window)

    def on_login_success(self, usuario: Usuario):
        """Callback que se ejecuta cuando el login es exitoso. Carga la interfaz principal."""
        # Limpia la ventana de login
        self._clear_widgets()
        # Actualiza el título para incluir el nombre del usuario conectado
        self.root.title(f"Supermercado - {usuario.username}")
        # Maximiza o agranda la ventana para la vista principal
        self.root.geometry("1024x768")
        # Instancia la GUI principal del supermercado
        self.main_view = SupermercadoGUI(self.root, usuario, self.controller, self.on_logout)

    def on_logout(self):
        """Callback para cerrar sesión y volver al login."""
        # Simplemente vuelve a mostrar la ventana de login
        self.show_login_window()

    def _clear_widgets(self):
        """Elimina todos los widgets de la ventana principal."""
        # Itera sobre todos los hijos de la ventana raíz y los destruye
        for widget in self.root.winfo_children():
            widget.destroy()

# Bloque principal de ejecución
if __name__ == "__main__":
    # Crea la instancia raíz de Tkinter
    root = tk.Tk()
    # Inicializa la aplicación
    app = Application(root)
    # Inicia el bucle de eventos de la interfaz gráfica
    root.mainloop()
