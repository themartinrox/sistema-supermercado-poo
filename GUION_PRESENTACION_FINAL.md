# Guion de Presentación: Sistema de Gestión de Minimarket

**Duración Estimada:** 10-15 Minutos
**Presentador:** Martin Rodriguez

---

## 1. Inicio y Título
**(Diapositiva 1: Título)**

"Buenos días profesor y compañeros. Soy Martin Rodriguez y hoy presentaré el detalle técnico y funcional de la actualización de nuestro 'Sistema de Gestión de Minimarket'. Esta presentación se centrará exclusivamente en la arquitectura, los algoritmos clave y el desglose detallado de las funcionalidades implementadas."

---

## 2. Arquitectura del Sistema
**(Diapositiva 2: Diagrama de Clases)**

"Comenzamos con la arquitectura. Como pueden ver en este Diagrama de Clases, el sistema sigue estrictamente el patrón **Modelo-Vista-Controlador (MVC)**.

*   **Modelos:** Tenemos clases como `Producto`, `Venta` y `Usuario`. Destaco que `Producto` utiliza composición para integrar objetos de `Categoria` y `Unidad`.
*   **Controladores:** La lógica está segregada. `ProductoController` maneja el inventario, `VentaController` las transacciones y `UsuarioController` la seguridad. Todo orquestado por un `SupermercadoController` que actúa como fachada.
*   **Vista:** La clase `SupermercadoGUI` maneja toda la interfaz gráfica con Tkinter."

---

## 3. Implementación y Algoritmos
**(Diapositiva 3: Modelo Producto)**

"Pasando al código, aquí vemos la clase `Producto`. Hemos actualizado el constructor para soportar **multimedia y unidades de medida**.
*   El atributo `imagen_path` almacena la ruta local de la imagen.
*   El atributo `unidad` define si el producto se maneja por Kilos o Unidades.
*   También vemos el método `tiene_stock_bajo`, que encapsula la lógica de negocio para las alertas."

**(Diapositiva 4: Vista - Carga de Imágenes)**

"Para la gestión visual, implementamos este algoritmo en la Vista utilizando la librería **Pillow**.
*   El método `mostrar_detalle_producto` verifica si la ruta de la imagen es válida.
*   Si existe, abre la imagen, la redimensiona usando un filtro de alta calidad (LANCZOS) para que no se deforme, y la convierte a un formato compatible con Tkinter.
*   Es crucial mantener la referencia de la imagen (`lbl_img.image = photo`) para evitar que el recolector de basura de Python la elimine de la memoria."

**(Diapositiva 5: Controlador - Actualización de Stock)**

"En el controlador, el método `actualizar_stock` demuestra polimorfismo de datos.
*   Maneja tanto números enteros (para unidades) como flotantes (para kilogramos) de forma transparente.
*   Valida que haya stock suficiente antes de restar.
*   Y lo más importante: verifica automáticamente si se debe disparar una alerta de stock bajo después de cada operación, garantizando la integridad del inventario en tiempo real."

---

## 4. Funcionalidades Detalladas
**(Diapositiva 6: Acceso y Autenticación)**

"Ahora revisemos las funcionalidades pantalla por pantalla.
*   **Login:** Es la puerta de entrada. Valida las credenciales y, dependiendo del rol (Admin o Comprador), redirige a la interfaz correspondiente.
*   **Registro:** Permite crear nuevos usuarios, asignándoles por defecto el rol de 'Comprador' por seguridad."

**(Diapositiva 7: Panel de Inventario - Visualización)**

"Para el Administrador, el panel de Inventario es el centro de mando.
*   Cuenta con una **Barra de Búsqueda** en tiempo real que filtra por nombre, código o categoría.
*   La interacción principal es el **Doble Click**, que abre la ficha técnica del producto mostrando su imagen y detalles completos."

**(Diapositiva 8: Panel de Inventario - Acciones)**

"Las capacidades de gestión son completas (CRUD):
*   **Nuevo Producto:** Permite ingresar todos los datos, incluyendo la selección de imagen desde el disco.
*   **Editar Producto:** Una funcionalidad nueva que permite corregir errores o actualizar precios e imágenes de productos existentes.
*   **Actualizar Stock:** Una vía rápida para reponer mercadería sin editar todo el producto.
*   También tenemos opciones para **Eliminar**, **Reiniciar** la base de datos, **Crear nuevos Administradores** y **Exportar a Excel (CSV)** para respaldos."

**(Diapositiva 9: Punto de Venta)**

"El módulo de ventas (POS) está diseñado para la velocidad.
*   Permite buscar productos por nombre o escanear códigos.
*   El selector de cantidad se adapta: permite decimales si el producto es a granel (Kg).
*   El carrito calcula los subtotales y el total general automáticamente.
*   Al confirmar, se genera un ID único de venta y se descuenta el stock inmediatamente."

**(Diapositiva 10: Reportes y Alertas)**

"Para la toma de decisiones:
*   **Reportes:** Permite auditar cada venta realizada, viendo el detalle exacto de qué se vendió.
*   **Alertas:** Esta pestaña filtra automáticamente los productos críticos. Si el stock baja del mínimo (ej. 5 kg), aparece aquí para avisar que es necesario reponer."

**(Diapositiva 11: Perfil Comprador)**

"Finalmente, el perfil de Comprador tiene una vista restringida.
*   Puede ver el **Catálogo** y buscar productos, pero solo en modo lectura (no puede editar ni ver stock interno).
*   Tiene su propia pestaña de **Comprar** para realizar pedidos de auto-atención.

Con esto concluye el detalle técnico y funcional del sistema. Muchas gracias."
