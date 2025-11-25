# 📦 Guía para Subir el Proyecto a GitHub

## Opción 1: Sin instalar Git (Más Fácil) 🌐

### Usando la Interfaz Web de GitHub

1. **Crear una cuenta en GitHub** (si no tienes)
   - Ve a https://github.com
   - Haz clic en "Sign up"
   - Completa el registro

2. **Crear un nuevo repositorio**
   - Una vez logueado, haz clic en el botón "+" (arriba a la derecha)
   - Selecciona "New repository"
   - Configura:
     - **Repository name**: `sistema-supermercado-poo`
     - **Description**: `Sistema de administración de supermercado con Python, Tkinter y arquitectura MVC`
     - **Public/Private**: Elige según prefieras
     - ⚠️ **NO marques** "Initialize this repository with a README"
   - Haz clic en "Create repository"

3. **Subir archivos**
   - En la página del nuevo repositorio, verás "uploading an existing file"
   - Haz clic en ese enlace
   - **Arrastra todos los archivos y carpetas** de tu proyecto
   - O haz clic en "choose your files" y selecciónalos
   - **IMPORTANTE**: GitHub web no permite subir carpetas vacías, así que:
     - Comprime el proyecto en un .zip primero, O
     - Sube los archivos de forma manual manteniendo la estructura

4. **Commit inicial**
   - En el cuadro de texto escribe: `Initial commit - Sistema POO Supermercado`
   - Haz clic en "Commit changes"

### ✅ Ventajas:
- No necesitas instalar nada
- Proceso visual e intuitivo
- Funciona desde cualquier navegador

### ❌ Desventajas:
- Más lento para proyectos grandes
- No tienes control de versiones local
- Difícil mantener la estructura de carpetas

---

## Opción 2: Instalando Git (Recomendado) 💻

### Paso 1: Instalar Git

1. **Descargar Git**
   - Ve a https://git-scm.com/download/win
   - Descarga el instalador para Windows
   - Ejecuta el instalador (.exe)

2. **Instalar Git**
   - Acepta todas las opciones por defecto
   - En "Choosing the default editor", puedes elegir tu editor preferido
   - **Importante**: Marca "Git from the command line and also from 3rd-party software"
   - Continúa con "Next" hasta finalizar

3. **Verificar instalación**
   - Abre una nueva terminal PowerShell
   - Ejecuta: `git --version`
   - Deberías ver algo como: `git version 2.43.0`

### Paso 2: Configurar Git (Primera vez)

Abre PowerShell y ejecuta:

```powershell
# Configura tu nombre (aparecerá en los commits)
git config --global user.name "Tu Nombre"

# Configura tu email (debe ser el mismo de GitHub)
git config --global user.email "tu-email@ejemplo.com"

# Verifica la configuración
git config --list
```

### Paso 3: Inicializar el Repositorio Local

```powershell
# Navega a la carpeta del proyecto
cd c:\Users\TheMa\OneDrive\Desktop\proyecto_poo_v2-main

# Inicializa Git
git init

# Verifica el estado
git status
```

### Paso 4: Preparar los Archivos

```powershell
# Agregar todos los archivos al staging area
git add .

# Verificar qué se agregó
git status

# Hacer el primer commit
git commit -m "Initial commit - Sistema de Supermercado con POO"
```

### Paso 5: Crear Repositorio en GitHub

1. Ve a https://github.com y haz login
2. Haz clic en "+" → "New repository"
3. Configuración:
   - **Name**: `sistema-supermercado-poo`
   - **Description**: `Sistema de administración de supermercado desarrollado con Python, Tkinter y arquitectura MVC`
   - **Public/Private**: Elige según prefieras
   - ⚠️ **NO marques** "Initialize this repository with..."
4. Haz clic en "Create repository"

### Paso 6: Conectar y Subir

GitHub te mostrará comandos. Copia tu URL del repositorio y ejecuta:

```powershell
# Agregar el repositorio remoto (reemplaza con TU URL)
git remote add origin https://github.com/TU-USUARIO/sistema-supermercado-poo.git

# Renombrar la rama principal a 'main'
git branch -M main

# Subir el código
git push -u origin main
```

### ✅ Listo!
Tu proyecto ahora está en GitHub. La URL será algo como:
`https://github.com/TU-USUARIO/sistema-supermercado-poo`

---

## 🔐 Opción 3: GitHub Desktop (Para principiantes)

Si prefieres una interfaz gráfica:

### Paso 1: Instalar GitHub Desktop

1. Ve a https://desktop.github.com/
2. Descarga e instala GitHub Desktop
3. Abre la aplicación y haz login con tu cuenta de GitHub

### Paso 2: Agregar el Proyecto

