"""Controlador para la gestión de usuarios.

Returns:
    class: Clase UsuarioController
"""

import os
import json
from typing import Dict, Optional
from models.usuario import Usuario

class UsuarioController:
    """Controlador encargado de la gestión de usuarios."""
    
    def __init__(self, archivo_usuarios: str = 'data/usuarios.json'):
        self.archivo_usuarios = archivo_usuarios
        self.usuarios: Dict[str, Usuario] = {}
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga los usuarios desde el archivo JSON."""
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

    def guardar_usuarios(self):
        """Guarda los usuarios en el archivo JSON."""
        try:
            usuarios_list = [u.to_dict() for u in self.usuarios.values()]
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar usuarios: {e}")

    def _crear_usuarios_ejemplo(self):
        """Crea usuario admin por defecto."""
        if "admin" not in self.usuarios:
            admin = Usuario("admin", "admin123", "admin")
            self.usuarios[admin.username] = admin
            self.guardar_usuarios()
            print("✓ Usuario admin creado (user: admin, pass: admin123)")

    def registrar_usuario(self, username, password, role='comprador') -> bool:
        """Registra un nuevo usuario."""
        # Validaciones
        if ' ' in username:
            raise ValueError("El nombre de usuario no puede contener espacios.")
        
        if not username.replace('-', '').isalnum():
             raise ValueError("El usuario solo puede contener letras, números y guiones.")

        if set(username) == {'-'}:
             raise ValueError("El usuario no puede ser solo guiones.")

        if username in self.usuarios:
            return False
        
        nuevo_usuario = Usuario(username, password, role)
        self.usuarios[username] = nuevo_usuario
        self.guardar_usuarios()
        return True

    def autenticar_usuario(self, username, password) -> Optional[Usuario]:
        """Verifica credenciales y retorna el usuario si es válido."""
        usuario = self.usuarios.get(username)
        if usuario and usuario.password == password:
            return usuario
        return None
