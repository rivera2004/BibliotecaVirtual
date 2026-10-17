# 📚 BibliotecaVirtual — Sistema de Gestión de Biblioteca Digital

**Universidad Técnica de Machala (UTMACH)**  
**Asignatura:** Estructura de Datos  
**Periodo académico:** Primer Hemisemestre

---

## 📖 Descripción del proyecto

BibliotecaVirtual es un sistema de gestión de biblioteca digital diseñado para administrar el catálogo de libros, gestionar préstamos y devoluciones, calcular multas, registrar reservas en espera y mantener un historial de las operaciones realizadas.

El proyecto aplica conceptos fundamentales de **Estructura de Datos**, mediante la implementación de estructuras dinámicas enlazadas y algoritmos de ordenamiento, búsqueda y recursividad.

Sus principales funcionalidades son:

- 📚 Administración y consulta del catálogo de libros.
- 🔍 Búsqueda de libros por título.
- 🔃 Ordenamiento por título y categoría.
- 📖 Registro y gestión de préstamos y devoluciones.
- 💰 Cálculo recursivo de multas por retraso.
- ⏳ Gestión de reservas mediante una cola de espera FIFO.
- 📋 Historial de transacciones mediante una pila LIFO.
- 📊 Consulta y actualización de la disponibilidad de ejemplares.

Las estructuras de datos y los algoritmos se implementan tanto en el backend con Python como en la interfaz web con JavaScript.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python 3.x | Lógica central del sistema, estructuras dinámicas y algoritmos. |
| HTML5 | Estructura de la interfaz web. |
| CSS3 | Diseño visual, modo oscuro y efectos de interfaz. |
| JavaScript ES6+ | Interactividad, estructuras enlazadas y algoritmos en el navegador. |
| Markdown | Documentación técnica y académica. |

---

## 📂 Archivos principales

| Archivo | Descripción |
|---|---|
| `biblioteca.py` | Lógica del sistema, clases `Nodo`, `Pila` y `Cola`, algoritmos recursivos y operaciones de biblioteca. |
| `biblioteca_ui.html` | Interfaz web interactiva con catálogo, préstamos, reservas, historial y estadísticas. |
| `abrir_interfaz.py` | Script encargado de abrir la interfaz web en el navegador predeterminado. |
| `README.md` | Documentación técnica y académica del proyecto. |

---

# 🧱 1. Estructuras de datos lineales dinámicas

Las estructuras lineales permiten organizar y administrar información siguiendo un orden determinado. En este proyecto se implementan mediante **nodos enlazados**, construidos desde cero, en lugar de depender exclusivamente de las estructuras nativas de Python o JavaScript.

## 1.1. Nodo (`Nodo`)

El nodo es el componente básico de las estructuras enlazadas. Almacena un dato y una referencia al siguiente nodo.

Cada nodo contiene:

- `dato`: información almacenada.
- `siguiente`: referencia al próximo nodo o `None` cuando no existe otro.

Representación de una lista enlazada:

```text
[Nodo: dato | siguiente] → [Nodo: dato | siguiente] → None
```

Los nodos permiten construir estructuras dinámicas cuyo tamaño puede cambiar durante la ejecución.

## 1.2. Pila (`Pila`) — LIFO

Una pila sigue el principio **LIFO (Last In, First Out)**: el último elemento en entrar es el primero en salir.

Representación:

```text
        CIMA (TOP)
             ↓
      [Transacción C]
      [Transacción B]
      [Transacción A]
             ↓
        BASE (None)
```

### Operaciones implementadas

| Operación | Método | Función |
|---|---|---|
| Insertar | `apilar(elemento)` | Agrega un elemento en la cima. |
| Extraer | `desapilar()` | Retira y devuelve el elemento de la cima. |
| Consultar | `ver_cima()` | Consulta el elemento superior sin retirarlo. |
| Verificar | `esta_vacia()` | Comprueba si la pila está vacía. |
| Contar | `tamano()` | Devuelve la cantidad de elementos. |
| Recorrer | `listar_elementos()` | Obtiene los elementos para su visualización. |

