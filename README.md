# 🛒 Sistema de Administración de Supermercado

Sistema completo de gestión para supermercados desarrollado en Python. Permite administrar inventario, realizar ventas, generar reportes y recibir alertas de stock bajo.

## 📋 Características Principales

### ✅ Gestión de Inventario
- **Ver inventario completo** organizado por categorías
- **Agregar nuevos productos** con toda su información
- **Actualizar stock** (agregar o reducir cantidades)
- **🗑️ Eliminar productos** del inventario
- **♻️ Reiniciar productos** a valores por defecto (sin afectar ventas/usuarios)
- **Buscar productos** por código, nombre o categoría
- **Alertas automáticas** cuando el stock llega a niveles críticos (≤5 unidades/kilos)

### 💰 Sistema de Ventas
- **Visualización de productos disponibles** antes de vender
- **Validación de stock** en tiempo real
- **Carrito de compras** interactivo
- **Resumen de venta** antes de confirmar
- **Actualización automática** del inventario tras cada venta
- **Registro histórico** de todas las ventas realizadas
- **Generación de Boleta** con ID único de venta

### 📊 Reportes y Estadísticas
- Total de productos en catálogo
- Valor total del inventario
- Número de ventas realizadas
- Ingresos totales generados
- Productos con stock bajo
- Productos sin stock
- Historial de últimas ventas

### 🔔 Sistema de Alertas
- **Notificaciones de stock bajo** cuando productos llegan a 5 unidades/kilos
- **Alertas de productos sin stock**
- **Panel dedicado** para visualizar todas las alertas activas

### 🔄 Navegación Intuitiva
- **Menús interactivos** con navegación fácil
- **Opción de volver** a la pantalla anterior en cada menú
- **Pantalla limpia** automática para mejor visualización
- **Confirmaciones** antes de operaciones críticas

## 🚀 Instalación y Uso

### Requisitos
- Python 3.7 o superior
- Librería `tkinter` (incluida en la instalación estándar de Python)

### Ejecución
**Interfaz Gráfica (Recomendada):**
```bash
python main.py
```

El sistema cargará automáticamente los 3 archivos JSON (productos, ventas, usuarios) desde la carpeta `data/` o los creará con datos de ejemplo si no existen.

## 🖥️ Interfaz Gráfica (Tkinter)

El proyecto incluye una interfaz gráfica moderna y fácil de usar:
- **Pestañas de Navegación**: Inventario, Ventas, Reportes, Alertas.
- **Tablas Interactivas**: Visualización clara de datos.
- **Formularios**: Ventanas emergentes para agregar productos y stock.
- **Búsqueda en Tiempo Real**: Filtra productos mientras escribes.
- **Gestión de Administradores**: Funcionalidad exclusiva para crear nuevos administradores.

## ☁️ Subir a GitHub

El proyecto está listo para control de versiones. Sigue estos pasos para subirlo:

1. **Inicializar repositorio:**
   ```bash
   git init
   git add .
   git commit -m "Primer commit"
   ```

2. **Crear repositorio en GitHub:**
   - Ve a github.com y crea un nuevo repositorio.

3. **Subir archivos:**
   ```bash
   git branch -M main
   git remote add origin <URL_DE_TU_REPOSITORIO>
   git push -u origin main
   ```

## 🔐 Inicio de Sesión

El sistema cuenta con control de acceso por roles:

### Credenciales de Administrador (Por defecto)
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### Roles de Usuario
1. **Administrador:** Acceso total (Inventario, Ventas, Reportes, Alertas, Crear Admins).
2. **Comprador:** Acceso limitado (Catálogo de productos y Compras).

### Registro de Nuevos Usuarios
- Desde la pantalla de inicio de sesión, puedes crear nuevas cuentas de **Comprador**.
- Las cuentas de **Administrador** pueden crearse desde el panel de administración (requiere estar logueado como admin).

## 📖 Manual de Uso

### Menú Principal
Al iniciar el sistema, verás 5 opciones principales:

1. **Gestión de Inventario**: Administra productos y stock
2. **Realizar Venta**: Procesa ventas de productos
3. **Ver Reportes y Estadísticas**: Consulta métricas del negocio
4. **Alertas de Stock**: Revisa productos con stock bajo
5. **Buscar Producto**: Búsqueda rápida de productos
0. **Salir**: Guarda y cierra el sistema

### Gestión de Inventario

#### Ver Todos los Productos
- Muestra el inventario completo organizado por categorías
- Indica el stock actual y precio de cada producto
- **⚠️ Marca productos con stock bajo** automáticamente

#### Agregar Nuevo Producto
Información requerida:
- Código único del producto
- Nombre
- Precio
- Stock inicial
- Categoría
- Unidad de medida (unidades o kilos)
- Stock mínimo para alerta (por defecto: 5)

