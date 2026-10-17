# 📚 BibliotecaVirtual — Sistema de Gestión de Biblioteca Digital

**Universidad Técnica de Machala (UTMACH)**  
**Asignatura:** Estructura de Datos  
**Periodo académico:** Primer Hemisemestre

---

## 📖 Descripción del proyecto

BibliotecaVirtual es un sistema integral de gestión de biblioteca digital diseñado para administrar catálogos bibliográficos, gestionar préstamos y devoluciones, procesar reservas en espera y llevar un historial detallado de transacciones.

El proyecto implementa de manera práctica los conceptos fundamentales de la materia **Estructura de Datos**:
- **Estructuras de Datos Lineales Dinámicas:** Pilas (Stacks - LIFO) y Colas (Queues - FIFO) implementadas mediante Nodos Enlazados.
- **Algoritmos de Ordenamiento:** QuickSort recursivo (por título y por categoría).
- **Algoritmos de Búsqueda:** Búsqueda Binaria recursiva ($O(\log n)$) y Búsqueda Lineal recursiva.
- **Algoritmos Recursivos:** Cálculo acumulativo de multas y conteo de ejemplares disponibles.

Todas las estructuras y algoritmos están construidos desde cero tanto en el backend en **Python** como en la interfaz interactiva web en **JavaScript**.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| **Python 3.x** | Lógica central del sistema, estructuras dinámicas enlazadas y algoritmos de consola. |
| **HTML5 / CSS3** | Estructura y diseño premium con Glassmorphism y modo oscuro. |
| **JavaScript (ES6+)** | Interactividad reactiva, estructuras `Nodo`, `Pila`, `Cola` y algoritmos en el cliente. |
| **Markdown** | Documentación técnica y académica del proyecto. |

---

## 📂 Archivos principales

