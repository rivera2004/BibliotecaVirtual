# 📚 BibliotecaVirtual — Sistema de Gestión de Biblioteca Digital

**Universidad Técnica de Machala (UTMACH)**  
**Facultad de Ingeniería Civil — Carrera de Ciencia de Datos e Inteligencia Artificial**  
**Asignatura:** Estructura de Datos  
**Periodo Académico:** Primer Hemisemestre  

---

## 📖 Descripción General del Proyecto

**BibliotecaVirtual** es un sistema integral de gestión bibliotecaria digital desarrollado con un enfoque pedagógico riguroso para la asignatura de **Estructura de Datos**. Permite administrar el catálogo de libros, préstamos, devoluciones con cálculo de moras, atención de reservas y auditoría de operaciones.

El sistema fue diseñado con una **arquitectura dual complementaria**:
1. **Lógica de backend y consola en Python (`biblioteca.py`)**: Implementa desde cero las estructuras dinámicas basadas en nodos, los algoritmos recursivos de ordenamiento, búsqueda y cálculos matemáticos.
2. **Interfaz visual web reactiva en JavaScript (`biblioteca_ui.html`)**: Replica con fidelidad académica las estructuras (`Nodo`, `Pila`, `Cola`) y los algoritmos (`QuickSort`, Búsqueda Binaria, Recursión de Multas) en el lado del cliente con una estética moderna en modo oscuro (*Glassmorphism*).

---

## 🛠️ Tecnologías y Entorno

| Tecnología | Rol en el Proyecto |
|---|---|
| **Python 3.x** | Lógica central del sistema, estructuras lineales enlazadas, recursividad y consola interactiva. |
| **HTML5 / CSS3** | Estructura semántica, diseño visual *Glassmorphism*, paleta oscura y adaptación responsiva. |
| **JavaScript ES6+** | Algoritmos en el cliente, clases dinámicas `Nodo`, `Pila`, `Cola` y reactividad del DOM. |
| **JSON / LocalStorage** | Mecanismos de persistencia en disco y almacenamiento web local. |
| **Markdown** | Documentación técnica y académica estructurada. |

---

## 📂 Archivos Principales del Repositorio

