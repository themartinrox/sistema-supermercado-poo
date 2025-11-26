"""Representa un usuario del sistema.

Returns:
    class: Clase Usuario
"""

class Usuario:
    def __init__(self, username: str, password: str, role: str = 'comprador'):
        self.username = username
        self.password = password
        self.role = role  # 'admin' o 'comprador'

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @staticmethod
    def from_dict(data: dict):
        return Usuario(data['username'], data['password'], data.get('role', 'comprador'))
