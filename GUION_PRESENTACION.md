# Guion de Presentación: Sistema de Gestión de Minimarket
**Duración Estimada:** 20 Minutos
**Integrantes:** Martin, Juan, Ignacio, Diego

---

## Introducción y Objetivos (Speaker 1: Martin)
**(Tiempo estimado: 5 minutos)**

**Diapositiva 1: Título**
*   **Martin:** "Buenos días profesor y compañeros. Nosotros somos el grupo compuesto por Juan Aguilar, Ignacio Iturra, Diego Dominguez y quien les habla, Martin Rodriguez. Hoy vamos a presentar nuestro proyecto final de Programación Orientada a Objetos: el 'Sistema de Gestión de Minimarket'."

**Diapositiva 2: Contenido**
*   **Martin:** "Esta es la agenda que seguiremos hoy. Comenzaremos con la introducción y la problemática, pasaremos por los objetivos, luego profundizaremos en la parte técnica y arquitectónica, revisaremos la implementación del código y finalizaremos con las funcionalidades y conclusiones."

**Diapositiva 3: Introducción (Contexto y Problema)**
*   **Martin:** "Para entender por qué desarrollamos este software, primero debemos mirar el contexto. Muchos pequeños negocios, como los minimarkets de barrio, todavía operan de manera muy análoga. Dependen de cuadernos, calculadoras manuales y la memoria del dueño."
*   **Martin:** "Esto genera problemas graves: errores en el cálculo del stock (nunca saben realmente cuánto tienen), pérdidas financieras 'hormiga' que no se detectan, y una atención lenta al cliente porque hay que sumar todo a mano. Nuestro proyecto nace como una respuesta a esta necesidad de modernización accesible."

**Diapositiva 4: Solución Propuesta**
*   **Martin:** "Nuestra solución es un sistema de escritorio robusto pero ligero, desarrollado en Python. No buscamos competir con grandes ERPs como SAP, sino ofrecer una herramienta a medida para el pequeño comerciante. El sistema automatiza el descuento de inventario, calcula totales exactos y genera un historial de ventas confiable."

**Diapositiva 5: Objetivos**
*   **Martin:** "Nuestro Objetivo General fue desarrollar este sistema de información integral. Pero para lograrlo, nos planteamos objetivos específicos técnicos muy claros:"
*   **Martin:** "Primero, y lo más importante para esta asignatura, fue implementar estrictamente el patrón **MVC (Modelo-Vista-Controlador)**. No queríamos código espagueti; queríamos una arquitectura limpia."
*   **Martin:** "Segundo, diseñar una interfaz gráfica (GUI) con **Tkinter** que fuera amigable para personas no tecnológicas."
*   **Martin:** "Y tercero, asegurar la persistencia de datos de forma organizada, para lo cual elegimos trabajar con archivos **JSON**, separando productos, ventas y usuarios."

---

## Fundamentación Técnica y Arquitectura (Speaker 2: Juan)
**(Tiempo estimado: 5 minutos)**

**Diapositiva 6: Fundamentación Técnica**
*   **Juan:** "Gracias Martin. Ahora, profundicemos en cómo construimos esto. Elegimos **Python 3.14** como lenguaje base por su claridad y potencia. Para la interfaz, usamos **Tkinter**, que es la librería estándar de GUI en Python, lo que facilita la portabilidad sin instalar dependencias pesadas."
*   **Juan:** "En cuanto a los Patrones de Diseño, el núcleo es **MVC**. Separamos totalmente la lógica de negocio de la interfaz visual. Además, implementamos el patrón **Facade** en nuestro `SupermercadoController`. Este controlador actúa como una 'fachada' que simplifica la comunicación entre la vista y los sub-controladores más complejos que manejan la lógica interna."

**Diapositiva 7: Arquitectura del Sistema (Diagrama de Clases)**
*   **Juan:** "Aquí pueden ver nuestro Diagrama de Clases, que es el mapa de nuestro sistema. (Señalar el diagrama en la pantalla)."
*   **Juan:** "En la capa del **Modelo**, tenemos clases como `Producto`, `Venta` y `Usuario`. Noten que `Producto` no es una clase plana; utiliza **Composición** con las clases `Categoria` y `Unidad`. Esto es POO puro: un producto *tiene* una categoría, no *es* una categoría."
*   **Juan:** "En la capa de **Controladores**, verán que dividimos la lógica. Tenemos un `ProductoController` para el inventario, un `VentaController` para las transacciones y un `UsuarioController` para la autenticación. El `SupermercadoController` orquesta todo esto."