Las operaciones de inserción y extracción en la cima tienen una complejidad temporal de \(O(1)\).

### Aplicación en BibliotecaVirtual

La pila almacena el historial de transacciones recientes, como préstamos, devoluciones y reservas. Esto permite consultar primero las operaciones más recientes y visualizar la actividad del sistema.

## 1.3. Cola (`Cola`) — FIFO

Una cola sigue el principio **FIFO (First In, First Out)**: el primer elemento en entrar es el primero en salir.

Representación:

```text
FRENTE                                      FINAL
   ↓                                           ↓
[Solicitud 1] → [Solicitud 2] → [Solicitud 3]
```

### Operaciones implementadas

| Operación | Método | Función |
|---|---|---|
| Insertar | `encolar(elemento)` | Agrega una solicitud al final. |
| Extraer | `desencolar()` | Retira y devuelve la primera solicitud. |
| Consultar | `ver_frente()` | Consulta la primera solicitud sin retirarla. |
| Verificar | `esta_vacia()` | Comprueba si la cola está vacía. |
| Contar | `tamano()` | Devuelve el número de solicitudes. |
| Recorrer | `listar_elementos()` | Obtiene las solicitudes para su visualización. |

Las operaciones de inserción y extracción tienen una complejidad temporal de \(O(1)\) cuando se mantienen las referencias al frente y al final de la cola.

### Aplicación en BibliotecaVirtual

La cola administra las reservas de libros que no tienen ejemplares disponibles. Cuando un libro se devuelve, el sistema puede atender al primer usuario en espera y retirar su solicitud de la cola.

---

# ⚡ 2. Algoritmos de ordenamiento

Los algoritmos de ordenamiento permiten organizar los libros según distintos criterios, facilitando su consulta y preparando los datos para la búsqueda binaria.

## 2.1. `quicksort_libros_por_titulo(libros)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 141

Ordena los libros alfabéticamente por título mediante el algoritmo **QuickSort**, basado en la técnica *Divide y Vencerás* (*Divide and Conquer*).

- **Estrategia:** selecciona un pivote y divide los elementos en menores, iguales y mayores.
- **Caso base:** si la lista tiene cero o un elemento, ya está ordenada.
- **Paso recursivo:** ordena las sublistas menores y mayores, y las combina con los elementos iguales.
- **Uso:** organiza el catálogo y permite preparar los datos para la búsqueda binaria.

### Complejidad

| Caso | Complejidad temporal |
|---|---:|
| Promedio | \(O(n \log n)\) |
| Peor caso | \(O(n^2)\) |

El consumo de memoria depende de la implementación. Si se crean sublistas, puede ser mayor que el de una versión que ordena directamente sobre la lista original.

## 2.2. `quicksort_libros_por_categoria(libros)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 162

Ordena los libros por categoría mediante el mismo principio recursivo de QuickSort.

- **Objetivo:** organizar el catálogo por género o categoría bibliográfica.
- **Funcionamiento:** divide los elementos según el criterio de comparación y ordena recursivamente las sublistas.
- **Uso:** facilita la organización y consulta del catálogo.

---

# 🔍 3. Algoritmos de búsqueda

## 3.1. `busqueda_binaria_libro_recursiva(libros, titulo_buscar, inicio, fin)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 104

Busca un libro por su título reduciendo a la mitad el espacio de búsqueda en cada llamada recursiva.

**Requisito:** la lista debe estar ordenada previamente según el mismo criterio de comparación utilizado en la búsqueda.

### Funcionamiento

1. Calcula la posición central de la lista.
2. Compara el título central con el título buscado.
3. Si coincide, devuelve el libro.
4. Si el título buscado es menor, continúa por la mitad izquierda.
5. Si es mayor, continúa por la mitad derecha.
6. Si el intervalo queda vacío, devuelve `None`.

### Casos base

- **Libro no encontrado:** si `inicio > fin`, retorna `None`.
- **Libro encontrado:** si el título del elemento central coincide, retorna el libro.

### Complejidad

- **Temporal:** \(O(\log n)\) en el caso habitual de una búsqueda binaria sobre una lista ordenada.
- **Espacial:** \(O(\log n)\) para la pila de llamadas recursivas en el caso habitual.

