"""
Modelo que representa un usuario del sistema.
Maneja la información de autenticación y roles.
"""

class Usuario:
    """
    Clase que define un usuario del sistema.
    Atributos:
        username (str): Nombre de usuario único.
        password (str): Contraseña del usuario.
        role (str): Rol del usuario ('admin' o 'comprador').
    """
    def __init__(self, username: str, password: str, role: str = 'comprador'):
        self.username = username
        self.password = password
        self.role = role  # 'admin' o 'comprador'

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @staticmethod
    def from_dict(data: dict):
        """Crea una instancia de Usuario desde un diccionario."""
        return Usuario(data['username'], data['password'], data.get('role', 'comprador'))