**Diapositiva 8: Estructura del Proyecto**
*   **Juan:** "Esta arquitectura se refleja directamente en nuestras carpetas. No tenemos todos los archivos mezclados.
    *   `models/`: Contiene la definición de nuestros objetos.
    *   `views/`: Contiene toda la lógica de Tkinter.
    *   `controllers/`: Contiene la inteligencia del sistema.
    *   `data/`: Es nuestra 'base de datos' basada en archivos JSON.
    *   Esta estructura nos permitió trabajar en paralelo sin pisarnos el código unos a otros."

---

## Implementación y Algoritmos (Speaker 3: Ignacio)
**(Tiempo estimado: 5 minutos)**

**Diapositiva 9: Implementación - Modelo Producto**
*   **Ignacio:** "Continuando con la implementación, quiero destacar cómo aplicamos la POO en el código. Aquí vemos la clase `Producto`. En el constructor `__init__`, pueden ver la composición que mencionaba Juan."
*   **Ignacio:** "Recibimos objetos de tipo `Categoria` y `Unidad`. Esto es crucial porque nos permite escalar. Si mañana la `Categoria` necesita tener una descripción o un código propio, solo modificamos la clase `Categoria` y el `Producto` se adapta automáticamente. Además, el método `to_dict` es fundamental para serializar nuestros objetos a JSON."

**Diapositiva 10: Algoritmos de Generación Automática**
*   **Ignacio:** "Uno de los desafíos lógicos fue la generación de identificadores únicos. Implementamos algoritmos de autoincremento tanto para las **Ventas** como para los **Productos**."
*   **Ignacio:** "En `ProductoController`, el método `generar_codigo` escanea los códigos existentes (como '001', '002') y genera el siguiente automáticamente. Esto evita que el usuario tenga que inventar códigos y previene duplicados. Lo mismo aplicamos para los IDs de las boletas en `VentaController`, asegurando una numeración correlativa y consistente incluso al reiniciar el programa."

**Diapositiva 11: Lógica de Venta y Validaciones**
*   **Ignacio:** "El corazón del sistema es el método `realizar_venta`. Este método es transaccional. Recibe una lista de items y hace tres cosas críticas:"
    1.  "Genera el nuevo ID."
    2.  "Itera sobre los productos y descuenta el stock en tiempo real."
    3.  "Guarda la venta en el archivo JSON inmediatamente."
*   **Ignacio:** "Además, hemos blindado el sistema con validaciones estrictas en los controladores. Por ejemplo, en `UsuarioController`, utilizamos métodos de cadena y validaciones lógicas para impedir espacios en los nombres de usuario o caracteres especiales no permitidos, asegurando la integridad de los datos antes de que lleguen al archivo JSON."

---

## Funcionalidades y Conclusión (Speaker 4: Diego)
**(Tiempo estimado: 5 minutos)**

**Diapositiva 12: Funcionalidades Clave**
*   **Diego:** "Para el usuario final, toda esa lógica se traduce en funcionalidades concretas. El sistema cuenta con:"
    *   **Control de Acceso:** Tenemos roles diferenciados. Un vendedor no puede borrar productos ni crear administradores; solo un Admin puede hacerlo.
    *   **Gestión de Inventario:** Permite crear, editar y eliminar productos, con soporte para **unidades y gramos**.
    *   **Integridad de Datos:** El sistema valida automáticamente que los stocks sean números enteros cuando corresponde y bloquea entradas inválidas en el registro de usuarios.
    *   **Punto de Venta (POS):** Es la pantalla principal de venta. Es rápida, permite buscar por nombre y calcula el total automáticamente.
    *   **Administración:** Agregamos una función para crear nuevos administradores desde la misma interfaz, algo que facilita la autogestión del negocio."

**Diapositiva 13: Conclusiones**
*   **Diego:** "Para concluir nuestro trabajo, podemos afirmar que el uso del patrón MVC fue determinante. Al principio nos costó separar la lógica de la vista, pero a largo plazo hizo que el código fuera mucho más ordenado y fácil de corregir."
*   **Diego:** "Logramos un sistema funcional que cumple con los requerimientos de un minimarket real: persistencia de datos, validaciones de stock y reportes claros."

**Diapositiva 14: Trabajo Futuro**
*   **Diego:** "Sin embargo, sabemos que siempre se puede mejorar. Como trabajo futuro, el paso natural sería migrar de archivos JSON a una base de datos real como **SQLite o PostgreSQL** para manejar miles de productos con mayor eficiencia."
*   **Diego:** "También nos gustaría implementar gráficos visuales con `matplotlib` para que el dueño vea sus ventas en barras o tortas, y agregar soporte para lectores de código de barras físicos."

**Diapositiva 15: Cierre**
*   **Diego:** "Con esto damos por finalizada nuestra presentación. El código fuente está disponible y documentado. Muchas gracias por su atención y quedamos atentos a sus preguntas."

---
