"""Controlador para la gestión de usuarios.

Este controlador maneja:
- Carga y guardado de usuarios desde/hacia JSON
- Autenticación (login) con RUT y contraseña
- Registro de nuevos usuarios con validación de RUT y nombre
- Limpieza de datos de usuarios
"""

import os
import re  # Para validar formato de RUT y nombre con expresiones regulares
import json
from typing import Dict, Optional
from models.usuario import Usuario

class UsuarioController:
    """
    Controlador encargado de la gestión de usuarios (autenticación y registro).
    """
    
    def __init__(self, archivo_usuarios: str = 'data/usuarios.json'):
        # Ruta donde se guarda el archivo JSON de usuarios
        self.archivo_usuarios = archivo_usuarios
        # Diccionario en memoria con los usuarios cargados (clave: RUT, valor: objeto Usuario)
        self.usuarios: Dict[str, Usuario] = {}
        # Cargar usuarios del archivo JSON al iniciar
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga la base de datos de usuarios desde el archivo JSON."""
        if os.path.exists(self.archivo_usuarios):
            try:
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                    usuarios_data = json.load(f)
                # Ahora usamos `rut` como clave única del diccionario; mantener compatibilidad con datos antiguos que usaban 'username'
                self.usuarios = { (u.get('rut') or u.get('username')): Usuario.from_dict(u) for u in usuarios_data }
                print(f"Usuarios cargados: {len(self.usuarios)}")
            except Exception as e:
                print(f"Error al cargar usuarios: {e}")
                # Si hay error, crear usuario admin por defecto
                self._crear_usuarios_ejemplo()
        else:
            print("No se encontró archivo de usuarios. Creando usuario admin.")
            # Si el archivo no existe, crear el admin por defecto
            self._crear_usuarios_ejemplo()

    def guardar_usuarios(self):
        """Persiste los usuarios en memoria al archivo JSON."""
        try:
            # Convertir cada usuario a diccionario
            usuarios_list = [u.to_dict() for u in self.usuarios.values()]
            # Asegurar que el directorio exista antes de escribir (crear si no existe)
            dirpath = os.path.dirname(self.archivo_usuarios)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # Guardar como JSON formateado (indent=2 para que sea legible)
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")

    def _crear_usuarios_ejemplo(self):
        """Genera un usuario administrador por defecto si no existe."""
        # Crear admin por defecto con RUT válido (8 dígitos + '-' + dígito verificador)
        default_rut = '00000000-0'
        if default_rut not in self.usuarios:
            # Crear usuario admin con credenciales por defecto
            admin = Usuario(default_rut, "admin123", "Administrador", "admin")
            self.usuarios[admin.rut] = admin
            # Guardar el admin creado en el archivo JSON
            self.guardar_usuarios()
            print(f"Usuario admin creado (rut: {default_rut}, pass: admin123)")

    def limpiar_usuarios(self, keep_admin: bool = True) -> bool:
        """Limpia el archivo de usuarios (elimina todos los registros).
        
        Si keep_admin es True, recrea el usuario administrador por defecto después de limpiar.
        """
        try:
            # Vaciar el diccionario de usuarios
            self.usuarios.clear()
            # Preparar lista vacía para guardar en JSON
            usuarios_list = []
            # Asegurar que el directorio exista
            dirpath = os.path.dirname(self.archivo_usuarios)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            # Guardar lista vacía en el archivo
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios_list, f, indent=2, ensure_ascii=False)

            # Si se solicita, recrear el admin por defecto
            if keep_admin:
                self._crear_usuarios_ejemplo()

            print("Archivo de usuarios limpiado")
            return True
        except Exception as e:
            print(f"Error al limpiar usuarios: {e}")
            return False

    def registrar_usuario(self, rut: str, password: str, nombre: str = '', role: str = 'comprador') -> bool:
        """
        Crea un nuevo usuario identificado por `rut`.
        
        Valida:
        - RUT: formato 7-8 dígitos + guion + dígito verificador (ej: 12345678-9)
        - Nombre: obligatorio, solo letras (incluyendo acentos) y espacios
        - Que el RUT no esté ya registrado
        
        Retorna True si se registró exitosamente, False si el RUT ya existe.
        Lanza ValueError si hay problemas con la validación.
        """
        # Normalizar RUT: quitar espacios en blanco al inicio y final
        rut = (rut or '').strip()

        # Validar formato del RUT usando expresión regular
        # Debe tener: 7 u 8 dígitos, un guion, y un dígito verificador (0-9 o K mayúscula/minúscula)
        rut_pattern = re.compile(r'^\d{7,8}-[0-9Kk]$')
        if not rut_pattern.match(rut):
            raise ValueError('El RUT debe tener 7 u 8 dígitos, un guion y un dígito verificador (ej: 12345678-9). No use puntos.')

        # Verificar que el RUT no esté ya registrado
        if rut in self.usuarios:
            return False

        # Validar nombre: obligatorio, no puede ser solo espacios
        nombre = (nombre or '').strip()
        if not nombre:
            raise ValueError('El nombre es obligatorio y no puede estar vacío')

        # Validar que el nombre solo contiene letras latinas (mayúsculas/minúsculas), acentos y espacios
        # Rango À-ÿ incluye: á, é, í, ó, ú, ñ, Á, É, Í, Ó, Ú, Ñ y otros caracteres latinos con tilde
        pattern = re.compile(r"^[A-Za-zÀ-ÿÑñ ]+$")
        if not pattern.match(nombre):
            raise ValueError('El nombre solo puede contener letras y espacios')

        # Crear nuevo usuario con los datos validados
        nuevo_usuario = Usuario(rut, password, nombre, role)
        # Guardar en el diccionario usando RUT como clave única
        self.usuarios[rut] = nuevo_usuario
        # Persistir cambios al archivo JSON
        self.guardar_usuarios()
        return True

    def autenticar_usuario(self, rut: str, password: str) -> Optional[Usuario]:
        """
        Valida las credenciales de login usando RUT y contraseña.
        
        Retorna el objeto Usuario si es correcto, None si las credenciales son inválidas.
        """
        # Buscar el usuario por su RUT
        usuario = self.usuarios.get(rut)
        # Verificar que exista y que la contraseña coincida
        if usuario and usuario.password == password:
            return usuario
        return None