## 3.2. `buscar_libro_catalogo(libros, titulo_buscar)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 175

Integra el ordenamiento QuickSort y la búsqueda binaria en una sola operación.

1. Ordena los libros utilizando QuickSort.
2. Ejecuta la búsqueda binaria sobre el catálogo ordenado.
3. Devuelve el libro encontrado o el resultado de búsqueda correspondiente.

**Complejidad promedio:** \(O(n \log n)\) cuando se ordena todo el catálogo antes de buscar. El costo total queda dominado por el ordenamiento.

## 3.3. `buscar_prestamo_recursivo(prestamos, codigo, indice)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 90

Realiza una búsqueda lineal recursiva para localizar un préstamo por su código.

- **Caso base:** el índice queda fuera de los límites de la lista o se encuentra el código buscado.
- **Paso recursivo:** continúa con el siguiente elemento mediante `indice + 1`.
- **Uso:** permite localizar el préstamo activo durante el proceso de devolución.

**Complejidad temporal:** \(O(n)\) en el peor caso.

---

# 🔁 4. Algoritmos recursivos adicionales

La recursividad consiste en resolver un problema mediante una función que se llama a sí misma hasta alcanzar un caso base.

## 4.1. `calcular_multa_recursiva(dias_retraso, tarifa_por_semana)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 79

Calcula el valor acumulado de las multas según los días de retraso, sumando la tarifa semanal mediante llamadas recursivas.

### Funcionamiento

- **Caso base:** si `dias_retraso <= 0`, retorna `0.0`.
- **Paso recursivo:** suma la tarifa semanal y vuelve a llamar a la función restando siete días.

La expresión conceptual es:

```python
tarifa_por_semana + calcular_multa_recursiva(
    dias_retraso - 7,
    tarifa_por_semana
)
```

- **Uso:** se integra en `registrar_devolucion()` para calcular las multas durante las devoluciones.
- **Complejidad temporal:** \(O(n/7)\), equivalente a \(O(n)\) respecto a los días de retraso.

## 4.2. `contar_libros_disponibles_recursivo(libros, indice)`

**Archivo:** `biblioteca.py`  
**Línea de referencia:** 126

Recorre recursivamente la lista para contar los ejemplares disponibles para préstamo.

- **Caso base:** si `indice >= len(libros)`, retorna `0`.
- **Paso recursivo:** suma `1` si el libro está disponible o `0` si está prestado, y continúa con el siguiente índice.
- **Resultado:** devuelve la cantidad total de libros disponibles.

La operación conceptual es:

```python
(1 if libro.esta_disponible() else 0) + contar_libros_disponibles_recursivo(
    libros,
    indice + 1
)
```

**Complejidad temporal:** \(O(n)\), porque se evalúa cada elemento de la lista una vez.

---

# 🌐 5. Implementación en la interfaz web

**Archivo:** `biblioteca_ui.html`  
**Tecnología:** JavaScript ES6+  
**Ubicación de referencia:** a partir de las líneas 1058–1080.

La interfaz web incorpora versiones equivalentes de las estructuras y algoritmos para ofrecer una experiencia interactiva y actualizar la información del catálogo.

## 5.1. Estructuras de datos en JavaScript

Se implementan las clases equivalentes:

- `Nodo`: almacena los datos y la referencia al siguiente nodo.
- `Pila`: gestiona el historial de operaciones bajo el principio LIFO.
- `Cola`: administra las solicitudes pendientes mediante el principio FIFO.

## 5.2. `quicksortLibros(lista, criterio, asc)`

Organiza dinámicamente los libros según el criterio seleccionado.

- Ordenamiento por título o categoría.
- Orden ascendente o descendente.
- Indicador visual del algoritmo activo.

## 5.3. `buscarLibroBinarioRecursivo(librosOrdenados, titulo, inicio, fin)`

Realiza búsquedas mediante búsqueda binaria recursiva en el catálogo web.

- Reduce progresivamente el espacio de búsqueda.
- Se integra con la barra de búsqueda.
- Requiere que la lista esté ordenada según el criterio utilizado.