#### Actualizar Stock
- Selecciona el producto por código
- Elige si agregar o reducir stock
- El sistema valida que no se reduzca más stock del disponible
- **Alerta automática** si el stock queda bajo

#### Ver Productos con Stock Bajo
- Lista todos los productos que están por debajo del stock mínimo
- Útil para planificar reabastecimiento

### Sistema de Ventas

#### Realizar una Venta
1. El sistema muestra **solo productos con stock disponible**
2. Ingresa el código del producto
3. Especifica la cantidad a vender
4. El sistema valida que haya suficiente stock
5. Puedes agregar múltiples productos
6. Escribe `fin` cuando termines
7. Revisa el **resumen de la venta**
8. Confirma la operación
9. El inventario se actualiza automáticamente

**Validaciones automáticas:**
- No se pueden vender productos sin stock
- No se puede vender más cantidad de la disponible
- Alertas de stock bajo después de la venta

### Reportes y Estadísticas

Visualiza métricas importantes:
- 📊 Total de productos
- 💰 Valor del inventario
- 🛒 Ventas realizadas
- 💵 Ingresos totales
- ⚠️ Productos críticos
- 📅 Historial de últimas 5 ventas

### Alertas de Stock

Panel centralizado que muestra:
- **Productos sin stock** (requieren reabastecimiento urgente)
- **Productos con stock bajo** (próximos a agotarse)

## 💾 Almacenamiento de Datos

El sistema utiliza **3 archivos JSON separados** en la carpeta `data/` para mejor organización:
- **`data/productos.json`**: Inventario de productos
- **`data/ventas.json`**: Historial de ventas
- **`data/usuarios.json`**: Cuentas de usuarios

Esta separación permite:
- 🔄 **Reiniciar productos** sin afectar ventas ni usuarios
- 🗑️ **Eliminar productos** de forma independiente
- 📊 **Respaldos selectivos** por tipo de datos
- ⚡ **Mejor rendimiento** al cargar datos específicos

Los datos se guardan automáticamente después de cada operación y persisten entre sesiones.
**Primera ejecución**: Se crean productos de ejemplo automáticamente.

## 🎯 Características Destacadas

### ✅ Validaciones Implementadas
- Stock disponible antes de vender
- Códigos únicos de productos
- Valores numéricos válidos
- Cantidades positivas

### 🔔 Sistema de Alertas Inteligente
- **Automático**: No requiere configuración manual
- **Personalizable**: Stock mínimo configurable por producto
- **Visible**: Alertas en múltiples pantallas
- **Proactivo**: Previene quiebres de stock

### 📦 Soporte Múltiples Unidades
- **Unidades**: Para productos contables (botellas, paquetes, etc.)
- **Kilos**: Para productos a granel (frutas, carnes, etc.)

### 🎨 Interfaz Amigable
- Emojis para mejor visualización
- Organización por categorías
- Mensajes claros y descriptivos
- Navegación intuitiva

## 📝 Estructura de Datos

### Producto
```python
{
    "codigo": "001",
    "nombre": "Arroz",
    "precio": 2.50,
    "stock": 50,
    "categoria": "Abarrotes",
    "unidad": "kilos",
    "stock_minimo": 10
}
```

### Venta
```python
{
    "id": 1,
    "fecha": "2025-11-24 10:30:00",
    "items": [
        {
            "codigo": "001",
            "nombre": "Arroz",
            "cantidad": 2,
            "precio_unitario": 2.50,
            "subtotal": 5.00,
            "unidad": "kilos"
        }
    ],
    "total": 5.00
}
```

## 🔧 Personalización

### Cambiar Stock Mínimo por Defecto
Modifica el parámetro `stock_minimo` al crear productos:
```python
Producto("código", "nombre", precio, stock, "categoría", "unidad", stock_minimo=10)
```

### Agregar Nuevas Categorías
Las categorías se crean automáticamente al agregar productos.

### Modificar Productos de Ejemplo
Edita el método `_crear_productos_ejemplo()` en la clase `ProductoController`.

## 🐛 Solución de Problemas

**Error al cargar datos:**
- Verifica que los archivos en `data/` no estén corruptos
- Elimina los archivos para reiniciar con datos frescos

**Productos duplicados:**
- Cada producto debe tener un código único
- El sistema previene duplicados automáticamente

**Stock negativo:**
- El sistema valida que no se pueda reducir más stock del disponible

## 📈 Mejoras Futuras Sugeridas

- [ ] Exportación de reportes a PDF/Excel
- [ ] Gráficos de ventas e inventario
- [ ] Sistema de proveedores
- [ ] Órdenes de compra automáticas
- [ ] Códigos de barras
- [ ] Descuentos y promociones
- [ ] Control de vencimientos
- [ ] Base de datos SQL

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

## 👨‍💻 Autor

Sistema desarrollado para administración de supermercados.

---

**Versión:** 2.0  
**Fecha:** Noviembre 2025  
**Python:** 3.14
