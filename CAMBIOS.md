# 📝 Registro de Cambios

## Versión 2.0 - Refactorización JSON y Nuevas Funcionalidades

### 🔄 Cambios Estructurales

#### Separación de Archivos JSON
Antes el sistema usaba un único archivo `supermercado_data.json`. Ahora utiliza **3 archivos separados**:

1. **`productos.json`** - Inventario de productos
   ```json
   [
     {
       "codigo": "001",
       "nombre": "Arroz",
       "precio": 1500,
       "stock": 50,
       "categoria": "Abarrotes",
       "unidad": "kilos",
       "stock_minimo": 10
     }
   ]
   ```

2. **`ventas.json`** - Historial de transacciones
   ```json
   [
     {
       "fecha": "2025-01-20 14:30:00",
       "items": [...],
       "total": 15000
     }
   ]
   ```

3. **`usuarios.json`** - Cuentas de acceso
   ```json
   [
     {
       "username": "admin",
       "password": "admin123",
       "role": "admin"
     }
   ]
   ```

#### Beneficios de la Separación
- ✅ **Operaciones independientes**: Puedes resetear productos sin perder ventas o usuarios
- ✅ **Respaldos selectivos**: Respalda solo lo que necesitas
- ✅ **Mejor rendimiento**: Carga solo los datos necesarios
- ✅ **Mantenimiento más fácil**: Código más limpio y organizado

---

### 🆕 Nuevas Funcionalidades

#### 1. 🗑️ Eliminar Producto
**Ubicación**: Pestaña "📦 Inventario" (Solo administradores)

**Cómo usar**:
1. Selecciona un producto de la tabla
2. Haz clic en el botón **"🗑️ Eliminar Producto"**
3. Confirma la eliminación en el diálogo
4. El producto se elimina permanentemente de `productos.json`

**Características**:
- ⚠️ Requiere confirmación para evitar eliminaciones accidentales
- 💾 Guarda automáticamente después de eliminar
- 🔄 Actualiza la vista del inventario inmediatamente
- 📊 No afecta el historial de ventas ni usuarios

**Código relevante**:
```python
def eliminar_producto(self, codigo: str) -> bool:
    """Elimina un producto del inventario"""
    if codigo not in self.productos:
        return False
    
    producto = self.productos[codigo]
    del self.productos[codigo]
    self.guardar_productos()  # Solo guarda productos.json
    return True
```

#### 2. ♻️ Reiniciar Productos
**Ubicación**: Pestaña "📦 Inventario" (Solo administradores)

**Cómo usar**:
1. Haz clic en el botón **"♻️ Reiniciar Productos"**
2. Lee el mensaje de confirmación con atención
3. Confirma para restaurar productos a valores por defecto
4. Los productos originales son reemplazados por 5 productos de ejemplo

**Características**:
- ⚠️ Elimina TODOS los productos actuales
- 🔄 Restaura los 5 productos de ejemplo predeterminados
- 🛡️ **NO afecta ventas ni usuarios** (datos protegidos)
- 💾 Los cambios son permanentes
- ⏰ Útil para demos, pruebas o reiniciar el sistema

**Productos de Ejemplo Creados**:
1. Arroz - $1,500 (50 kilos)
2. Leche - $1,200 (30 unidades)
3. Pan - $800 (100 unidades)
4. Manzanas - $2,500 (4 kilos)
5. Pollo - $5,000 (15 kilos)

**Código relevante**:
```python
def reiniciar_productos(self) -> bool:
    """Reinicia los productos a los valores por defecto"""
    self.productos.clear()
    self._crear_productos_ejemplo()
    self.guardar_productos()  # Solo guarda productos.json
    return True
```

---

### 🔧 Cambios Técnicos en el Código

#### Clase SupermercadoController

**Antes** (1 archivo):
```python
def __init__(self, archivo_datos="supermercado_data.json"):
    self.archivo_datos = archivo_datos
    self.productos = {}
    self.ventas = []
    self.usuarios = {}
    self.cargar_datos()
```

**Ahora** (3 archivos):
```python
def __init__(self, archivo_productos="productos.json", 
             archivo_ventas="ventas.json", 
             archivo_usuarios="usuarios.json"):
    self.archivo_productos = archivo_productos
    self.archivo_ventas = archivo_ventas
    self.archivo_usuarios = archivo_usuarios
    self.productos = {}
    self.ventas = []
    self.usuarios = {}
    self.cargar_datos()
```

#### Nuevos Métodos de Guardado

**`guardar_productos()`** - Guarda solo productos
```python
def guardar_productos(self):
    productos_list = [p.to_dict() for p in self.productos.values()]
    with open(self.archivo_productos, 'w', encoding='utf-8') as f:
        json.dump(productos_list, f, indent=2, ensure_ascii=False)
```

**`guardar_ventas()`** - Guarda solo ventas
```python
def guardar_ventas(self):
    with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
        json.dump(self.ventas, f, indent=2, ensure_ascii=False)
```

**`guardar_usuarios()`** - Guarda solo usuarios
```python
def guardar_usuarios(self):
    usuarios_list = [u.to_dict() for u in self.usuarios.values()]
    with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
        json.dump(usuarios_list, f, indent=2, ensure_ascii=False)
```