## 5.4. `calcularMultaRecursiva(dias, tarifa)`

Calcula las multas por retraso mediante recursividad.

- Se utiliza al renderizar las tarjetas de devolución.
- Participa en el procesamiento de las multas durante las devoluciones.

## 5.5. `contarDisponiblesRecursivo(libros, index)`

Cuenta recursivamente los ejemplares disponibles.

- Actualiza las métricas del catálogo.
- Permite actualizar las insignias del encabezado mediante la función `chips()`.

## 5.6. Reservas e historial interactivo

La interfaz web también integra las estructuras dinámicas en sus funcionalidades:

- **Cola de reservas FIFO:** muestra usuarios en espera y permite gestionar las solicitudes.
- **Historial LIFO:** presenta las operaciones recientes mediante tarjetas e indicadores visuales.
- **Control de disponibilidad:** si un libro no tiene ejemplares disponibles, ofrece registrar una reserva.
- **Devoluciones:** cuando se devuelve un ejemplar, el sistema puede atender al primer usuario de la cola de espera.

---

# 📊 6. Matriz comparativa de estructuras y algoritmos

| Componente | Tipo | Complejidad temporal | Aplicación |
|---|---|---|---|
| `Nodo` | Estructura enlazada | \(O(1)\) para acceder a sus referencias | Construcción de pilas y colas |
| `Pila` | Estructura lineal LIFO | \(O(1)\) en inserción y extracción | Historial de transacciones |
| `Cola` | Estructura lineal FIFO | \(O(1)\) en inserción y extracción | Reservas y lista de espera |
| QuickSort | Ordenamiento recursivo | \(O(n \log n)\) promedio | Organización del catálogo |
| Búsqueda binaria | Búsqueda recursiva | \(O(\log n)\) | Localización de libros ordenados |
| Búsqueda de préstamos | Búsqueda lineal recursiva | \(O(n)\) | Localización de préstamos |
| Cálculo de multas | Recursividad | \(O(n)\) respecto a los días de retraso | Devoluciones con mora |
| Conteo de disponibles | Recorrido recursivo | \(O(n)\) | Control del inventario |

*Las complejidades corresponden a las operaciones descritas y pueden variar según los detalles de implementación.*

---

# 🎯 7. Conceptos de Estructura de Datos aplicados

El proyecto integra los siguientes conceptos de la asignatura:

- **Estructuras enlazadas:** construcción de nodos y referencias para organizar los datos dinámicamente.
- **Pilas (LIFO):** administración del historial de transacciones.
- **Colas (FIFO):** gestión ordenada de reservas pendientes.
- **Ordenamiento:** organización de libros por título y categoría mediante QuickSort.
- **Búsqueda binaria:** localización de libros en un catálogo ordenado.
- **Búsqueda lineal recursiva:** localización de préstamos por código.
- **Recursividad:** cálculo de multas y conteo de ejemplares disponibles.
- **Integración de algoritmos:** combinación de ordenamiento y búsqueda en una misma operación.
- **Desarrollo multiplataforma:** aplicación de los conceptos tanto en Python como en JavaScript.

---

# ✅ 8. Conclusión y aprendizajes

BibliotecaVirtual demuestra cómo los conceptos de Estructura de Datos pueden aplicarse en un sistema funcional de gestión bibliotecaria.

La implementación de nodos enlazados, pilas y colas permite administrar el historial de operaciones y las reservas pendientes. Por su parte, QuickSort y la búsqueda binaria facilitan la organización y consulta del catálogo, mientras que la recursividad permite calcular multas y contar los ejemplares disponibles.

La integración de estas funcionalidades en Python y JavaScript conecta la lógica del sistema con una interfaz web interactiva y permite comprender la utilidad práctica de los algoritmos estudiados.

---

## 👨‍🎓 Información académica

**Institución:** Universidad Técnica de Machala  
**Asignatura:** Estructura de Datos  
**Proyecto:** BibliotecaVirtual — Sistema de Gestión de Biblioteca Digital  
**Periodo:** Primer Hemisemestre