| Archivo | Ubicación | Descripción Técnica |
|---|---|---|
| [`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py) | Raíz del proyecto | Código fuente en Python: clases `Nodo`, `Pila`, `Cola`, recursividad, QuickSort, búsqueda binaria y CLI. |
| [`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html) | Raíz del proyecto | Interfaz gráfica completa en un solo archivo con Dashboard, Catálogo, Préstamos, Cola FIFO e Historial LIFO. |
| [`abrir_interfaz.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/abrir_interfaz.py) | Raíz del proyecto | Lanzador en Python que abre automáticamente `biblioteca_ui.html` en el navegador predeterminado. |
| [`README.md`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/README.md) | Raíz del proyecto | Documentación exhaustiva con detalle teórico, casos de uso y mapa exacto de líneas de código. |

> [!NOTE]  
> **Credenciales de Acceso Administrativo:**  
> - **Usuario:** `admin`  
> - **Contraseña:** `123`  
> *(Definidas en `biblioteca.py` línea 43 y en `biblioteca_ui.html` línea 1109)*.

---

# 🧱 1. Estructuras de Datos Lineales Dinámicas: Pilas y Colas

Ambas estructuras se construyeron sobre el principio de **Nodos Enlazados Dinámicos**, donde cada elemento apunta a su sucesor en memoria mediante punteros (`siguiente`), garantizando inserciones y eliminaciones en tiempo constante $O(1)$.

```
       [ Nodo: dato | siguiente ] ───> [ Nodo: dato | siguiente ] ───> None
```

---

### 1.1. Clase `Nodo`
* **Definición conceptual:** Unidad básica que almacena el `dato` genérico y la referencia `siguiente`.

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**  
  * **Líneas 189–194:** Definición de la clase `Nodo(dato)` con atributos `self.dato` y `self.siguiente = None`.
* **JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):**  
  * **Líneas 1179–1184:** Definición de la clase `class Nodo { constructor(dato) { ... } }`.

---

### 1.2. Pila (`Pila`) — Principio LIFO (*Last In, First Out*)
* **Definición conceptual:** Estructura lineal donde el último elemento insertado en la **cima (*top*)** es el primero en ser retirado.
* **Operaciones implementadas ($O(1)$):**
  * `apilar(elemento)` (*Push*): Inserta un nodo en la cima.
  * `desapilar()` (*Pop*): Extrae y retorna el nodo de la cima.
  * `ver_cima()` (*Peek*): Inspecciona la cima sin extraerla.
  * `esta_vacia()`: Retorna `True` si la cima es `None`.
  * `tamano()`: Retorna el número de elementos.
  * `listar_elementos()`: Recorrido desde la cima hacia la base.
* **Caso de uso en el sistema:** **Historial de Operaciones Recientes y Auditoría**. Cada acción (préstamo, devolución, reserva, desencolado) se apila en la cima, permitiendo visualizar de inmediato las últimas transacciones realizadas y sirviendo de base para funciones de desapilado (*Undo/Deshacer*).

```
        CIMA (TOP) ───> [ Operación 3: Devolución Libro A ]
                        [ Operación 2: Préstamo Libro B    ]
                        [ Operación 1: Préstamo Libro A    ] ───> BASE (None)
```

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**
  * **Líneas 196–244:** Implementación completa de la clase `Pila`.
  * **Línea 656:** Instanciación en el estado global: `"pila_historial": Pila()`.
  * **Líneas 522–527:** Registro de un nuevo préstamo con `datos_sistema["pila_historial"].apilar(...)`.
  * **Líneas 566–571:** Registro de una devolución con `datos_sistema["pila_historial"].apilar(...)`.
  * **Líneas 900–905:** Registro de una reserva en cola de espera con `pila_historial.apilar(...)`.
  * **Líneas 1260–1278:** Función `widget_pila_historial()` que recorre y visualiza la pila en consola.
* **JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):**
  * **Líneas 1186–1226:** Implementación completa de la clase `Pila` en JavaScript (incluyendo método `cargarDesdeArray`).
  * **Línea 1278:** Instanciación global: `const pilaHistorial = new Pila();`.
  * **Líneas 1282 y 1291:** Persistencia de la pila en `localStorage` (`save()` y `load()`).
  * **Líneas 1063–1074:** Maquetación HTML de la vista `view-pila-historial`.
  * **Líneas 1514–1519:** Invocación `pilaHistorial.apilar(...)` al registrar una reserva en cola.
  * **Líneas 1533–1538:** Invocación `pilaHistorial.apilar(...)` al confirmar un préstamo activo.
  * **Líneas 1572–1577:** Invocación `pilaHistorial.apilar(...)` al procesar una devolución.
  * **Líneas 1615–1620:** Invocación `pilaHistorial.apilar(...)` al desencolar un turno.
  * **Líneas 1623–1637:** Función `rPilaHistorial()` que renderiza las tarjetas de la pila mostrando la cima destacada.

---

### 1.3. Cola (`Cola`) — Principio FIFO (*First In, First Out*)
* **Definición conceptual:** Estructura lineal donde el primer elemento que ingresa por el **final (*rear*)** es el primero en ser atendido por el **frente (*front*)**.
* **Operaciones implementadas ($O(1)$):**
  * `encolar(elemento)` (*Enqueue*): Añade un nodo al final manteniendo el puntero `final`.
  * `desencolar()` (*Dequeue*): Retira y devuelve el nodo del frente.
  * `ver_frente()` (*Peek*): Consulta el frente sin extraerlo.
  * `esta_vacia()`: Retorna `True` si el frente es `None`.
  * `tamano()`: Retorna el número de elementos en espera.
  * `listar_elementos()`: Recorrido ordenado desde el frente hacia el final.
* **Caso de uso en el sistema:** **Cola de Reservas y Lista de Espera**. Cuando un estudiante solicita un libro sin ejemplares disponibles (`disponible == False`), su solicitud ingresa automáticamente a la cola FIFO. Al registrarse la devolución del ejemplar, el sistema atiende prioritariamente al primer usuario que estaba en el frente de la fila.

```
FRENTE (FRONT)                                                            FINAL (REAR)
[ Turno #1: Ana Pérez ] ───> [ Turno #2: Carlos Mora ] ───> [ Turno #3: Luis Ortiz ]
```

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**
  * **Líneas 246–301:** Implementación completa de la clase `Cola`.
  * **Línea 657:** Instanciación en el estado global: `"cola_espera": Cola()`.
  * **Líneas 574–578:** En `registrar_devolucion()`, consulta con `ver_frente()` y atiende con `desencolar()`.
  * **Líneas 894–899:** En `seleccionar_libro()`, cuando el libro está prestado, se encola con `cola_espera.encolar(...)`.
  * **Líneas 1237–1258:** Función `widget_cola_espera()` que muestra los turnos ordenados en consola.
* **JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):**
  * **Líneas 1228–1276:** Implementación completa de la clase `Cola` en JavaScript.
  * **Línea 1279:** Instanciación global: `const colaEspera = new Cola();`.
  * **Líneas 1283 y 1292:** Persistencia de la cola en `localStorage`.
  * **Líneas 1035–1061:** Maquetación HTML de la vista `view-cola-espera` con tabla de turnos.
  * **Líneas 1505–1512:** Encolado automático en `confirmarPrestamo()` con `colaEspera.encolar(...)`.
  * **Líneas 1581–1585:** Desencolado automático en `procesarDevolucion()` con `colaEspera.desencolar()`.
  * **Líneas 1592–1607:** Función `rColaEspera()` que renderiza la tabla con badges de `Turno #1 (Frente)`.
  * **Líneas 1609–1621:** Función `desencolarFrenteCola()` para atención manual o anticipada de turnos.

---

# ⚡ 2. Algoritmos de Ordenamiento: QuickSort Recursivo

El sistema utiliza el algoritmo **QuickSort**, fundamentado en la técnica algorítmica de **Divide y Vencerás (*Divide and Conquer*)**. Permite ordenar el catálogo eficientemente y es el prerrequisito indispensable para ejecutar búsquedas binarias.

### 2.1. Fundamento Teórico y Casos
* **Estrategia:**
  1. Se selecciona un elemento pivote (en este proyecto, el elemento central `lista[len // 2]`).
  2. Se particionan los datos en tres sublistas: `menores`, `iguales` y `mayores`.
  3. **Caso Base:** Si la sublista tiene longitud $\le 1$, ya se encuentra ordenada por definición y se retorna directamente.
  4. **Paso Recursivo:** Se ordenan recursivamente las sublistas `menores` y `mayores`, combinándolas:
     $$\text{QuickSort}(\text{menores}) + \text{iguales} + \text{QuickSort}(\text{mayores})$$
* **Complejidad Temporal:**
  * **Caso Promedio:** $O(n \log n)$
  * **Mejor Caso:** $O(n \log n)$
  * **Peor Caso:** $O(n^2)$ (cuando el pivote seleccionado divide el arreglo de forma totalmente desbalanceada).
* **Complejidad Espacial:** $O(\log n)$ en la pila de llamadas de recursión.

---

### 2.2. Ubicación en el Código:

#### En Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):
* **Líneas 142–160:** Función `quicksort_libros_por_titulo(libros)`:
  * Caso base: línea 151 (`if len(libros) <= 1: return libros.copy()`).
  * Pivote y partición: líneas 154–157.
  * Llamada recursiva doble: línea 159.
* **Líneas 162–173:** Función `quicksort_libros_por_categoria(libros)`:
  * Ordenamiento recursivo por categoría bibliográfica.
* **Línea 181:** En `buscar_libro_catalogo()`: ordena la lista antes de invocar la búsqueda binaria.
* **Línea 1000:** En `widget_catalogo()`: ordena el catálogo en pantalla: `libros_ordenados = quicksort_libros_por_titulo(...)`.

#### En JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):
* **Líneas 1153–1174:** Función `quicksortLibros(lista, criterio, asc)`:
  * Caso base: línea 1154 (`if (lista.length <= 1) return [...lista];`).
  * Selección de pivote y partición: líneas 1155–1164.
  * Concatena llamadas recursivas: líneas 1167 y 1169 (soporta orden ascendente y descendente).
* **Líneas 1363–1372:** En `rCatalogo()`: ordena la colección según la selección del usuario (`titulo-az`, `titulo-za`, `categoria`).
* **Línea 1380:** En `rCatalogo()`: genera la lista ordenada previa a la búsqueda binaria interactiva.

---

# 🔍 3. Algoritmos de Búsqueda

Se implementaron dos estrategias de búsqueda según la naturaleza y el orden de los datos:

---

### 3.1. Búsqueda Binaria Recursiva (`busqueda_binaria_libro_recursiva`)
* **Fundamento Teórico:** Reduce a la mitad el espacio de búsqueda en cada paso recursivo dividiendo el segmento entre `inicio` y `fin`.
* **Requisito Indispensable:** La colección debe estar **ordenada previamente** (en nuestro caso, mediante QuickSort).
* **Complejidad Temporal:** $O(\log n)$ frente a $O(n)$ de la búsqueda secuencial.
* **Casos Base:**
  * **Caso Base 1 (No encontrado):** Si `inicio > fin`, el rango se agotó y retorna `None`.
  * **Caso Base 2 (Encontrado):** Si `titulo_medio == busqueda`, retorna la instancia del libro.
* **Paso Recursivo:**
  * Si `busqueda < titulo_medio`: llamada recursiva al subsegmento izquierdo `[inicio, medio - 1]`.
  * Si `busqueda > titulo_medio`: llamada recursiva al subsegmento derecho `[medio + 1, fin]`.

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**
  * **Líneas 104–124:** Implementación de `busqueda_binaria_libro_recursiva(libros, titulo_buscar, inicio, fin)`.
  * **Líneas 175–183:** Función integradora `buscar_libro_catalogo()` (combina QuickSort + Búsqueda Binaria).
  * **Línea 1027:** En `widget_catalogo()`: llamada durante la búsqueda interactiva en consola.
* **JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):**
  * **Líneas 1140–1148:** Implementación de `buscarLibroBinarioRecursivo(librosOrdenados, titulo, inicio, fin)`.
  * **Línea 1381:** En `rCatalogo()`: invocada en tiempo real cuando el usuario teclea en el buscador del catálogo.

---

### 3.2. Búsqueda Lineal Recursiva (`buscar_prestamo_recursivo`)
* **Fundamento Teórico:** Recorre una lista no ordenada evaluando un elemento a la vez mediante llamadas recursivas sucesivas.
* **Complejidad Temporal:** $O(n)$ en el peor caso.
* **Casos Base:**
  * **Caso Base 1 (No encontrado):** Si `indice >= len(prestamos)`, retorna `None`.
  * **Caso Base 2 (Encontrado):** Si `codigo_prestamo == codigo`, retorna el préstamo coincidente.
* **Paso Recursivo:** Llamada con el índice incrementado: `buscar_prestamo_recursivo(prestamos, codigo, indice + 1)`.

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**
  * **Líneas 90–102:** Definición de la función `buscar_prestamo_recursivo(prestamos, codigo, indice = 0)`.
  * **Línea 541:** En `registrar_devolucion()`: localiza el préstamo activo a devolver mediante su código único.

---

# 🔁 4. Algoritmos Recursivos Adicionales

Además del ordenamiento y la búsqueda, la recursividad se aplica directamente a problemas de cálculo acumulativo y procesamiento de colecciones:

---

### 4.1. Cálculo Recursivo de Multas (`calcular_multa_recursiva`)
* **Propósito:** Calcular la sanción económica acumulada por semanas completas o fracciones de retraso en la devolución de un libro.
* **Fórmula conceptual:**
  $$\text{Multa}(d) = \begin{cases} 0.0 & \text{si } d \le 0 \\ \text{tarifa} + \text{Multa}(d - 7) & \text{si } d > 0 \end{cases}$$
* **Caso Base:** Si `dias_retraso <= 0`, retorna `0.0`.
* **Paso Recursivo:** Suma la tarifa semanal y llama recursivamente restando 7 días:  
  `tarifa_por_semana + calcular_multa_recursiva(dias_retraso - 7, tarifa_por_semana)`.

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**
  * **Líneas 79–88:** Implementación de `calcular_multa_recursiva(dias_retraso, tarifa_por_semana)`.
  * **Línea 553:** En `registrar_devolucion()`: calcula la penalización monetaria si la devolución ocurre después de la fecha límite.
* **JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):**
  * **Líneas 1129–1132:** Implementación de `calcularMultaRecursiva(dias, tarifa = MULTA)`.
  * **Línea 1554:** En `rDevolucion()`: calcula la multa proyectada para mostrar en la tarjeta de préstamo con mora.
  * **Línea 1567:** En `procesarDevolucion()`: aplica la multa calculada recursivamente al saldo del estudiante.

