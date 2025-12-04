"""Punto de entrada principal de la aplicación.

Returns:
     Inicia el bucle principal de la interfaz gráfica.
"""

import tkinter as tk
from controllers.supermercado_controller import SupermercadoController
from views.gui import LoginWindow, SupermercadoGUI, RegistroWindow
from models.usuario import Usuario

class Application:
    """
    Clase principal de la aplicación que gestiona el flujo de ventanas.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Supermercado")
        self.root.geometry("400x350")
        
        # Inicializa el controlador principal que orquesta la lógica del negocio
        self.controller = SupermercadoController(
            archivo_productos="data/productos.json",
            archivo_ventas="data/ventas.json",
            archivo_usuarios="data/usuarios.json"
        )
        # Muestra la ventana de inicio de sesión al arrancar
        self.show_login_window()

    def show_login_window(self):
        """Muestra la ventana de login."""
        self._clear_widgets()
        self.root.title("Inicio de Sesión - Supermercado")
        self.root.geometry("400x350")
        self.login_view = LoginWindow(self.root, self.controller, self.on_login_success, self.show_registro_window)

    def show_registro_window(self):
        """Muestra la ventana de registro de nuevos usuarios."""
        self._clear_widgets()
        self.root.title("Registro de Usuario - Supermercado")
        self.root.geometry("400x400")
        self.registro_view = RegistroWindow(self.root, self.controller, self.show_login_window, self.show_login_window)

    def on_login_success(self, usuario: Usuario):
        """Callback que se ejecuta cuando el login es exitoso. Carga la interfaz principal."""
        self._clear_widgets()
        self.root.title(f"Supermercado - {usuario.username}")
        self.root.geometry("1024x768")
        self.main_view = SupermercadoGUI(self.root, usuario, self.controller, self.on_logout)

    def on_logout(self):
        """Callback para cerrar sesión y volver al login."""
        self.show_login_window()

    def _clear_widgets(self):
        """Elimina todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

    def on_logout(self):
        """Callback para cerrar sesión y volver al login."""
        self._clear_widgets()
        self.show_login_window()

    def _clear_widgets(self):
        """Elimina todos los widgets de la ventana actual para cambiar de vista."""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