| Archivo | Descripción |
|---|---|
| [`biblioteca.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca.py) | Lógica del sistema, clases `Nodo`, `Pila`, `Cola`, algoritmos recursivos y widgets interactivos. |
| [`biblioteca_ui.html`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/biblioteca_ui.html) | Dashboard web interactivo con vistas de catálogo, préstamos, cola FIFO e historial LIFO. |
| [`abrir_interfaz.py`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/abrir_interfaz.py) | Script lanzador que abre automáticamente la interfaz web en el navegador predeterminado. |
| [`README.md`](file:///c:/Users/marcos/Desktop/3semestre/estrectutra/1hemi/README.md) | Documentación académica y técnica completa del proyecto. |

---

## 🔐 Credenciales de Acceso Administrativo

El acceso administrativo al panel web o al menú de configuración utiliza:
- **Usuario:** `admin`
- **Contraseña:** `123`

---

# 🧱 Estructuras de Datos Lineales Implementadas

Las estructuras lineales dinámicas se implementaron utilizando **Nodos Enlazados** para garantizar inserciones y eliminaciones en tiempo constante $O(1)$ sin depender de estructuras nativas estáticas.

```
       [Nodo: dato | siguiente] ---> [Nodo: dato | siguiente] ---> None
```

### 1. `Nodo`
- **Atributos:** `dato` (información almacenada) y `siguiente` (puntero al próximo nodo o `None`).

---

### 2. Pila (Stack — LIFO: *Last In, First Out*)

En una **Pila**, el último elemento en ingresar es el primero en salir.

```
       CIMA (TOP) ---> [ Transacción C ]
                       [ Transacción B ]
                       [ Transacción A ] ---> BASE (None)
```

- **Operaciones implementadas:**
  - `apilar(elemento)` (*Push*): Inserta un nuevo nodo en la cima de la pila en tiempo $O(1)$.
  - `desapilar()` (*Pop*): Retira y devuelve el nodo ubicado en la cima en tiempo $O(1)$. Retorna `None` si la pila está vacía.
  - `ver_cima()` (*Peek*): Consulta el dato de la cima sin extraerlo en tiempo $O(1)$.
  - `esta_vacia()`: Retorna `True` si la cima es `None`.
  - `tamano()`: Retorna la cantidad actual de nodos.
  - `listar_elementos()`: Recorre la pila desde la cima hasta la base para visualización.
- **Caso de uso en el sistema:**
  - **Historial de Transacciones Recientes:** Cada préstamo, devolución o reserva se apila en la cima. Permite auditar de inmediato la actividad más reciente y sienta las bases para funciones de desapilado ("Deshacer / Undo").

---

### 3. Cola (Queue — FIFO: *First In, First Out*)

En una **Cola**, el primer elemento en ingresar es el primero en ser atendido.

```
FRENTE (FRONT)                                                    FINAL (REAR)
[ Solicitud 1 ] ---> [ Solicitud 2 ] ---> [ Solicitud 3 ] ---> [ Solicitud 4 ]
```

- **Operaciones implementadas:**
  - `encolar(elemento)` (*Enqueue*): Añade un elemento al final de la cola en tiempo $O(1)$ manteniendo el puntero `final`.
  - `desencolar()` (*Dequeue*): Extrae y retorna el elemento del frente de la cola en tiempo $O(1)$. Si la cola queda vacía, actualiza `final = None`.
  - `ver_frente()` (*Peek*): Consulta el elemento en espera en el frente sin retirarlo en tiempo $O(1)$.
  - `esta_vacia()`: Retorna `True` si `frente` es `None`.
  - `tamano()`: Retorna el número de solicitudes en espera.
  - `listar_elementos()`: Retorna la lista ordenada de solicitudes en espera para renderizado.
- **Caso de uso en el sistema:**
  - **Cola de Espera y Reservas:** Cuando un estudiante solicita un libro que no tiene ejemplares disponibles, su solicitud ingresa automáticamente a la cola FIFO. Tan pronto como otro usuario devuelve un ejemplar del libro, el sistema atiende y desencola automáticamente al primer usuario en espera.

---

# 🔄 Algoritmos Implementados

## ⚡ 1. Algoritmos de ordenamiento

### 1.1. `quicksort_libros_por_titulo(libros)`
- **Técnica:** *Divide y Vencerás* (Divide and Conquer) recursivo.
- **Complejidad:** $O(n \log n)$ promedio, $O(n^2)$ peor caso.
- **Caso base:** Si la lista tiene $\le 1$ elementos, se retorna tal cual.
- **Paso recursivo:** Selecciona un pivote, particiona en `menores`, `iguales` y `mayores`, y concatena:
  $$\text{QuickSort}(\text{menores}) + \text{iguales} + \text{QuickSort}(\text{mayores})$$
- **Uso:** Ordena el catálogo alfabéticamente para visualización y como requisito previo para la búsqueda binaria.

### 1.2. `quicksort_libros_por_categoria(libros)`
- Aplica el principio de QuickSort organizando los libros por género/categoría bibliográfica de forma recursiva.

---

## 🔍 2. Algoritmos de búsqueda

### 2.1. `busqueda_binaria_libro_recursiva(libros, titulo_buscar, inicio, fin)`
- **Complejidad:** $O(\log n)$.
- **Requisito:** Catálogo ordenado alfabéticamente previamente.
- **Caso base 1:** Si `inicio > fin`, el libro no existe en el catálogo (retorna `None`).
- **Caso base 2:** Si el libro en `medio = (inicio + fin) // 2` coincide con el título buscado, retorna la instancia del libro.
- **Paso recursivo:** Si el título buscado es alfabéticamente menor, busca en el subsegmento izquierdo `[inicio, medio - 1]`; si es mayor, busca en el derecho `[medio + 1, fin]`.

### 2.2. `buscar_libro_catalogo(libros, titulo_buscar)`
- Orquesta el ordenamiento QuickSort y la búsqueda binaria recursiva en una sola operación optimizada.

### 2.3. `buscar_prestamo_recursivo(prestamos, codigo, indice)`
- Búsqueda lineal recursiva con paso `indice + 1` y casos base de fin de lista o coincidencia de código de préstamo.

---

## 🔁 3. Algoritmos recursivos adicionales

### 3.1. `calcular_multa_recursiva(dias_retraso, tarifa_por_semana)`
- Calcula la sanción acumulada sumando la tarifa por cada período de retraso de forma recursiva.
- **Caso base:** Si `dias_retraso <= 0`, retorna `0.0`.
- **Paso recursivo:** `tarifa_por_semana + calcular_multa_recursiva(dias_retraso - 7, tarifa_por_semana)`.

### 3.2. `contar_libros_disponibles_recursivo(libros, indice)`
- Recorre la lista de libros de forma recursiva sumando `1` si el libro está disponible o `0` si está agotado.
- **Caso base:** Si `indice >= len(libros)`, retorna `0`.

---

## 🌐 4. Implementación en la Interfaz Web (`biblioteca_ui.html`)

La interfaz web en JavaScript implementa exactamente las mismas estructuras y algoritmos en el lado del cliente:

1. **Clases JS:** `Nodo`, `Pila` y `Cola` gestionan el estado reactivo del navegador.
2. **Cola de Reservas (FIFO):** Muestra tarjetas interactivas de usuarios en espera y botón para desencolar o procesar turnos.
3. **Historial de Operaciones (LIFO):** Muestra la pila con badges de tiempo y detalles de cada acción reciente.
4. **Buscador Reactivo:** Selector entre ordenamiento QuickSort (A-Z, Z-A, Categoría) y barra de búsqueda binaria recursiva en tiempo real.
5. **Autoevaluación de Disponibilidad:** Al presionar "Prestar" en un libro con 0 ejemplares, el sistema ofrece registrar al usuario automáticamente en la cola de reservas. Al registrar una devolución, atiende automáticamente al primer reservante.

---

## 📊 5. Matriz Comparativa de Estructuras y Algoritmos

| Componente | Tipo | Complejidad Temporal | Aplicación Práctica en el Sistema |
|---|---|---|---|
| `Nodo` | Estructura Enlazada | $O(1)$ | Bloque constructor fundamental de Pilas y Colas. |
| `Pila` (LIFO) | Estructura Lineal | $O(1)$ en Push / Pop | Historial y auditoría de transacciones recientes. |
| `Cola` (FIFO) | Estructura Lineal | $O(1)$ en Enqueue / Dequeue | Lista de espera y reservas de libros agotados. |
| `quicksort_libros` | Ordenamiento Recursivo | $O(n \log n)$ prom. | Ordenación del catálogo por título o categoría. |
| `busqueda_binaria` | Búsqueda Recursiva | $O(\log n)$ | Localización ultrarrápida de títulos en el catálogo. |
| `calcular_multa` | Recursividad Matemática | $O(n/7)$ | Cálculo acumulado de recargos por mora. |
| `contar_disponibles`| Recorrido Recursivo | $O(n)$ | Conteo de inventario disponible en catálogo. |

---

## 🎯 6. Conclusión y Aprendizajes

El sistema **BibliotecaVirtual** ejemplifica con rigor académico la transición desde la teoría de **Estructura de Datos** hacia una aplicación interactiva funcional:
1. **Modularidad y Abstracción:** Las estructuras dinámicas (`Pila` y `Cola`) encapsulan sus punteros internos y exponen interfaces limpias (`apilar`, `desapilar`, `encolar`, `desencolar`).
2. **Eficiencia Algorítmica:** La combinación de QuickSort con Búsqueda Binaria optimiza drásticamente la búsqueda de libros frente a recorridos secuenciales tradicionales.
3. **Consistencia Dual (Python & JavaScript):** Garantiza que tanto la ejecución por consola como la experiencia visual en el navegador mantengan la misma lógica y eficiencia en estructuras de datos.