---

### 4.2. Conteo Recursivo de Ejemplares Disponibles (`contar_libros_disponibles_recursivo`)
* **Propósito:** Determinar la cantidad exacta de libros listos para préstamo recorriendo la estructura de forma puramente recursiva, sin usar bucles iterativos (`for` o `while`).
* **Caso Base:** Si `indice >= len(libros)`, retorna `0`.
* **Paso Recursivo:** Evalúa el estado del libro actual (`1` si está disponible, `0` si está prestado) y suma el resultado de la llamada al siguiente índice (`indice + 1`):  
  `actual + contar_libros_disponibles_recursivo(libros, indice + 1)`.

#### 📌 Ubicación en el código:
* **Python ([`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py)):**
  * **Líneas 126–136:** Implementación de `contar_libros_disponibles_recursivo(libros, indice = 0)`.
  * **Línea 1001:** En `widget_catalogo()`: calcula el total de disponibles para el encabezado del catálogo.
* **JavaScript ([`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html)):**
  * **Líneas 1134–1138:** Implementación de `contarDisponiblesRecursivo(libros, index = 0)`.
  * **Línea 1345:** En `chips()`: actualiza las insignias superiores de estadísticas del panel administrativo.
  * **Líneas 1393, 1397 y 1398:** En `rCatalogo()`: actualiza el contador dinámico y las tarjetas métricas del catálogo.

