# Sistema de Administración de Supermercado - POO

Sistema completo de administración de supermercado desarrollado con Python y Tkinter, siguiendo los principios de **Programación Orientada a Objetos (POO)** y arquitectura **Modelo-Vista-Controlador (MVC)**.

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado siguiendo los principios de POO y el patrón MVC:

```
proyecto_poo_v2-main/
│
├── models/                      # Capa de Modelo (Datos)
│   ├── __init__.py
│   ├── producto.py             # Clase Producto
│   ├── usuario.py              # Clase Usuario
│   └── venta.py                # Clase Venta
│
├── controllers/                 # Capa de Controlador (Lógica de negocio)
│   └── supermercado_controller.py  # Controlador principal
│
├── views/                       # Capa de Vista (Interfaz gráfica)
│   └── gui.py                  # Interfaz Tkinter (LoginWindow, SupermercadoGUI, RegistroWindow)
│
├── main.py                      # Punto de entrada de la aplicación
├── supermercado_data.json      # Base de datos (JSON)
└── README.md                    # Documentación principal
```

## 📦 Características Principales

### Sistema de Autenticación
- **Login**: Inicio de sesión con usuario y contraseña
- **Registro**: Creación de nuevos usuarios compradores
- **Roles**: Administrador y Comprador con permisos diferenciados
- **✨ Todo en una ventana**: Sin ventanas emergentes (Toplevel)

### Para Administradores
- ✅ **Gestión de Inventario**
  - Agregar nuevos productos (formulario integrado)
  - Actualizar stock (formulario integrado)
  - Búsqueda de productos en tiempo real
  - Vista completa del catálogo
  
- 💰 **Gestión de Ventas**
  - Procesar ventas
  - Carrito de compras
  - Validación de stock

- 📊 **Reportes y Estadísticas**
  - Total de productos
  - Valor del inventario
  - Ingresos totales
  - Historial de ventas

- ⚠️ **Alertas de Stock**
  - Productos con stock bajo
  - Productos agotados

### Para Compradores
- 🛒 **Sistema de Compras**
  - Ver catálogo de productos
  - Agregar productos al carrito
  - Finalizar compras
  - Búsqueda de productos

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.7 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución
```bash
cd proyecto_poo_v2-main
python main.py
```

## 👤 Credenciales por Defecto

### Administrador
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Crear Comprador
Usa el botón "Crear cuenta de Comprador" en la pantalla de login.

## 🎯 Principios de POO Implementados

### 1. **Encapsulación**
- Cada clase tiene responsabilidades bien definidas
- Los atributos y métodos están organizados lógicamente
- Los datos se manipulan a través de métodos controlados

**Ejemplo:**
```python
class Producto:
    def __init__(self, codigo, nombre, precio, stock, categoria, unidad, stock_minimo):
        self.codigo = codigo
        self.nombre = nombre
        # ... otros atributos encapsulados
    
    def tiene_stock_bajo(self):
        return self.stock <= self.stock_minimo
```

### 2. **Abstracción**
- Separación clara entre la lógica de negocio (controllers) y la presentación (views)
- Interfaces claras entre componentes
- Modelos de datos independientes

**Ejemplo:**
```
Usuario → LoginWindow → SupermercadoController → Producto
(Vista)      (Vista)        (Controlador)         (Modelo)
```

### 3. **Separación de Responsabilidades (SRP)**
- **Models**: Solo representan datos y su conversión
- **Controllers**: Solo manejan la lógica de negocio
- **Views**: Solo manejan la presentación e interacción

### 4. **Bajo Acoplamiento y Alta Cohesión**
- Cada módulo es independiente
- Los cambios en un módulo no afectan a otros
- Cada clase tiene métodos relacionados con su propósito

## 📱 Características de la Interfaz

- ✨ **Ventana única**: Toda la navegación ocurre en la misma ventana
- 🎨 **Diseño moderno**: Usa el tema 'clam' de ttk
- 📱 **Responsiva**: Se adapta al tamaño de la ventana
- 🔄 **Actualización en tiempo real**: Los datos se actualizan automáticamente
- ⌨️ **Búsqueda en tiempo real**: Filtrado instantáneo de productos
- ✅ **Validaciones**: Validación de datos en todos los formularios
- 📋 **Formularios integrados**: No hay ventanas emergentes (Toplevel)

## 💾 Persistencia de Datos

Los datos se almacenan en formato JSON (`supermercado_data.json`):
- Productos
- Ventas
- Usuarios

## 🔧 Funcionalidades Técnicas

### Validaciones Implementadas
- ✅ Validación de tipos de datos (enteros/decimales según unidad)
- ✅ Validación de stock disponible
- ✅ Validación de credenciales
- ✅ Validación de campos obligatorios
- ✅ Corrección automática de datos corruptos

