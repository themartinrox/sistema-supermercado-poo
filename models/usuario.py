"""
Modelo que representa un usuario dentro del sistema de gestión.
Se encarga de almacenar y manejar la información relacionada con la
identidad del usuario, incluyendo sus credenciales de acceso y el rol
que desempeña dentro de la aplicación.
"""

class Usuario:
    """
    Clase que define la estructura y comportamiento básico de un usuario.

    Atributos:
        username (str): Nombre de usuario único que se utiliza para iniciar sesión.
        password (str): Contraseña asociada al usuario para autenticación.
        role (str): Rol asignado al usuario, el cual determina sus permisos
                    dentro del sistema. Puede ser 'admin' o 'comprador'.
    """

    def __init__(self, username: str, password: str, role: str = 'comprador'):
        """
        Inicializa una nueva instancia de Usuario.

        Args:
            username (str): Identificador único del usuario.
            password (str): Clave secreta utilizada para validar su acceso.
            role (str, opcional): Tipo de usuario según sus privilegios.
                                  Por defecto se asigna 'comprador'.
        """
        self.username = username
        self.password = password
        self.role = role  # Puede tomar valores como 'admin' o 'comprador'

    def to_dict(self) -> dict:
        """
        Convierte el objeto Usuario en un diccionario estándar de Python.
        Este diccionario puede ser utilizado para serialización en formato JSON
        o para almacenar los datos en archivos o bases de datos.

        Returns:
            dict: Diccionario con los datos del usuario.
        """
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Genera una instancia de Usuario a partir de un diccionario previamente
        obtenido desde una fuente externa, como un archivo JSON o una base de datos.

        Args:
            data (dict): Diccionario que contiene los valores necesarios para
                         reconstruir un usuario. Se espera que incluya al menos
                         'username' y 'password'. Si no contiene 'role', se
                         asignará 'comprador' por defecto.

        Returns:
            Usuario: Nueva instancia creada con los datos proporcionados.
        """
        return Usuario(
            data['username'],
            data['password'],
            data.get('role', 'comprador')
        )