---

# 📊 5. Matriz Comparativa y Mapa Completo de Líneas de Código

La siguiente tabla resume y localiza con precisión cada concepto temático dentro del código fuente del proyecto:

| Tema | Componente / Función | Archivo | Líneas de Código | Tipo / Complejidad | Rol en el Sistema |
|---|---|---|---|---|---|
| **Estructuras Lineales** | `Nodo` | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 189–194<br>Líneas 1179–1184 | Nodo Enlazado<br>$O(1)$ | Elemento atómico con puntero `siguiente`. |
| **Pilas (LIFO)** | `Pila` (Clase) | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 196–244<br>Líneas 1186–1226 | Pila Dinámica<br>$O(1)$ Push/Pop | Estructura LIFO con operaciones de cima. |
| **Pilas (LIFO)** | Registro de historial | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 523, 567, 901<br>Líneas 1514, 1533, 1573, 1615 | Apilar transacciones<br>$O(1)$ | Apila préstamos, devoluciones, reservas y desencolados. |
| **Pilas (LIFO)** | Vista de Historial | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 1260–1278<br>Líneas 1063–1074, 1623–1637 | Visualización LIFO | Renderiza la pila mostrando la cima destacada. |
| **Colas (FIFO)** | `Cola` (Clase) | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 246–301<br>Líneas 1228–1276 | Cola Dinámica<br>$O(1)$ Enqueue/Dequeue | Estructura FIFO con punteros frente y final. |
| **Colas (FIFO)** | Encolado de reservas | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 894–899<br>Líneas 1505–1512 | Encolar solicitud<br>$O(1)$ | Entra a la cola cuando un libro está prestado. |
| **Colas (FIFO)** | Desencolado / Atención | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 574–578<br>Líneas 1581–1585, 1609–1621 | Desencolar turno<br>$O(1)$ | Atiende automáticamente al devolver o mediante botón manual. |
| **Colas (FIFO)** | Vista de Cola de Espera | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 1237–1258<br>Líneas 1035–1061, 1592–1607 | Visualización FIFO | Lista ordenada por turnos de llegada (Frente = Turno #1). |
| **Ordenamiento** | `quicksort_libros_por_titulo` | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 142–160<br>Líneas 1153–1174 | QuickSort Recursivo<br>$O(n \log n)$ prom. | Ordena el catálogo alfabéticamente por título. |
| **Ordenamiento** | `quicksort_libros_por_categoria` | `biblioteca.py` | Líneas 162–173 | QuickSort Recursivo<br>$O(n \log n)$ prom. | Ordena el catálogo por categoría bibliográfica. |
| **Búsqueda** | `busqueda_binaria_libro_recursiva` | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 104–124<br>Líneas 1140–1148 | Búsqueda Binaria<br>$O(\log n)$ | Localiza libros en catálogo previamente ordenado. |
| **Búsqueda** | `buscar_libro_catalogo` | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 175–183<br>Líneas 1378–1391 | Integración Orden + Búsqueda | Combina QuickSort previo con Búsqueda Binaria. |
| **Búsqueda** | `buscar_prestamo_recursivo` | `biblioteca.py` | Líneas 90–102 | Búsqueda Lineal<br>$O(n)$ | Localiza préstamos activos por código numérico. |
| **Recursividad** | `calcular_multa_recursiva` | `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 79–88, 553<br>Líneas 1129–1132, 1554, 1567 | Recursión matemática<br>$O(n/7)$ | Acumula tarifas semanales por mora en devoluciones. |
| **Recursividad** | `contar_libros_disponibles_recursivo`| `biblioteca.py`<br>`biblioteca_ui.html` | Líneas 126–136, 1001<br>Líneas 1134–1138, 1345, 1393 | Recorrido recursivo<br>$O(n)$ | Cuenta libros con ejemplar disponible sin bucles. |

---

# 🚀 6. Guía de Ejecución y Pruebas

### 6.1. Ejecución del Backend en Consola (Python)
Para ejecutar la consola interactiva con widgets y menús:
```powershell
python biblioteca.py
```
* **Opciones del menú de consola:**
  * Opción `1`: Registrar préstamo (si el libro está prestado, ingresa a la Cola FIFO).
  * Opción `2`: Registrar devolución (aplica búsqueda lineal recursiva, cálculo de multas y atiende al frente de la cola).
  * Opción `3`: Ver catálogo (aplica QuickSort recursivo y permite Búsqueda Binaria recursiva).
  * Opción `7`: Ver Cola de Reservas (FIFO).
  * Opción `8`: Ver Historial de Operaciones Recientes (Pila LIFO).

---

### 6.2. Ejecución de la Interfaz Gráfica Web
Para lanzar la interfaz web automáticamente en el navegador:
```powershell
python abrir_interfaz.py
```
*(O abrir directamente [`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html) en cualquier navegador moderno)*.