**`guardar_datos()`** - Guarda todo
```python
def guardar_datos(self):
    self.guardar_productos()
    self.guardar_ventas()
    self.guardar_usuarios()
```

#### Método de Carga Actualizado

```python
def cargar_datos(self):
    # Cargar productos
    if os.path.exists(self.archivo_productos):
        with open(self.archivo_productos, 'r', encoding='utf-8') as f:
            productos_data = json.load(f)
        self.productos = {p['codigo']: Producto.from_dict(p) for p in productos_data}
    
    # Cargar ventas
    if os.path.exists(self.archivo_ventas):
        with open(self.archivo_ventas, 'r', encoding='utf-8') as f:
            self.ventas = json.load(f)
    
    # Cargar usuarios
    if os.path.exists(self.archivo_usuarios):
        with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
            usuarios_data = json.load(f)
        self.usuarios = {u['username']: Usuario.from_dict(u) for u in usuarios_data}
```

---

### 📊 Comparación de Arquitectura

| Aspecto | Antes (v1.0) | Ahora (v2.0) |
|---------|--------------|--------------|
| **Archivos JSON** | 1 (`supermercado_data.json`) | 3 (productos, ventas, usuarios) |
| **Estructura** | Anidada por categorías | Lista plana por tipo |
| **Guardado** | Todo junto | Selectivo por tipo |
| **Reiniciar** | ❌ No disponible | ✅ Solo productos |
| **Eliminar** | ✅ Individual | ✅ Individual + mejorado |
| **Respaldos** | Todo o nada | Por tipo de dato |
| **Rendimiento** | Carga todo siempre | Carga según necesidad |

---

### 🎯 Casos de Uso

#### Escenario 1: Resetear para Demo
```
Situación: Necesitas mostrar el sistema a un cliente con datos limpios
Solución: 
1. Haz clic en "♻️ Reiniciar Productos"
2. Los productos vuelven a los 5 de ejemplo
3. Las ventas históricas se mantienen intactas
4. Los usuarios no se ven afectados
```

#### Escenario 2: Eliminar Producto Descontinuado
```
Situación: Ya no vendes un producto y quieres limpiarlo del sistema
Solución:
1. Busca el producto en el inventario
2. Selecciónalo
3. Haz clic en "🗑️ Eliminar Producto"
4. Confirma la eliminación
5. El producto desaparece de productos.json
```

#### Escenario 3: Respaldo Selectivo
```
Situación: Quieres respaldar solo las ventas sin tocar productos
Solución:
1. Copia el archivo ventas.json a un lugar seguro
2. Si algo sale mal, restaura solo ese archivo
3. Los productos y usuarios no se ven afectados
```

---

### 🔒 Consideraciones de Seguridad

#### Confirmaciones Implementadas
- ❗ **Eliminar Producto**: Diálogo de confirmación con nombre del producto
- ❗ **Reiniciar Productos**: Advertencia clara de que la acción es irreversible
- ❗ Ambas operaciones requieren aceptación explícita del usuario

#### Protección de Datos
- ✅ Las **ventas** nunca se eliminan con reiniciar productos
- ✅ Los **usuarios** permanecen intactos en todas las operaciones
- ✅ Cada operación guarda solo los archivos afectados
- ✅ Los archivos JSON tienen codificación UTF-8 para caracteres especiales

---

### 🚀 Migración desde v1.0

Si tienes un `supermercado_data.json` de la versión anterior:

1. **Automático**: El sistema detecta si no existen los 3 archivos nuevos y crea datos de ejemplo
2. **Manual**: Puedes separar tu archivo antiguo en 3:
   - Extrae el array `productos` → `productos.json`
   - Extrae el array `ventas` → `ventas.json`
   - Extrae el array `usuarios` → `usuarios.json`

El sistema ya no usa `supermercado_data.json`, puedes eliminarlo o guardarlo como respaldo.

---

### 📚 Documentación Adicional

Para más información sobre:
- **Instalación**: Ver `README.md`
- **Uso básico**: Ver `GUIA_RAPIDA.md`
- **Estructura de clases**: Ver comentarios en código fuente

---

### 🐛 Problemas Conocidos Resueltos

- ✅ **Problema**: Reiniciar productos afectaba ventas y usuarios
  - **Solución**: Archivos separados + métodos de guardado selectivo

- ✅ **Problema**: Eliminar productos era riesgoso sin confirmación
  - **Solución**: Diálogos de confirmación con información clara

- ✅ **Problema**: Respaldos eran todo o nada
  - **Solución**: 3 archivos independientes para respaldos selectivos

---

### 📅 Historial de Versiones

- **v2.0** (Enero 2025) - Separación de JSON + Eliminar/Reiniciar
- **v1.1** (Diciembre 2024) - Sistema de usuarios y roles
- **v1.0** (Noviembre 2024) - Versión inicial

---

### 👨‍💻 Contribuciones

Este cambio mejora significativamente la arquitectura del sistema y facilita futuras expansiones.

**Siguiente mejora sugerida**: Implementar sistema de respaldos automáticos diarios.
