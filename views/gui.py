"""Interfaz gráfica del sistema de supermercado.

Returns:
    class: Clases de la interfaz gráfica (LoginWindow, SupermercadoGUI, RegistroWindow)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models import Producto, Usuario
from controllers.supermercado_controller import SupermercadoController

class SupermercadoGUI:
    """
    Clase principal de la interfaz gráfica del supermercado.
    Maneja las pestañas y la interacción del usuario con el sistema.
    """
    def __init__(self, root, usuario: Usuario, controller: SupermercadoController, on_logout):
        # Referencias principales
        self.root = root
        self.usuario = usuario
        self.controller = controller
        self.on_logout = on_logout
        
        # Configuración de la ventana principal
        self.root.title(f"Supermercado - {self.usuario.username} ({self.usuario.role})")
        self.root.geometry("1024x768")
        
        # Configuración de estilos visuales
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Contenedor principal con padding
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inicialización de componentes
        self._setup_header()
        self._setup_notebook()
        
        # Evento para actualizar datos al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def _setup_header(self):
        """Configura el encabezado con el título y botones de sesión."""
        frame_header = ttk.Frame(self.main_container)
        frame_header.pack(fill=tk.X, pady=5)
        
        # Título dinámico según el rol
        titulo_texto = "Supermercado Manager" if self.usuario.role == 'admin' else "Supermercado - Compras"
        lbl_titulo = ttk.Label(frame_header, text=titulo_texto, font=('Helvetica', 18, 'bold'))
        lbl_titulo.pack(side=tk.LEFT, pady=(0, 10))

        # Botones de acción global
        ttk.Button(frame_header, text="Cerrar Sesión", command=self.cerrar_sesion).pack(side=tk.RIGHT)
        ttk.Button(frame_header, text="Recargar Datos", command=self.recargar_datos).pack(side=tk.RIGHT, padx=5)

    def _setup_notebook(self):
        """Configura las pestañas (tabs) según el rol del usuario."""
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Frames base para las pestañas
        self.tab_inventario = ttk.Frame(self.notebook)
        self.tab_ventas = ttk.Frame(self.notebook)
        
        if self.usuario.role == 'admin':
            # Pestañas exclusivas de administrador
            self.tab_reportes = ttk.Frame(self.notebook)
            self.tab_alertas = ttk.Frame(self.notebook)
            
            # Agrega pestañas al notebook
            self.notebook.add(self.tab_inventario, text="Inventario")
            self.notebook.add(self.tab_ventas, text="Ventas")
            self.notebook.add(self.tab_reportes, text="Reportes")
            self.notebook.add(self.tab_alertas, text="Alertas")
            
            # Inicializa el contenido de cada pestaña
            self.init_inventario_admin()
            self.init_ventas()
            self.init_reportes()
            self.init_alertas()
        else: # Comprador
            # Pestañas para comprador (orden diferente para priorizar la compra)
            self.notebook.add(self.tab_ventas, text="Comprar")
            self.notebook.add(self.tab_inventario, text="Catálogo")
            
            self.init_ventas()
            self.init_inventario_comprador()

    def recargar_datos(self):
        """Fuerza una recarga de datos desde los archivos JSON."""
        if messagebox.askyesno("Confirmar", "Recargar datos desde el archivo?"):
            self.controller.cargar_datos()
            self.on_tab_change() # Refresca la pestaña actual
            messagebox.showinfo("Éxito", "Datos actualizados.")

    def cerrar_sesion(self):
        """Ejecuta el callback de logout."""
        self.on_logout()

    def on_tab_change(self, event=None):
        """Manejador de evento de cambio de pestaña. Actualiza los datos visibles."""
        selected_tab_index = self.notebook.index(self.notebook.select())
        tab_text = self.notebook.tab(selected_tab_index, "text")
        
        # Lógica de actualización selectiva según la pestaña activa
        if "Inventario" in tab_text or "Catálogo" in tab_text:
            if self.usuario.role == 'admin':
                self.cargar_inventario_admin()
            else:
                self.cargar_inventario_comprador()
        elif "Reportes" in tab_text:
            self.actualizar_reportes()
        elif "Alertas" in tab_text:
            self.cargar_alertas()
        elif "Ventas" in tab_text or "Comprar" in tab_text:
            self.cargar_productos_venta()

    # --- Pestaña de Inventario (Admin) ---
    def init_inventario_admin(self):
        """Inicializa la pestaña de inventario para administradores."""
        # Frame para botones de acción y búsqueda
        self.frame_controles = ttk.Frame(self.tab_inventario)
        self.frame_controles.pack(fill=tk.X, pady=5)
        
        # Botones de gestión de inventario
        ttk.Button(self.frame_controles, text="Nuevo Producto", command=self.mostrar_dialogo_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_controles, text="Actualizar Stock", command=self.mostrar_dialogo_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_controles, text="Eliminar Producto", command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_controles, text="Reiniciar Productos", command=self.reiniciar_productos).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_controles, text="Crear Admin", command=self.mostrar_dialogo_crear_admin).pack(side=tk.LEFT, padx=5)
        
        # Campo de búsqueda en tiempo real
        ttk.Label(self.frame_controles, text="Buscar:").pack(side=tk.LEFT, padx=(20, 5))
        self.entry_buscar_inv = ttk.Entry(self.frame_controles)
        self.entry_buscar_inv.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        # Vincula el evento de soltar tecla para filtrar automáticamente
        self.entry_buscar_inv.bind('<KeyRelease>', lambda e: self.cargar_inventario_admin())
        
        # Configuración de la tabla (Treeview)
        columns = ('codigo', 'nombre', 'precio', 'stock', 'unidad', 'categoria', 'estado')
        self.tree_inv = ttk.Treeview(self.tab_inventario, columns=columns, show='headings')
        
        # Configura encabezados
        for col in columns:
            self.tree_inv.heading(col, text=col.capitalize())
        
        self.tree_inv.pack(fill=tk.BOTH, expand=True)
        # Carga inicial de datos
        self.cargar_inventario_admin()

    def cargar_inventario_admin(self):
        """Carga y muestra los productos en la tabla de inventario."""
        # Limpia la tabla actual
        for item in self.tree_inv.get_children():
            self.tree_inv.delete(item)
        
        # Obtiene el término de búsqueda
        termino = self.entry_buscar_inv.get()
        # Filtra si hay término de búsqueda, sino muestra todo
        productos = self.controller.buscar_producto(termino) if termino else self.controller.productos.values()
        
        for p in sorted(productos, key=lambda x: x.nombre):
            # Determina el estado visual del stock
            estado = "BAJO" if p.tiene_stock_bajo() else "OK"
            if p.stock == 0: estado = "AGOTADO"
            
            # Formatear stock según unidad (1 decimal para kg, enteros para otros)
            if p.unidad == 'kg':
                stock_display = f"{p.stock:.1f}"
            else:
                stock_display = f"{int(p.stock)}"
                
            # Inserta la fila en la tabla
            self.tree_inv.insert('', tk.END, iid=p.codigo, values=(
                p.codigo, p.nombre, f"${p.precio:,.0f}", stock_display, p.unidad, p.categoria, estado
            ))

    # --- Pestaña de Inventario (Comprador) ---
    def init_inventario_comprador(self):
        """Inicializa la vista de catálogo para compradores."""
        # Búsqueda
        frame_controles = ttk.Frame(self.tab_inventario)
        frame_controles.pack(fill=tk.X, pady=5)
        ttk.Label(frame_controles, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entry_buscar_cat = ttk.Entry(frame_controles)
        self.entry_buscar_cat.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar_cat.bind('<KeyRelease>', lambda e: self.cargar_inventario_comprador())

        # Tabla de catálogo (simplificada para el cliente)
        columns = ('nombre', 'precio', 'stock', 'categoria')
        self.tree_cat = ttk.Treeview(self.tab_inventario, columns=columns, show='headings')
        for col in columns:
            self.tree_cat.heading(col, text=col.capitalize())
        self.tree_cat.pack(fill=tk.BOTH, expand=True)
        self.cargar_inventario_comprador()

    def cargar_inventario_comprador(self):
        """Carga los productos en el catálogo del comprador."""
        for item in self.tree_cat.get_children():
            self.tree_cat.delete(item)
            
        termino = self.entry_buscar_cat.get()
        productos = self.controller.buscar_producto(termino) if termino else self.controller.productos.values()

        for p in sorted(productos, key=lambda x: x.nombre):
            # Formatear stock según unidad para visualización amigable
            if p.unidad == 'kg':
                stock_display = f"{p.stock:.1f} {p.unidad}"
            else:
                stock_display = f"{int(p.stock)} {p.unidad}"

            self.tree_cat.insert('', tk.END, values=(
                p.nombre, f"${p.precio:,.0f}", stock_display, p.categoria
            ))

    # --- Pestaña de Ventas ---
    def init_ventas(self):
        """Inicializa la interfaz de ventas (POS)."""
        # Panel dividido: Izquierda (Productos), Derecha (Carrito)
        paned = ttk.PanedWindow(self.tab_ventas, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel de productos disponibles
        frame_prod = ttk.Labelframe(paned, text="Productos Disponibles")
        self.entry_buscar_venta = ttk.Entry(frame_prod)
        self.entry_buscar_venta.pack(fill=tk.X, padx=5, pady=5)
        self.entry_buscar_venta.bind('<KeyRelease>', lambda e: self.cargar_productos_venta())
        
        cols_prod = ('nombre', 'precio', 'stock')
        self.tree_venta_prod = ttk.Treeview(frame_prod, columns=cols_prod, show='headings', height=10)
        for col in cols_prod: self.tree_venta_prod.heading(col, text=col.capitalize())
        self.tree_venta_prod.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_add = ttk.Frame(frame_prod)
        frame_add.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(frame_add, text="Cantidad:").pack(side=tk.LEFT)
        self.entry_cant_venta = ttk.Entry(frame_add, width=10)
        self.entry_cant_venta.pack(side=tk.LEFT, padx=5)
        self.entry_cant_venta.insert(0, "1")
        ttk.Button(frame_add, text="Agregar ->", command=self.agregar_al_carrito).pack(side=tk.RIGHT)
        
        # Panel de carrito de compras
        frame_cart = ttk.Labelframe(paned, text="Carrito")
        cols_cart = ('nombre', 'cantidad', 'subtotal')
        self.tree_cart = ttk.Treeview(frame_cart, columns=cols_cart, show='headings')
        for col in cols_cart: self.tree_cart.heading(col, text=col.capitalize())
        self.tree_cart.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.lbl_total = ttk.Label(frame_cart, text="TOTAL: $0.00", font=('Helvetica', 14, 'bold'))
        self.lbl_total.pack(pady=5)
        
        ttk.Button(frame_cart, text="Finalizar Venta", command=self.finalizar_venta).pack(fill=tk.X, padx=5)
        ttk.Button(frame_cart, text="Limpiar", command=self.limpiar_carrito).pack(fill=tk.X, padx=5, pady=5)
        
        paned.add(frame_prod, weight=1)
        paned.add(frame_cart, weight=1)
        
        self.carrito_items = {} # Diccionario para almacenar items del carrito {codigo: cantidad}
        self.cargar_productos_venta()

    def cargar_productos_venta(self):
        """Carga los productos disponibles para la venta (stock > 0)."""
        # Limpia la lista de productos
        for item in self.tree_venta_prod.get_children():
            self.tree_venta_prod.delete(item)
        
        # Filtra productos disponibles
        termino = self.entry_buscar_venta.get()
        productos = self.controller.buscar_producto(termino) if termino else self.controller.obtener_productos_disponibles()
        
        for p in sorted(productos, key=lambda x: x.nombre):
            if p.stock > 0:
                # Formatear stock según unidad
                if p.unidad == 'kg':
                    stock_display = f"{p.stock:.1f}"
                else:
                    stock_display = f"{int(p.stock)}"
                self.tree_venta_prod.insert('', tk.END, iid=p.codigo, values=(p.nombre, f"${p.precio:,.0f}", stock_display))

    def agregar_al_carrito(self):
        """Agrega el producto seleccionado al carrito de compras."""
        selected = self.tree_venta_prod.selection()
        if not selected: return
        codigo = selected[0]
        
        try:
            # Obtiene la cantidad ingresada
            cantidad_val = float(self.entry_cant_venta.get())
            producto = self.controller.productos[codigo]
            
            if cantidad_val <= 0: raise ValueError("Cantidad debe ser positiva.")
            
            # Validación específica por tipo de unidad
            if producto.unidad == 'kg':
                # Para kg permitimos 1 decimal
                cantidad = round(cantidad_val, 1)
            else:
                # Para unidades discretas, debe ser entero
                if not cantidad_val.is_integer():
                    raise ValueError(f"Producto se vende en {producto.unidad} enteras.")
                cantidad = int(cantidad_val)

            # Verifica stock disponible
            if cantidad > producto.stock:
                raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

            # Actualiza la cantidad si ya existe en el carrito
            self.carrito_items[codigo] = self.carrito_items.get(codigo, 0) + cantidad
            self.actualizar_carrito_y_total()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_carrito_y_total(self):
        """Refresca la vista del carrito y recalcula el total."""
        # Limpia la tabla del carrito
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)
        
        total = 0
        # Recorre los items en el carrito para calcular subtotales
        for codigo, cantidad in self.carrito_items.items():
            producto = self.controller.productos[codigo]
            subtotal = producto.precio * cantidad
            total += subtotal
            
            # Formato de cantidad según unidad
            if producto.unidad == 'kg':
                cant_display = f"{cantidad:.1f}"
            else:
                cant_display = f"{int(cantidad)}"
                
            self.tree_cart.insert('', tk.END, values=(producto.nombre, cant_display, f"${subtotal:,.0f}"))
        
        # Actualiza la etiqueta del total
        self.lbl_total.config(text=f"TOTAL: ${total:,.0f}")

    def limpiar_carrito(self):
        """Vacía el carrito de compras."""
        self.carrito_items.clear()
        self.actualizar_carrito_y_total()

    def finalizar_venta(self):
        """Procesa la venta final, actualizando stock y guardando registro."""
        if not self.carrito_items: return
        
        items_venta = list(self.carrito_items.items())
        # Confirmación de usuario
        if messagebox.askyesno("Confirmar", f"Proceder con la venta por {self.lbl_total['text']}?"):
            # Llama al controlador para procesar la transacción
            venta = self.controller.realizar_venta(items_venta)
            if venta:
                messagebox.showinfo("Éxito", f"Venta realizada! ID: {venta.id}\nTotal: ${venta.total:,.0f}")
                # Limpia y actualiza la vista
                self.limpiar_carrito()
                self.cargar_productos_venta()
            else:
                messagebox.showerror("Error", "No se pudo procesar la venta. Verifique el stock.")

    # --- Pestaña de Reportes ---
    def init_reportes(self):
        """Inicializa la vista de reportes y estadísticas."""
        self.frame_stats = ttk.Frame(self.tab_reportes, padding=20)
        self.frame_stats.pack(fill=tk.BOTH, expand=True)
        
        # Etiquetas para métricas generales
        self.lbl_stats_prod = ttk.Label(self.frame_stats, font=('Helvetica', 12))
        self.lbl_stats_prod.pack(anchor=tk.W, pady=5)
        
        self.lbl_stats_ventas = ttk.Label(self.frame_stats, font=('Helvetica', 12))
        self.lbl_stats_ventas.pack(anchor=tk.W, pady=5)
        
        self.lbl_stats_ingresos = ttk.Label(self.frame_stats, font=('Helvetica', 12))
        self.lbl_stats_ingresos.pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.frame_stats).pack(fill=tk.X, pady=20)
        ttk.Label(self.frame_stats, text="Últimas Ventas (Doble click para ver detalle):", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        
        # Tabla de historial de ventas
        cols = ('id', 'fecha', 'total', 'items')
        self.tree_ventas = ttk.Treeview(self.frame_stats, columns=cols, show='headings', height=10)
        self.tree_ventas.heading('id', text='ID')
        self.tree_ventas.heading('fecha', text='Fecha')
        self.tree_ventas.heading('total', text='Total')
        self.tree_ventas.heading('items', text='Items')
        
        self.tree_ventas.column('id', width=50)
        self.tree_ventas.column('fecha', width=150)
        self.tree_ventas.column('total', width=100)
        self.tree_ventas.column('items', width=50)
        
        self.tree_ventas.pack(fill=tk.BOTH, expand=True, pady=10)
        # Vincula doble click para ver detalles de una venta específica
        self.tree_ventas.bind("<Double-1>", self.mostrar_detalle_venta)
        
        self.actualizar_reportes()

    def actualizar_reportes(self):
        """Calcula y muestra las estadísticas actualizadas."""
        # Obtiene datos agregados del controlador
        stats = self.controller.obtener_estadisticas()
        self.lbl_stats_prod.config(text=f"Total Productos: {stats['total_productos']} (Valor: ${stats['valor_inventario']:,.0f})")
        self.lbl_stats_ventas.config(text=f"Total Ventas: {stats['total_ventas']}")
        self.lbl_stats_ingresos.config(text=f"Ingresos Totales: ${stats['ingresos_totales']:,.0f}")
        
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
            
        for venta in reversed(self.controller.ventas):
            id_venta = venta.get('id', 'N/A')
            self.tree_ventas.insert('', tk.END, iid=id_venta, values=(
                id_venta, 
                venta['fecha'], 
                f"${venta['total']:,.0f}", 
                len(venta['items'])
            ))

    def mostrar_detalle_venta(self, event):
        """Muestra un popup con los detalles de la venta seleccionada."""
        selected = self.tree_ventas.selection()
        if not selected: return
        
        id_venta = selected[0]
        # Buscar la venta por ID (como es string en el treeview, convertir si es necesario)
        venta_data = next((v for v in self.controller.ventas if str(v.get('id')) == str(id_venta)), None)
        
        if not venta_data: return
        
        # Crea ventana emergente (Toplevel)
        detalle = tk.Toplevel(self.root)
        detalle.title(f"Detalle Venta #{id_venta}")
        detalle.geometry("500x400")
        
        ttk.Label(detalle, text=f"Venta #{id_venta} - {venta_data['fecha']}", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Tabla de detalle de items
        cols = ('producto', 'cantidad', 'precio', 'subtotal')
        tree_det = ttk.Treeview(detalle, columns=cols, show='headings')
        tree_det.heading('producto', text='Producto')
        tree_det.heading('cantidad', text='Cant.')
        tree_det.heading('precio', text='Precio Unit.')
        tree_det.heading('subtotal', text='Subtotal')
        
        tree_det.column('producto', width=150)
        tree_det.column('cantidad', width=60)
        tree_det.column('precio', width=80)
        tree_det.column('subtotal', width=80)
        
        tree_det.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for item in venta_data['items']:
            # Formato condicional para cantidad en el detalle histórico
            if item.get('unidad') == 'kg':
                cant_display = f"{item['cantidad']:.1f}"
            else:
                cant_display = f"{int(item['cantidad'])}"

            tree_det.insert('', tk.END, values=(
                item['nombre'],
                f"{cant_display} {item.get('unidad', '')}",
                f"${item['precio_unitario']:,.0f}",
                f"${item['subtotal']:,.0f}"
            ))
            
        ttk.Label(detalle, text=f"TOTAL: ${venta_data['total']:,.0f}", font=('Helvetica', 12, 'bold')).pack(pady=10, padx=10, anchor=tk.E)
        ttk.Button(detalle, text="Cerrar", command=detalle.destroy).pack(pady=10)

    # --- Pestaña de Alertas ---
    def init_alertas(self):
        """Inicializa la vista de alertas de stock bajo."""
        ttk.Label(self.tab_alertas, text="Productos con Stock Crítico", font=('Helvetica', 14, 'bold'), foreground='red').pack(pady=10)
        
        # Tabla de alertas
        cols = ('codigo', 'nombre', 'stock', 'minimo')
        self.tree_alertas = ttk.Treeview(self.tab_alertas, columns=cols, show='headings')
        for col in cols: self.tree_alertas.heading(col, text=col.capitalize())
        self.tree_alertas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Button(self.tab_alertas, text="Actualizar", command=self.cargar_alertas).pack(pady=10)
        self.cargar_alertas()

    def cargar_alertas(self):
        """Filtra y muestra solo los productos con stock bajo."""
        # Limpia la tabla
        for item in self.tree_alertas.get_children():
            self.tree_alertas.delete(item)
            
        # Obtiene productos críticos desde el controlador
        for p in self.controller.obtener_productos_stock_bajo():
            # Formatear stock según unidad
            if p.unidad == 'kg':
                stock_display = f"{p.stock:.1f}"
                min_display = f"{p.stock_minimo:.1f}"
            else:
                stock_display = f"{int(p.stock)}"
                min_display = f"{int(p.stock_minimo)}"
            self.tree_alertas.insert('', tk.END, values=(p.codigo, p.nombre, stock_display, min_display))

    # --- Diálogos ---
    def mostrar_dialogo_producto(self):
        """Muestra formulario para agregar producto en la misma ventana"""
        # Ocultar la tabla y controles temporalmente para mostrar el formulario
        self.tree_inv.pack_forget()
        self.frame_controles.pack_forget()
        
        # Crear frame para el formulario
        form_frame = ttk.Frame(self.tab_inventario)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Nuevo Producto", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Campos del formulario
        campos_frame = ttk.Frame(form_frame)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        
        entries = {}
        
        # Código (Oculto, se genera al guardar)
        # row_frame = ttk.Frame(campos_frame)
        # row_frame.pack(fill=tk.X, pady=5)
        # ttk.Label(row_frame, text="Código:", width=25).pack(side=tk.LEFT)
        # nuevo_codigo = self.controller.producto_controller.generar_codigo()
        # entry_codigo = ttk.Entry(row_frame)
        # entry_codigo.insert(0, nuevo_codigo)
        # entry_codigo.config(state='readonly')
        # entry_codigo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # entries['codigo'] = entry_codigo
        
        # Nombre
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Nombre:", width=25).pack(side=tk.LEFT)
        entry_nombre = ttk.Entry(row_frame)
        entry_nombre.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entries['nombre'] = entry_nombre
        
        # Precio
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Precio (CLP):", width=25).pack(side=tk.LEFT)
        entry_precio = ttk.Entry(row_frame)
        entry_precio.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entries['precio'] = entry_precio
        
        # Stock
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Stock Inicial:", width=25).pack(side=tk.LEFT)
        entry_stock = ttk.Entry(row_frame)
        entry_stock.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entries['stock'] = entry_stock
        
        # Categoría (Combobox)
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Categoría:", width=25).pack(side=tk.LEFT)
        combo_categoria = ttk.Combobox(row_frame, state='readonly', values=[
            "Abarrotes", "Lácteos", "Panadería", "Frutas", "Verduras", 
            "Carnes", "Bebidas", "Limpieza", "Snacks", "Congelados"
        ])
        combo_categoria.pack(side=tk.LEFT, fill=tk.X, expand=True)
        combo_categoria.set("Abarrotes")  # Valor por defecto
        entries['categoria'] = combo_categoria
        
        # Unidad (Combobox)
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Unidad:", width=25).pack(side=tk.LEFT)
        combo_unidad = ttk.Combobox(row_frame, state='readonly', values=["unidades", "kg"])
        combo_unidad.pack(side=tk.LEFT, fill=tk.X, expand=True)
        combo_unidad.set("kg")  # Valor por defecto cambiado a kg
        entries['unidad'] = combo_unidad

        # Evento para cambiar unidades según categoría
        def on_categoria_change(event):
            cat = combo_categoria.get()
            if cat == "Bebidas":
                combo_unidad['values'] = ["unidades", "kg", "mL"]
            else:
                combo_unidad['values'] = ["unidades", "kg"]
                if combo_unidad.get() == "mL":
                    combo_unidad.set("kg")
        
        combo_categoria.bind("<<ComboboxSelected>>", on_categoria_change)
        
        # Stock Mínimo
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Stock Mínimo:", width=25).pack(side=tk.LEFT)
        entry_stock_minimo = ttk.Entry(row_frame)
        entry_stock_minimo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry_stock_minimo.insert(0, "5")
        entries['stock_minimo'] = entry_stock_minimo
        
        def guardar():
            try:
                # Generar código automáticamente al guardar
                codigo = self.controller.producto_controller.generar_codigo()
                
                nombre = entries['nombre'].get().strip()
                categoria = entries['categoria'].get().strip()
                unidad = entries['unidad'].get().strip() # No usar lower() para mantener 'mL'
                
                if not nombre or not categoria:
                    messagebox.showwarning("Error", "Todos los campos de texto son obligatorios")
                    return

                # Validación de nombre (Permitir letras, números, espacios y caracteres comunes)
                # Se permite alfanumérico para casos como "Coca Cola 3L" o "Arroz 1kg"
                caracteres_validos = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .-%")
                if not set(nombre).issubset(caracteres_validos):
                    messagebox.showwarning("Error", "El nombre contiene caracteres no válidos.\nUse letras, números, espacios, puntos, guiones o %.")
                    return
                
                # Validación lógica: Debe contener al menos una letra (evita "123" o "---")
                if not any(c.isalpha() for c in nombre):
                     messagebox.showwarning("Error", "El nombre del producto debe contener al menos una letra.")
                     return

                if unidad not in ['unidades', 'kg', 'mL']:
                    messagebox.showwarning("Error", "La unidad debe ser 'unidades', 'kg' o 'mL'")
                    return

                precio = int(entries['precio'].get())
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo")

                # Enforzar enteros para el stock (Unidades y mL se manejan en enteros)
                # Para kg permitimos decimales (1 decimal)
                try:
                    stock_val = float(entries['stock'].get())
                    if unidad == 'kg':
                        stock = round(stock_val, 1)
                    else:
                        stock = int(stock_val)
                except ValueError:
                    raise ValueError("El stock debe ser un número válido")
                
                if stock < 0:
                    raise ValueError("El stock no puede ser negativo")

                try:
                    stock_min_val = float(entries['stock_minimo'].get())
                    if unidad == 'kg':
                        stock_min = round(stock_min_val, 1)
                    else:
                        stock_min = int(stock_min_val)
                except ValueError:
                    raise ValueError("El stock mínimo debe ser un número válido")
                
                if stock_min < 0:
                    raise ValueError("El stock mínimo no puede ser negativo")

                p = Producto(codigo, nombre, precio, stock, categoria, unidad, stock_min)
                
                if self.controller.agregar_producto(p):
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    cancelar()
                    self.cargar_inventario_admin()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el producto.\nVerifique que el código o el nombre no existan ya.")
            except ValueError as e:
                messagebox.showerror("Error", f"Valores inválidos: {str(e)}")
        
        def cancelar():
            form_frame.destroy()
            self.frame_controles.pack(fill=tk.X, pady=5)
            self.tree_inv.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=cancelar).pack(side=tk.LEFT, padx=5)

    def mostrar_dialogo_stock(self):
        """Muestra formulario para actualizar stock en la misma ventana"""
        selected = self.tree_inv.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione un producto de la lista")
            return
            
        codigo = selected[0]
        producto = self.controller.productos[codigo]
        
        # Ocultar la tabla y controles temporalmente
        self.tree_inv.pack_forget()
        self.frame_controles.pack_forget()
        
        # Crear frame para el formulario
        form_frame = ttk.Frame(self.tab_inventario)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text=f"Actualizar Stock", font=('Helvetica', 14, 'bold')).pack(pady=10)
        ttk.Label(form_frame, text=f"Producto: {producto.nombre}", font=('Helvetica', 12)).pack(pady=5)
        
        if producto.unidad == 'kg':
            stock_str = f"{producto.stock:.1f}"
        else:
            stock_str = f"{int(producto.stock)}"
            
        ttk.Label(form_frame, text=f"Stock actual: {stock_str} {producto.unidad}", font=('Helvetica', 10)).pack(pady=5)
        
        # Frame para opciones
        opciones_frame = ttk.Frame(form_frame)
        opciones_frame.pack(pady=20)
        
        tipo_var = tk.StringVar(value="agregar")
        ttk.Radiobutton(opciones_frame, text="Agregar", variable=tipo_var, value="agregar").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(opciones_frame, text="Restar", variable=tipo_var, value="restar").pack(side=tk.LEFT, padx=10)
        
        # Campo de cantidad
        ttk.Label(form_frame, text="Cantidad:").pack(pady=5)
        entry_cant = ttk.Entry(form_frame, width=20)
        entry_cant.pack(pady=5)
        entry_cant.focus()
        
        def actualizar():
            try:
                # Enforzar enteros para la cantidad, excepto si es kg
                cant_val = float(entry_cant.get())
                if cant_val <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return

                if producto.unidad == 'kg':
                    cant = round(cant_val, 1)
                else:
                    if not cant_val.is_integer():
                         messagebox.showerror("Error", f"El producto se maneja por {producto.unidad}.\nNo se admiten decimales.")
                         return
                    cant = int(cant_val)

                if self.controller.actualizar_stock(codigo, cant, tipo_var.get()):
                    prod = self.controller.productos[codigo]
                    if prod.tiene_stock_bajo():
                        if prod.unidad == 'kg':
                            stock_msg = f"{prod.stock:.1f}"
                        else:
                            stock_msg = f"{int(prod.stock)}"
                        messagebox.showwarning("Alerta de Stock", f"El producto '{prod.nombre}' tiene stock bajo: {stock_msg} {prod.unidad}")
                    else:
                        messagebox.showinfo("Éxito", "Stock actualizado correctamente")
                    
                    cancelar()
                    self.cargar_inventario_admin()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar (Stock insuficiente?)")
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida")
        
        def cancelar():
            form_frame.destroy()
            self.frame_controles.pack(fill=tk.X, pady=5)
            self.tree_inv.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame, text="Actualizar", command=actualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=cancelar).pack(side=tk.LEFT, padx=5)
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        selected = self.tree_inv.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione un producto de la lista")
            return
            
        codigo = selected[0]
        producto = self.controller.productos[codigo]
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Está seguro de eliminar el producto '{producto.nombre}'?\n\nEsta acción no se puede deshacer."):
            if self.controller.eliminar_producto(codigo):
                messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' eliminado correctamente")
                self.cargar_inventario_admin()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
    
    def reiniciar_productos(self):
        """Reinicia todos los productos a los valores por defecto"""
        if messagebox.askyesno("Confirmar Reinicio", 
                              "¿Está seguro de reiniciar todos los productos a los valores por defecto?\n\n"
                              "Esto eliminará todos los productos actuales y los reemplazará con los productos de ejemplo.\n"
                              "Las ventas y usuarios NO se verán afectados.\n\n"
                              "Esta acción no se puede deshacer."):
            if self.controller.reiniciar_productos():
                messagebox.showinfo("Éxito", "Productos reiniciados correctamente")
                self.cargar_inventario_admin()
            else:
                messagebox.showerror("Error", "No se pudo reiniciar los productos")

    def mostrar_dialogo_crear_admin(self):
        """Muestra formulario para crear un nuevo administrador"""
        # Ocultar la tabla y controles temporalmente
        self.tree_inv.pack_forget()
        self.frame_controles.pack_forget()
        
        # Crear frame para el formulario
        form_frame = ttk.Frame(self.tab_inventario)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Nuevo Administrador", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Campos del formulario
        campos_frame = ttk.Frame(form_frame)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        
        entries = {}
        
        # Usuario
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Usuario:", width=25).pack(side=tk.LEFT)
        entry_user = ttk.Entry(row_frame)
        entry_user.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entries['username'] = entry_user
        
        # Contraseña
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Contraseña:", width=25).pack(side=tk.LEFT)
        entry_pass = ttk.Entry(row_frame, show="*")
        entry_pass.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entries['password'] = entry_pass
        
        def guardar():
            username = entries['username'].get().strip()
            password = entries['password'].get().strip()
            
            if not username or not password:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return

            try:
                if self.controller.registrar_usuario(username, password, 'admin'):
                    messagebox.showinfo("Éxito", f"Administrador '{username}' creado correctamente")
                    cancelar()
                else:
                    messagebox.showerror("Error", "El nombre de usuario ya existe")
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
        
        def cancelar():
            form_frame.destroy()
            self.frame_controles.pack(fill=tk.X, pady=5)
            self.tree_inv.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame, text="Crear Admin", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=cancelar).pack(side=tk.LEFT, padx=5)

class LoginWindow:
    def __init__(self, root, controller: SupermercadoController, on_login_success, on_show_registro):
        self.root = root
        self.controller = controller
        self.on_login_success = on_login_success
        self.on_show_registro = on_show_registro
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.frame, text="Iniciar Sesión", font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        ttk.Label(self.frame, text="Usuario:").pack(anchor=tk.W)
        self.entry_user = ttk.Entry(self.frame)
        self.entry_user.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.frame, text="Contraseña:").pack(anchor=tk.W)
        self.entry_pass = ttk.Entry(self.frame, show="*")
        self.entry_pass.pack(fill=tk.X, pady=5)
        
        ttk.Button(self.frame, text="Ingresar", command=self.login).pack(fill=tk.X, pady=20)
        ttk.Button(self.frame, text="Crear cuenta de Comprador", command=self.mostrar_registro).pack(fill=tk.X)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        usuario = self.controller.autenticar_usuario(user, pwd)
        
        if usuario:
            self.frame.destroy()
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_registro(self):
        self.on_show_registro()

class RegistroWindow:
    def __init__(self, root, controller: SupermercadoController, on_volver_login, on_registro_exitoso):
        self.root = root
        self.controller = controller
        self.on_volver_login = on_volver_login
        self.on_registro_exitoso = on_registro_exitoso
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.frame, text="Nuevo Usuario", font=('Helvetica', 14, 'bold')).pack(pady=20)
        
        ttk.Label(self.frame, text="Usuario:").pack(anchor=tk.W)
        self.entry_user = ttk.Entry(self.frame)
        self.entry_user.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.frame, text="Contraseña:").pack(anchor=tk.W)
        self.entry_pass = ttk.Entry(self.frame, show="*")
        self.entry_pass.pack(fill=tk.X, pady=5)
        
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(btn_frame, text="Registrar", command=self.registrar).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(btn_frame, text="Volver", command=self.volver).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

    def volver(self):
        self.frame.destroy()
        self.on_volver_login()

    def registrar(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if not user or not pwd:
            messagebox.showwarning("Aviso", "Complete todos los campos")
            return
            
        try:
            if self.controller.registrar_usuario(user, pwd, 'comprador'):
                messagebox.showinfo("Éxito", "Usuario registrado. Ahora puede iniciar sesión.")
                self.frame.destroy()
                self.on_registro_exitoso()
            else:
                messagebox.showerror("Error", "El nombre de usuario ya existe")
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