### Características Avanzadas
- 🔄 Recarga de datos desde archivo
- 💾 Guardado automático después de cada operación
- ⚠️ Alertas de stock bajo
- 📊 Estadísticas en tiempo real
- 🛒 Carrito de compras funcional
- 🎯 Navegación fluida sin ventanas emergentes

## 📝 Estructura de Clases

### Models (Modelos)
```python
# models/producto.py
class Producto:
    - to_dict()          # Conversión a diccionario
    - from_dict()        # Creación desde diccionario
    - tiene_stock_bajo() # Validación de stock

# models/usuario.py
class Usuario:
    - to_dict()          # Conversión a diccionario
    - from_dict()        # Creación desde diccionario

# models/venta.py
class Venta:
    - agregar_item()     # Agregar producto a la venta
    - to_dict()          # Conversión a diccionario
```

### Controllers (Controladores)
```python
# controllers/supermercado_controller.py
class SupermercadoController:
    - cargar_datos()               # Cargar desde JSON
    - guardar_datos()              # Guardar en JSON
    - agregar_producto()           # Agregar producto
    - actualizar_stock()           # Actualizar stock
    - buscar_producto()            # Buscar productos
    - realizar_venta()             # Procesar venta
    - obtener_estadisticas()       # Calcular estadísticas
    - autenticar_usuario()         # Validar credenciales
    - registrar_usuario()          # Crear nuevo usuario
```

### Views (Vistas)
```python
# views/gui.py
class LoginWindow:
    - login()                      # Procesar login
    - mostrar_registro()           # Mostrar registro

class RegistroWindow:
    - registrar()                  # Registrar usuario
    - volver()                     # Volver al login

class SupermercadoGUI:
    # Inventario
    - init_inventario_admin()      # Vista admin
    - init_inventario_comprador()  # Vista comprador
    - mostrar_dialogo_producto()   # Formulario producto
    - mostrar_dialogo_stock()      # Formulario stock
    
    # Ventas
    - init_ventas()                # Inicializar ventas
    - agregar_al_carrito()         # Agregar al carrito
    - finalizar_venta()            # Procesar venta
    
    # Reportes y Alertas
    - init_reportes()              # Inicializar reportes
    - init_alertas()               # Inicializar alertas
```

## 🎓 Conceptos de POO Aplicados

### 1. **Separación de Responsabilidades (SRP)**
Cada clase tiene una única responsabilidad:
- `Producto`: Representar un producto
- `SupermercadoController`: Gestionar la lógica de negocio
- `SupermercadoGUI`: Presentar la interfaz

### 2. **Bajo Acoplamiento**
Los componentes son independientes:
- Los modelos no conocen los controladores
- Las vistas se comunican con controladores, no con modelos directamente
- El controlador puede cambiar sin afectar la vista

### 3. **Alta Cohesión**
Los métodos de cada clase están relacionados:
- Todos los métodos de `Producto` están relacionados con productos
- Todos los métodos de `SupermercadoController` están relacionados con la gestión del supermercado

### 4. **Código Reutilizable**
- Las clases pueden usarse en diferentes contextos
- Los métodos son genéricos y parametrizables

### 5. **Mantenibilidad**
- Estructura clara que facilita encontrar y modificar código
- Cambios en un módulo no afectan a otros
- Fácil agregar nuevas funcionalidades

## 🔄 Flujo de Datos

```
Usuario → Vista → Controlador → Modelo → Persistencia
                                            ↓
                                        JSON File
```

**Ejemplo de flujo para agregar un producto:**
1. Usuario llena formulario en `SupermercadoGUI`
2. Se llama a `controller.agregar_producto(producto)`
3. El controlador valida y agrega el producto a `self.productos`
4. El controlador llama a `guardar_datos()` para persistir
5. La vista se actualiza automáticamente

## 🆕 Mejoras Implementadas vs Versión Anterior

### ✅ Arquitectura MVC
- **Antes**: Todo en un solo archivo o archivos mal organizados
- **Ahora**: Separación clara en models, views, controllers

### ✅ Sin Ventanas Emergentes
- **Antes**: Uso de `Toplevel` para diálogos
- **Ahora**: Formularios integrados en la misma ventana

### ✅ Mejor Organización
- **Antes**: Clases mezcladas
- **Ahora**: Cada clase en su propio archivo

### ✅ Navegación Fluida
- **Antes**: Múltiples ventanas confusas
- **Ahora**: Todo en una sola ventana con navegación clara

## 📊 Ventajas de esta Arquitectura

1. **Escalabilidad**: Fácil agregar nuevas funcionalidades
2. **Mantenibilidad**: Fácil encontrar y corregir bugs
3. **Testabilidad**: Cada componente puede testearse independientemente
4. **Legibilidad**: Código claro y bien organizado
5. **Reutilización**: Componentes pueden usarse en otros proyectos

## 📄 Licencia

Proyecto educativo para el aprendizaje de Programación Orientada a Objetos.

---

**Versión:** 2.0 (Refactorizada con POO)  
**Fecha:** Noviembre 2025  
**Python:** 3.7+