1. **File** → **Add local repository**
2. Selecciona la carpeta: `c:\Users\TheMa\OneDrive\Desktop\proyecto_poo_v2-main`
3. Si dice "This directory does not appear to be a Git repository":
   - Haz clic en "create a repository"
   - O usa **File** → **New repository** y selecciona la carpeta existente

### Paso 3: Primer Commit

1. Verás todos los archivos en la ventana izquierda
2. En "Summary" escribe: `Initial commit - Sistema POO Supermercado`
3. Haz clic en "Commit to main"

### Paso 4: Publicar en GitHub

1. Haz clic en "Publish repository"
2. Configura:
   - **Name**: `sistema-supermercado-poo`
   - **Description**: `Sistema de administración de supermercado con POO`
   - Elige Public o Private
3. Haz clic en "Publish repository"

### ✅ Ventajas:
- Interfaz gráfica intuitiva
- Fácil de usar
- Control de versiones visual
- No necesitas comandos

---

## 📝 Contenido del .gitignore (Ya incluido)

Tu proyecto ya tiene un archivo `.gitignore`. Verifica que contenga:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
```

---

## 🚀 Comandos Git Útiles (Para el futuro)

Una vez que tengas Git instalado:

```powershell
# Ver estado de los archivos
git status

# Agregar cambios
git add .                    # Agregar todos
git add archivo.py           # Agregar un archivo específico

# Hacer commit
git commit -m "Descripción del cambio"

# Ver historial
git log
git log --oneline           # Versión compacta

# Subir cambios
git push

# Descargar cambios (si trabajas en varios equipos)
git pull

# Ver diferencias
git diff

# Ver ramas
git branch

# Crear nueva rama
git branch nombre-rama
git checkout nombre-rama

# O crear y cambiar en un comando
git checkout -b nombre-rama

# Volver a rama principal
git checkout main
```

---

## 📋 Workflow Recomendado

Para futuras actualizaciones:

```powershell
# 1. Modificar archivos en tu editor
# 2. Ver qué cambió
git status

# 3. Agregar cambios
git add .

# 4. Hacer commit con mensaje descriptivo
git commit -m "Agregado sistema de descuentos"

# 5. Subir a GitHub
git push
```

---

## 🎯 Descripción Sugerida para GitHub

Cuando crees el repositorio, usa esta descripción:

```
Sistema de Administración de Supermercado

Sistema completo desarrollado con Python y Tkinter siguiendo principios de 
Programación Orientada a Objetos (POO) y arquitectura Modelo-Vista-Controlador (MVC).

Características:
✅ Gestión de inventario con alertas de stock
✅ Sistema de ventas con carrito de compras
✅ Autenticación de usuarios (Admin/Comprador)
✅ Reportes y estadísticas en tiempo real
✅ Precios en pesos chilenos (CLP)
✅ Interfaz gráfica moderna con Tkinter

Tecnologías: Python 3.7+, Tkinter, JSON
Arquitectura: MVC (Model-View-Controller)
```

---

## 🏷️ Topics/Tags Sugeridos para GitHub

Cuando estés en la página del repositorio, agrega estos topics:

```
python
tkinter
poo
oop
mvc
inventory-management
pos-system
point-of-sale
python3
gui
desktop-app
chilean-pesos
stock-management
```

Para agregar topics:
1. Ve a tu repositorio en GitHub
2. Haz clic en el ícono de engranaje ⚙️ junto a "About"
3. En "Topics" agrega los tags separados por espacios
4. Guarda

---

## 📄 README.md para GitHub

Tu proyecto ya tiene un `README.md`. Para hacerlo más atractivo en GitHub, 
considera agregar badges al inicio:

```markdown
# Sistema de Administración de Supermercado

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

[Resto del README actual...]
```

---

## ❓ Problemas Comunes

### "Git no se reconoce como comando"
**Solución**: Reinicia PowerShell después de instalar Git

### "Permission denied (publickey)"
**Solución**: Configura SSH keys o usa HTTPS con usuario/contraseña

### "Failed to push some refs"
**Solución**: Primero haz `git pull` y luego `git push`

### OneDrive sincronizando constantemente
**Solución**: 
1. Mueve el proyecto fuera de OneDrive
2. O excluye la carpeta `.git` de la sincronización

---

## 🎓 Recursos Adicionales

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Learn Git Branching**: https://learngitbranching.js.org/

---

## ✅ Checklist Final

Antes de subir a GitHub:

- [ ] Eliminar información sensible (contraseñas, API keys)
- [ ] Verificar que `.gitignore` funciona correctamente
- [ ] Probar que el proyecto funciona
- [ ] README.md actualizado
- [ ] Licencia agregada (si es necesario)
- [ ] Commits con mensajes descriptivos

---

**¿Necesitas ayuda?** Cuéntame qué opción prefieres y te guío paso a paso! 🚀
