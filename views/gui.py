import tkinter as tk
from tkinter import ttk, messagebox
from models import Producto, Usuario
from controllers.supermercado_controller import SupermercadoController

class SupermercadoGUI:
    def __init__(self, root, usuario: Usuario, controller: SupermercadoController, on_logout):
        self.root = root
        self.usuario = usuario
        self.controller = controller
        self.on_logout = on_logout
        
        self.root.title(f"Supermercado - {self.usuario.username} ({self.usuario.role})")
        self.root.geometry("1024x768")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._setup_header()
        self._setup_notebook()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def _setup_header(self):
        frame_header = ttk.Frame(self.main_container)
        frame_header.pack(fill=tk.X, pady=5)
        
        titulo_texto = "🛒 Supermercado Manager" if self.usuario.role == 'admin' else "🛒 Supermercado - Compras"
        lbl_titulo = ttk.Label(frame_header, text=titulo_texto, font=('Helvetica', 18, 'bold'))
        lbl_titulo.pack(side=tk.LEFT, pady=(0, 10))

        ttk.Button(frame_header, text="Cerrar Sesión", command=self.cerrar_sesion).pack(side=tk.RIGHT)
        ttk.Button(frame_header, text="🔄 Recargar Datos", command=self.recargar_datos).pack(side=tk.RIGHT, padx=5)

    def _setup_notebook(self):
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab_inventario = ttk.Frame(self.notebook)
        self.tab_ventas = ttk.Frame(self.notebook)
        
        if self.usuario.role == 'admin':
            self.tab_reportes = ttk.Frame(self.notebook)
            self.tab_alertas = ttk.Frame(self.notebook)
            
            self.notebook.add(self.tab_inventario, text="📦 Inventario")
            self.notebook.add(self.tab_ventas, text="💰 Ventas")
            self.notebook.add(self.tab_reportes, text="📊 Reportes")
            self.notebook.add(self.tab_alertas, text="⚠️ Alertas")
            
            self.init_inventario_admin()
            self.init_ventas()
            self.init_reportes()
            self.init_alertas()
        else: # Comprador
            self.notebook.add(self.tab_ventas, text="🛒 Comprar")
            self.notebook.add(self.tab_inventario, text="📋 Catálogo")
            
            self.init_ventas()
            self.init_inventario_comprador()

    def recargar_datos(self):
        if messagebox.askyesno("Confirmar", "Recargar datos desde el archivo?"):
            self.controller.cargar_datos()
            self.on_tab_change() # Refresh current tab
            messagebox.showinfo("Éxito", "Datos actualizados.")

    def cerrar_sesion(self):
        self.on_logout()

    def on_tab_change(self, event=None):
        selected_tab_index = self.notebook.index(self.notebook.select())
        tab_text = self.notebook.tab(selected_tab_index, "text")
        
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
        # Controles
        frame_controles = ttk.Frame(self.tab_inventario)
        frame_controles.pack(fill=tk.X, pady=5)
        ttk.Button(frame_controles, text="➕ Nuevo Producto", command=self.mostrar_dialogo_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="🔄 Actualizar Stock", command=self.mostrar_dialogo_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="🗑️ Eliminar Producto", command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="♻️ Reiniciar Productos", command=self.reiniciar_productos).pack(side=tk.LEFT, padx=5)
        
        # Búsqueda
        ttk.Label(frame_controles, text="Buscar:").pack(side=tk.LEFT, padx=(20, 5))
        self.entry_buscar_inv = ttk.Entry(frame_controles)
        self.entry_buscar_inv.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar_inv.bind('<KeyRelease>', lambda e: self.cargar_inventario_admin())
        
        # Tabla
        columns = ('codigo', 'nombre', 'precio', 'stock', 'unidad', 'categoria', 'estado')
        self.tree_inv = ttk.Treeview(self.tab_inventario, columns=columns, show='headings')
        for col in columns:
            self.tree_inv.heading(col, text=col.capitalize())
        self.tree_inv.pack(fill=tk.BOTH, expand=True)
        self.cargar_inventario_admin()

    def cargar_inventario_admin(self):
        for item in self.tree_inv.get_children():
            self.tree_inv.delete(item)
        
        termino = self.entry_buscar_inv.get()
        productos = self.controller.buscar_producto(termino) if termino else self.controller.productos.values()
        
        for p in sorted(productos, key=lambda x: x.nombre):
            estado = "⚠️ BAJO" if p.tiene_stock_bajo() else "✅ OK"
            if p.stock == 0: estado = "❌ AGOTADO"
            self.tree_inv.insert('', tk.END, iid=p.codigo, values=(
                p.codigo, p.nombre, f"${p.precio:,.0f}", p.stock, p.unidad, p.categoria, estado
            ))

    # --- Pestaña de Inventario (Comprador) ---
    def init_inventario_comprador(self):
        # Búsqueda
        frame_controles = ttk.Frame(self.tab_inventario)
        frame_controles.pack(fill=tk.X, pady=5)
        ttk.Label(frame_controles, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entry_buscar_cat = ttk.Entry(frame_controles)
        self.entry_buscar_cat.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar_cat.bind('<KeyRelease>', lambda e: self.cargar_inventario_comprador())

        # Tabla
        columns = ('nombre', 'precio', 'stock', 'categoria')
        self.tree_cat = ttk.Treeview(self.tab_inventario, columns=columns, show='headings')
        for col in columns:
            self.tree_cat.heading(col, text=col.capitalize())
        self.tree_cat.pack(fill=tk.BOTH, expand=True)
        self.cargar_inventario_comprador()

    def cargar_inventario_comprador(self):
        for item in self.tree_cat.get_children():
            self.tree_cat.delete(item)
            
        termino = self.entry_buscar_cat.get()
        productos = self.controller.buscar_producto(termino) if termino else self.controller.productos.values()

        for p in sorted(productos, key=lambda x: x.nombre):
            self.tree_cat.insert('', tk.END, values=(
                p.nombre, f"${p.precio:,.0f}", f"{p.stock} {p.unidad}", p.categoria
            ))

    # --- Pestaña de Ventas ---
    def init_ventas(self):
        paned = ttk.PanedWindow(self.tab_ventas, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel de productos
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
        ttk.Button(frame_add, text="Agregar ➡️", command=self.agregar_al_carrito).pack(side=tk.RIGHT)
        
        # Panel de carrito
        frame_cart = ttk.Labelframe(paned, text="Carrito")
        cols_cart = ('nombre', 'cantidad', 'subtotal')
        self.tree_cart = ttk.Treeview(frame_cart, columns=cols_cart, show='headings')
        for col in cols_cart: self.tree_cart.heading(col, text=col.capitalize())
        self.tree_cart.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.lbl_total = ttk.Label(frame_cart, text="TOTAL: $0.00", font=('Helvetica', 14, 'bold'))
        self.lbl_total.pack(pady=5)
        
        ttk.Button(frame_cart, text="✅ Finalizar Venta", command=self.finalizar_venta).pack(fill=tk.X, padx=5)
        ttk.Button(frame_cart, text="🗑️ Limpiar", command=self.limpiar_carrito).pack(fill=tk.X, padx=5, pady=5)
        
        paned.add(frame_prod, weight=1)
        paned.add(frame_cart, weight=1)
        
        self.carrito_items = {} # {codigo: cantidad}
        self.cargar_productos_venta()

    def cargar_productos_venta(self):
        for item in self.tree_venta_prod.get_children():
            self.tree_venta_prod.delete(item)
        
        termino = self.entry_buscar_venta.get()
        productos = self.controller.buscar_producto(termino) if termino else self.controller.obtener_productos_disponibles()
        
        for p in sorted(productos, key=lambda x: x.nombre):
            if p.stock > 0:
                self.tree_venta_prod.insert('', tk.END, iid=p.codigo, values=(p.nombre, f"${p.precio:,.0f}", p.stock))

    def agregar_al_carrito(self):
        selected = self.tree_venta_prod.selection()
        if not selected: return
        codigo = selected[0]
        
        try:
            cantidad = float(self.entry_cant_venta.get())
            producto = self.controller.productos[codigo]
            
            if cantidad <= 0: raise ValueError("Cantidad debe ser positiva.")
            if producto.unidad == 'unidades' and not cantidad.is_integer():
                raise ValueError("Producto se vende en unidades enteras.")
            if cantidad > producto.stock:
                raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

            self.carrito_items[codigo] = self.carrito_items.get(codigo, 0) + cantidad
            self.actualizar_carrito_y_total()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_carrito_y_total(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)
        
        total = 0
        for codigo, cantidad in self.carrito_items.items():
            producto = self.controller.productos[codigo]
            subtotal = producto.precio * cantidad
            total += subtotal
            self.tree_cart.insert('', tk.END, values=(producto.nombre, cantidad, f"${subtotal:,.0f}"))
        
        self.lbl_total.config(text=f"TOTAL: ${total:,.0f}")

    def limpiar_carrito(self):
        self.carrito_items.clear()
        self.actualizar_carrito_y_total()

    def finalizar_venta(self):
        if not self.carrito_items: return
        
        items_venta = list(self.carrito_items.items())
        if messagebox.askyesno("Confirmar", f"Proceder con la venta por {self.lbl_total['text']}?"):
            venta = self.controller.realizar_venta(items_venta)
            if venta:
                messagebox.showinfo("Éxito", f"Venta realizada! Total: ${venta.total:,.0f}")
                self.limpiar_carrito()
                self.cargar_productos_venta()
            else:
                messagebox.showerror("Error", "No se pudo procesar la venta. Verifique el stock.")

    # --- Pestaña de Reportes ---
    def init_reportes(self):
        self.frame_stats = ttk.Frame(self.tab_reportes, padding=20)
        self.frame_stats.pack(fill=tk.BOTH, expand=True)
        
        self.lbl_stats_prod = ttk.Label(self.frame_stats, font=('Helvetica', 12))
        self.lbl_stats_prod.pack(anchor=tk.W, pady=5)
        
        self.lbl_stats_ventas = ttk.Label(self.frame_stats, font=('Helvetica', 12))
        self.lbl_stats_ventas.pack(anchor=tk.W, pady=5)
        
        self.lbl_stats_ingresos = ttk.Label(self.frame_stats, font=('Helvetica', 12))
        self.lbl_stats_ingresos.pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.frame_stats).pack(fill=tk.X, pady=20)
        ttk.Label(self.frame_stats, text="Últimas Ventas:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        
        self.txt_log = tk.Text(self.frame_stats, height=15, state='disabled')
        self.txt_log.pack(fill=tk.BOTH, expand=True, pady=10)
        self.actualizar_reportes()

    def actualizar_reportes(self):
        stats = self.controller.obtener_estadisticas()
        self.lbl_stats_prod.config(text=f"📦 Total Productos: {stats['total_productos']} (Valor: ${stats['valor_inventario']:,.0f})")
        self.lbl_stats_ventas.config(text=f"🛒 Total Ventas: {stats['total_ventas']}")
        self.lbl_stats_ingresos.config(text=f"💰 Ingresos Totales: ${stats['ingresos_totales']:,.0f}")
        
        self.txt_log.config(state='normal')
        self.txt_log.delete(1.0, tk.END)
        for venta in reversed(self.controller.ventas[-10:]):
            self.txt_log.insert(tk.END, f"📅 {venta['fecha']} | Total: ${venta['total']:,.0f} | Items: {len(venta['items'])}\n")
        self.txt_log.config(state='disabled')

    # --- Pestaña de Alertas ---
    def init_alertas(self):
        ttk.Label(self.tab_alertas, text="⚠️ Productos con Stock Crítico", font=('Helvetica', 14, 'bold'), foreground='red').pack(pady=10)
        cols = ('codigo', 'nombre', 'stock', 'minimo')
        self.tree_alertas = ttk.Treeview(self.tab_alertas, columns=cols, show='headings')
        for col in cols: self.tree_alertas.heading(col, text=col.capitalize())
        self.tree_alertas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        ttk.Button(self.tab_alertas, text="🔄 Actualizar", command=self.cargar_alertas).pack(pady=10)
        self.cargar_alertas()

    def cargar_alertas(self):
        for item in self.tree_alertas.get_children():
            self.tree_alertas.delete(item)
        for p in self.controller.obtener_productos_stock_bajo():
            self.tree_alertas.insert('', tk.END, values=(p.codigo, p.nombre, p.stock, p.stock_minimo))

    # --- Diálogos ---
    def mostrar_dialogo_producto(self):
        """Muestra formulario para agregar producto en la misma ventana"""
        # Ocultar la tabla temporalmente
        self.tree_inv.pack_forget()
        
        # Crear frame para el formulario
        form_frame = ttk.Frame(self.tab_inventario)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="➕ Nuevo Producto", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Campos del formulario
        campos_frame = ttk.Frame(form_frame)
        campos_frame.pack(fill=tk.BOTH, expand=True)
        
        entries = {}
        
        # Código
        row_frame = ttk.Frame(campos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Código:", width=25).pack(side=tk.LEFT)
        entry_codigo = ttk.Entry(row_frame)
        entry_codigo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entries['codigo'] = entry_codigo
        
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
        combo_unidad = ttk.Combobox(row_frame, state='readonly', values=["unidades", "kilos"])
        combo_unidad.pack(side=tk.LEFT, fill=tk.X, expand=True)
        combo_unidad.set("unidades")  # Valor por defecto
        entries['unidad'] = combo_unidad
        
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
                codigo = entries['codigo'].get().strip()
                nombre = entries['nombre'].get().strip()
                categoria = entries['categoria'].get().strip()
                unidad = entries['unidad'].get().strip().lower()
                
                if not codigo or not nombre or not categoria:
                    messagebox.showwarning("Error", "Todos los campos de texto son obligatorios")
                    return

                if unidad not in ['unidades', 'kilos']:
                    messagebox.showwarning("Error", "La unidad debe ser 'unidades' o 'kilos'")
                    return

                precio = int(entries['precio'].get())
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo")

                stock = float(entries['stock'].get())
                if stock < 0:
                    raise ValueError("El stock no puede ser negativo")
                if unidad == 'unidades' and not stock.is_integer():
                    messagebox.showerror("Error", "Para 'unidades', el stock debe ser un número entero")
                    return

                stock_min = float(entries['stock_minimo'].get())
                if stock_min < 0:
                    raise ValueError("El stock mínimo no puede ser negativo")
                if unidad == 'unidades' and not stock_min.is_integer():
                    messagebox.showerror("Error", "Para 'unidades', el stock mínimo debe ser entero")
                    return

                p = Producto(codigo, nombre, precio, stock, categoria, unidad, stock_min)
                
                if self.controller.agregar_producto(p):
                    messagebox.showinfo("Éxito", "Producto agregado correctamente")
                    cancelar()
                    self.cargar_inventario_admin()
                else:
                    messagebox.showerror("Error", "El código ya existe")
            except ValueError as e:
                messagebox.showerror("Error", f"Valores inválidos: {str(e)}")
        
        def cancelar():
            form_frame.destroy()
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
        
        # Ocultar la tabla temporalmente
        self.tree_inv.pack_forget()
        
        # Crear frame para el formulario
        form_frame = ttk.Frame(self.tab_inventario)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text=f"🔄 Actualizar Stock", font=('Helvetica', 14, 'bold')).pack(pady=10)
        ttk.Label(form_frame, text=f"Producto: {producto.nombre}", font=('Helvetica', 12)).pack(pady=5)
        ttk.Label(form_frame, text=f"Stock actual: {producto.stock} {producto.unidad}", font=('Helvetica', 10)).pack(pady=5)
        
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
                cant = float(entry_cant.get())
                if cant <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return

                if producto.unidad == 'unidades' and not cant.is_integer():
                    messagebox.showerror("Error", f"El producto se maneja por unidades.\nNo se admiten decimales.")
                    return

                if self.controller.actualizar_stock(codigo, cant, tipo_var.get()):
                    prod = self.controller.productos[codigo]
                    if prod.tiene_stock_bajo():
                        messagebox.showwarning("⚠️ Alerta de Stock", f"El producto '{prod.nombre}' tiene stock bajo: {prod.stock} {prod.unidad}")
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

class LoginWindow:
    def __init__(self, root, controller: SupermercadoController, on_login_success, on_show_registro):
        self.root = root
        self.controller = controller
        self.on_login_success = on_login_success
        self.on_show_registro = on_show_registro
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.frame, text="🔐 Iniciar Sesión", font=('Helvetica', 16, 'bold')).pack(pady=20)
        
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
        
        ttk.Label(self.frame, text="📝 Nuevo Usuario", font=('Helvetica', 14, 'bold')).pack(pady=20)
        
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
            
        if self.controller.registrar_usuario(user, pwd, 'comprador'):
            messagebox.showinfo("Éxito", "Usuario registrado. Ahora puede iniciar sesión.")
            self.frame.destroy()
            self.on_registro_exitoso()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya existe")