1. **Iniciar sesión:** Usuario `admin`, Contraseña `123`.
2. **Probar QuickSort y Búsqueda Binaria en el Catálogo:**
   * Cambia el selector de ordenamiento entre `Título: A-Z (QuickSort)` y `Categoría (QuickSort)`.
   * Escribe en el buscador el título de un libro (ej. `Clean Code`): el sistema activará la insignia verde `🎯 Búsqueda Binaria O(log n)`.
3. **Probar la Cola de Espera (FIFO) y la Pila (LIFO):**
   * Presta un libro (ej. *Cien años de soledad*).
   * Intenta solicitar ese mismo libro para otro estudiante: el sistema detecta que está prestado y activa el botón **`⏳ Reservar en Cola (Turno #1 - FIFO)`**.
   * Confirma la reserva: el estudiante ingresará a la pestaña **Cola Reservas (FIFO)**.
   * Ve a **Devoluciones** y devuelve el libro: el sistema notificará y atenderá automáticamente al estudiante que estaba en el frente de la cola.
   * Ve a **Historial Pila (LIFO)**: podrás auditar todas las operaciones apiladas en orden cronológico inverso, con la última acción en la cima.

---

## 👨‍🎓 Información Académica

* **Institución:** Universidad Técnica de Machala (UTMACH)
* **Carrera:** Tecnologías de la Información
* **Cátedra:** Estructura de Datos
* **Periodo:** Primer Hemisemestre