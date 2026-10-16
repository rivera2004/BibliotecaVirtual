"""
Sistema de Gestión de Biblioteca Digital
Universidad Técnica de Machala

Módulo principal que integra clases del dominio, persistencia de datos
y la interfaz interactiva basada en ipywidgets para Jupyter Notebook.
"""

# ─────────────────────────────────────────────
# IMPORTACIONES
# ─────────────────────────────────────────────

import os
import json
import math
import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import ipywidgets as widgets
from IPython.display import display, clear_output

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────

ARCHIVO_DATOS        = "biblioteca_datos.json"
MULTA_POR_SEMANA     = 0.50      # dólares por semana de retraso
MAX_LIBROS_PRESTADOS = 3         # máximo simultáneo por estudiante
DIAS_PRESTAMO_LIBRO  = 7         # días que dura un préstamo de libro
CREDENCIALES_ADMIN   = {"usuario": "admin_biblioteca", "contrasena": "123"}

LIBROS_DEFAULT = [
    ("Cien años de soledad", "Novela",   "Realismo mágico"),
    ("Clean Code",           "Técnico",  "Programación"),
    ("El principito",        "Infantil", "Fábula"),
    ("Python para todos",    "Técnico",  "Educativo"),
    ("1984",                 "Novela",   "Distopía"),
    ("Don Quijote",          "Clásico",  "Aventura"),
]

# ─────────────────────────────────────────────
# UTILIDADES GENERALES
# ─────────────────────────────────────────────

def limpiar_pantalla():
    """Limpia la consola del sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def limpiar_pantalla_widgets():
    """Limpia la salida de la celda activa en Jupyter."""
    clear_output(wait=True)


def imprimir_titulo(texto):
    """Imprime un título centrado con bordes decorativos."""
    separador = "=" * 60
    print(f"\n{separador}")
    print(texto.center(60))
    print(f"{separador}\n")


def validar_email(email: str) -> bool:
    """Valida que la cadena tenga formato de correo electrónico."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_matricula(matricula: str) -> bool:
    """Valida que la matrícula sea numérica y tenga al menos 6 dígitos."""
    return matricula.isdigit() and len(matricula) >= 6


# ─────────────────────────────────────────────
# DOMINIO: CLASES DEL MODELO
# ─────────────────────────────────────────────

class Material(ABC):
    """Clase abstracta base para cualquier material de la biblioteca."""

    def __init__(self, id_material: str, titulo: str, categoria: str, genero: str):
        self.__id_material = id_material
        self.__titulo      = titulo
        self.__categoria   = categoria
        self.__genero      = genero
        self.__disponible  = True

    # ── Getters ──────────────────────────────
    def get_id(self)          -> str:  return self.__id_material
    def get_titulo(self)      -> str:  return self.__titulo
    def get_categoria(self)   -> str:  return self.__categoria
    def get_genero(self)      -> str:  return self.__genero
    def esta_disponible(self) -> bool: return self.__disponible

    def set_disponible(self, estado: bool):
        """Actualiza la disponibilidad del material."""
        self.__disponible = estado

    # ── Métodos abstractos ───────────────────
    @abstractmethod
    def mostrar_info(self) -> str:
        """Retorna una cadena con la información del material."""

    @abstractmethod
    def tipo_material(self) -> str:
        """Retorna el tipo de material (ej. 'Libro')."""

    @abstractmethod
    def tiempo_prestamo_dias(self) -> int:
        """Retorna la cantidad de días permitidos para el préstamo."""


# ─────────────────────────────────────────────

class Libro(Material):
    """Representa un libro dentro del catálogo de la biblioteca."""

    _contador = 100  # contador de IDs autoincremental

    def __init__(self, titulo: str, categoria: str, genero: str, id_material: str = None):
        if id_material is None:
            id_material = f"LIB-{Libro._contador}"
            Libro._contador += 1
        else:
            # Al cargar desde persistencia, sincronizar el contador
            try:
                num = int(id_material.split("-")[1])
                if num >= Libro._contador:
                    Libro._contador = num + 1
            except (IndexError, ValueError):
                pass

        super().__init__(id_material, titulo, categoria, genero)

    def mostrar_info(self) -> str:
        estado = "Disponible" if self.esta_disponible() else "Prestado"
        return (
            f"Titulo   : {self.get_titulo()}\n"
            f"   Categoria: {self.get_categoria()}\n"
            f"   Genero   : {self.get_genero()}\n"
            f"   Estado   : {estado}"
        )

    def tipo_material(self)        -> str: return "Libro"
    def tiempo_prestamo_dias(self) -> int: return DIAS_PRESTAMO_LIBRO


# ─────────────────────────────────────────────

class Persona:
    """Datos de identificación de una persona (nombre, correo, ID)."""

    def __init__(self, nombre: str, correo: str, id_persona: int):
        self.__nombre = nombre
        self.__correo = correo
        self.__id     = id_persona

    def get_nombre(self) -> str:  return self.__nombre
    def get_correo(self) -> str:  return self.__correo
    def get_id(self)     -> int:  return self.__id


# ─────────────────────────────────────────────

class Admin:
    """Administrador del sistema con lógica de inicio de sesión."""

    MAX_INTENTOS = 3

    def __init__(self, persona: Persona):
        self.__persona    = persona
        self.__usuario    = CREDENCIALES_ADMIN["usuario"]
        self.__contrasena = CREDENCIALES_ADMIN["contrasena"]

    def inicio_sesion(self) -> bool:
        """
        Solicita credenciales por consola.
        Retorna True si el acceso fue exitoso, False en caso contrario.
        """
        imprimir_titulo("INICIO DE SESION")
        intentos = Admin.MAX_INTENTOS

        while intentos > 0:
            usuario = input("Usuario: ")
            if usuario != self.__usuario:
                intentos -= 1
                print(f"Usuario incorrecto. Intentos restantes: {intentos}")
                continue

            contrasena = input("Contraseña: ")
            if contrasena == self.__contrasena:
                print(f"\nBienvenido, {self.__persona.get_nombre()}!")
                return True

            intentos -= 1
            print(f"Contraseña incorrecta. Intentos restantes: {intentos}")

        print("Acceso denegado.")
        return False


# ─────────────────────────────────────────────

class Estudiante:
    """Representa a un estudiante registrado en la biblioteca."""

    def __init__(self, persona: Persona, matricula: str):
        self.__persona           = persona
        self.__matricula         = matricula
        self.__libros_prestados  = 0
        self.__multas_pendientes = 0.0

    # ── Getters ──────────────────────────────
    def get_persona(self)           -> Persona: return self.__persona
    def get_matricula(self)         -> str:     return self.__matricula
    def get_libros_prestados(self)  -> int:     return self.__libros_prestados
    def get_multas_pendientes(self) -> float:   return self.__multas_pendientes

    # ── Lógica de negocio ────────────────────
    def agregar_multa(self, monto: float):
        """Acumula una multa y la reporta en consola."""
        self.__multas_pendientes += monto
        print(f"Multa: ${monto:.2f} | Total pendiente: ${self.__multas_pendientes:.2f}")

    def puede_prestar(self) -> bool:
        """Verifica si el estudiante puede recibir un nuevo préstamo."""
        if self.__multas_pendientes > 0:
            print(f"Tiene multas pendientes: ${self.__multas_pendientes:.2f}")
            return False
        if self.__libros_prestados >= MAX_LIBROS_PRESTADOS:
            print(f"Ya tiene {MAX_LIBROS_PRESTADOS} libros prestados (límite alcanzado).")
            return False
        return True

    def incrementar_prestamos(self):
        self.__libros_prestados += 1

    def decrementar_prestamos(self):
        if self.__libros_prestados > 0:
            self.__libros_prestados -= 1


# ─────────────────────────────────────────────

class Prestamo:
    """Gestiona los préstamos activos: registro y devolución."""

    _contador = 1000  # contador de códigos de préstamo

    def __init__(self):
        self.__prestamos_activos: list = []

    def get_prestamos_activos(self) -> list:
        """Retorna una copia de la lista de préstamos activos."""
        return self.__prestamos_activos.copy()

    def registrar_prestamo(self, estudiante: Estudiante, libro: Libro) -> bool:
        """
        Registra un nuevo préstamo si el libro está disponible
        y el estudiante cumple las condiciones.
        """
        if not libro.esta_disponible():
            print("El libro no está disponible.")
            return False
        if not estudiante.puede_prestar():
            return False

        codigo    = Prestamo._contador
        Prestamo._contador += 1
        fecha_hoy = datetime.now()
        fecha_dev = fecha_hoy + timedelta(days=libro.tiempo_prestamo_dias())

        self.__prestamos_activos.append({
            "codigo_prestamo"           : codigo,
            "estudiante"                : estudiante,
            "libro"                     : libro,
            "fecha_salida"              : fecha_hoy,
            "fecha_devolucion_esperada" : fecha_dev,
            "fecha_devolucion_real"     : None,
        })

        libro.set_disponible(False)
        estudiante.incrementar_prestamos()

        imprimir_titulo("PRESTAMO REGISTRADO")
        print(f"Código    : {codigo}")
        print(f"Estudiante: {estudiante.get_persona().get_nombre()}")
        print(f"Libro     : {libro.get_titulo()}")
        print(f"Devolver  : {fecha_dev.strftime('%d/%m/%Y')}")
        return True

    def registrar_devolucion(self, codigo_prestamo: int) -> bool:
        """
        Procesa la devolución de un préstamo.
        Calcula multa si hay retraso.
        """
        for prestamo in self.__prestamos_activos:
            if prestamo["codigo_prestamo"] != codigo_prestamo:
                continue

            estudiante = prestamo["estudiante"]
            libro      = prestamo["libro"]
            fecha_real = datetime.now()
            fecha_esp  = prestamo["fecha_devolucion_esperada"]

            if fecha_real > fecha_esp:
                dias    = (fecha_real - fecha_esp).days
                semanas = math.ceil(dias / 7)
                multa   = semanas * MULTA_POR_SEMANA
                imprimir_titulo("DEVOLUCIÓN CON RETRASO")
                print(f"Días de retraso: {dias} | Multa aplicada: ${multa:.2f}")
                estudiante.agregar_multa(multa)
            else:
                imprimir_titulo("DEVOLUCIÓN EXITOSA")
                print("Sin multa por retraso.")

            libro.set_disponible(True)
            estudiante.decrementar_prestamos()
            self.__prestamos_activos.remove(prestamo)
            return True

        print("Préstamo no encontrado.")
        return False

    def prestamos_activos_de_estudiante(self, estudiante: Estudiante) -> list:
        """Retorna los préstamos activos de un estudiante específico."""
        return [p for p in self.__prestamos_activos if p["estudiante"] == estudiante]


# ─────────────────────────────────────────────
# PERSISTENCIA (JSON)
# ─────────────────────────────────────────────

def guardar_datos(libros: list, estudiantes: list, archivo: str = ARCHIVO_DATOS):
    """Serializa libros y estudiantes en un archivo JSON."""
    datos = {
        "libros": [
            {
                "id"        : l.get_id(),
                "titulo"    : l.get_titulo(),
                "categoria" : l.get_categoria(),
                "genero"    : l.get_genero(),
                "disponible": l.esta_disponible(),
            }
            for l in libros
        ],
        "estudiantes": [
            {
                "nombre"          : e.get_persona().get_nombre(),
                "correo"          : e.get_persona().get_correo(),
                "id"              : e.get_persona().get_id(),
                "matricula"       : e.get_matricula(),
                "libros_prestados": e.get_libros_prestados(),
                "multas"          : e.get_multas_pendientes(),
            }
            for e in estudiantes
        ],
    }
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_datos(archivo: str = ARCHIVO_DATOS) -> tuple:
    """
    Lee el archivo JSON y reconstruye las listas de libros y estudiantes.
    Retorna ([], []) si el archivo no existe.
    """
    if not os.path.exists(archivo):
        return [], []

    with open(archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)

    libros = []
    for l in datos.get("libros", []):
        libro = Libro(l["titulo"], l["categoria"], l["genero"], l["id"])
        libro.set_disponible(l["disponible"])
        libros.append(libro)

    estudiantes = []
    for e in datos.get("estudiantes", []):
        persona    = Persona(e["nombre"], e["correo"], e["id"])
        estudiante = Estudiante(persona, e["matricula"])
        # Restaurar estado interno que no se puede asignar por getters
        estudiante._Estudiante__libros_prestados  = e.get("libros_prestados", 0)
        estudiante._Estudiante__multas_pendientes = e.get("multas", 0.0)
        estudiantes.append(estudiante)

    return libros, estudiantes


# ─────────────────────────────────────────────
# ESTADO GLOBAL DEL SISTEMA
# ─────────────────────────────────────────────

datos_sistema: dict = {
    "libros"     : [],
    "estudiantes": [],
    "prestamos"  : None,
}


# ─────────────────────────────────────────────
# HELPERS INTERNOS DE WIDGETS
# ─────────────────────────────────────────────

def _btn_volver_simple():
    """Muestra un botón de 'Volver al menú' independiente."""
    btn = widgets.Button(description="VOLVER AL MENÚ", button_style="info")
    btn.on_click(lambda _: [btn.close(), mostrar_menu()])
    display(btn)


# ─────────────────────────────────────────────
# WIDGETS: MENÚ PRINCIPAL
# ─────────────────────────────────────────────

def mostrar_menu():
    """Muestra el menú principal con un dropdown de opciones."""
    limpiar_pantalla_widgets()
    imprimir_titulo("MENÚ PRINCIPAL")

    opciones = [
        ("Seleccione...",             "0"),
        ("1. Registrar préstamo",     "1"),
        ("2. Registrar devolución",   "2"),
        ("3. Ver catálogo",           "3"),
        ("4. Agregar libro",          "4"),
        ("5. Eliminar libro",         "5"),
        ("6. Eliminar estudiante",    "6"),
        ("7. Salir",                  "7"),
    ]

    dropdown     = widgets.Dropdown(
        options=opciones, value="0",
        description="Opción:", layout=widgets.Layout(width="350px"),
    )
    btn_ejecutar = widgets.Button(
        description="EJECUTAR", button_style="primary",
        layout=widgets.Layout(width="150px"),
    )

    _ACCIONES_MENU = {
        "1": widget_prestamo,
        "2": widget_devolucion,
        "3": widget_catalogo,
        "4": widget_agregar_libro,
        "5": widget_eliminar_libro,
        "6": widget_eliminar_estudiante,
    }

    def ejecutar(_):
        opcion = dropdown.value
        dropdown.close()
        btn_ejecutar.close()

        if opcion in _ACCIONES_MENU:
            _ACCIONES_MENU[opcion]()
        elif opcion == "7":
            guardar_datos(datos_sistema["libros"], datos_sistema["estudiantes"])
            print("\n¡Gracias por usar el Sistema de Biblioteca Digital!")

    btn_ejecutar.on_click(ejecutar)
    display(dropdown, btn_ejecutar)


# ─────────────────────────────────────────────
# WIDGETS: FLUJO DE PRÉSTAMO
# ─────────────────────────────────────────────

def widget_prestamo():
    """Punto de entrada del flujo de registro de préstamo."""
    limpiar_pantalla_widgets()
    imprimir_titulo("REGISTRAR PRÉSTAMO")

    btn_existente = widgets.Button(
        description="ESTUDIANTE EXISTENTE", button_style="primary",
        layout=widgets.Layout(width="280px"),
    )
    btn_nuevo  = widgets.Button(
        description="NUEVO ESTUDIANTE", button_style="success",
        layout=widgets.Layout(width="280px"),
    )
    btn_volver = widgets.Button(
        description="VOLVER AL MENÚ", button_style="info",
        layout=widgets.Layout(width="280px"),
    )

    def _cerrar_botones():
        btn_existente.close(); btn_nuevo.close(); btn_volver.close()

    def ir_existente(_):
        _cerrar_botones()
        if not datos_sistema["estudiantes"]:
            limpiar_pantalla_widgets()
            imprimir_titulo("REGISTRAR PRÉSTAMO")
            print("No hay estudiantes registrados. Registre uno nuevo.")
            btn_ok = widgets.Button(description="REGISTRAR NUEVO", button_style="success")
            btn_ok.on_click(lambda _2: [btn_ok.close(), registrar_estudiante()])
            display(btn_ok)
        else:
            seleccionar_estudiante()

    btn_existente.on_click(ir_existente)
    btn_nuevo.on_click(lambda _: [_cerrar_botones(), registrar_estudiante()])
    btn_volver.on_click(lambda _: [_cerrar_botones(), mostrar_menu()])
    display(btn_existente, btn_nuevo, btn_volver)


def registrar_estudiante():
    """Formulario para registrar un nuevo estudiante."""
    limpiar_pantalla_widgets()
    imprimir_titulo("REGISTRAR NUEVO ESTUDIANTE")

    campo_nombre    = widgets.Text(placeholder="Nombre completo",    description="Nombre:",    layout=widgets.Layout(width="420px"))
    campo_correo    = widgets.Text(placeholder="Correo electrónico", description="Correo:",    layout=widgets.Layout(width="420px"))
    campo_matricula = widgets.Text(placeholder="Matrícula",          description="Matrícula:", layout=widgets.Layout(width="420px"))
    btn_guardar     = widgets.Button(description="GUARDAR",   button_style="success", layout=widgets.Layout(width="180px"))
    btn_cancelar    = widgets.Button(description="CANCELAR",  button_style="danger",  layout=widgets.Layout(width="180px"))
    salida          = widgets.Output()

    def _cerrar_formulario():
        campo_nombre.close(); campo_correo.close(); campo_matricula.close()
        btn_guardar.close(); btn_cancelar.close()

    def guardar(_):
        with salida:
            clear_output(wait=True)
            nombre    = campo_nombre.value.strip()
            correo    = campo_correo.value.strip()
            matricula = campo_matricula.value.strip()

            if not (nombre and correo and matricula):
                print("ERROR: Todos los campos son obligatorios.")
                return

            try:
                if not nombre.replace(" ", "").isalpha():
                    raise ValueError("El nombre solo debe contener letras y espacios.")
                if not validar_email(correo):
                    raise ValueError("El formato del correo no es válido.")
                if not validar_matricula(matricula):
                    raise ValueError("La matrícula debe tener solo números (mín. 6 dígitos).")

                estudiantes = datos_sistema["estudiantes"]
                if any(e.get_matricula() == matricula for e in estudiantes):
                    print("ERROR: Ya existe un estudiante con esa matrícula.")
                    return

                nuevo_id = (max(e.get_persona().get_id() for e in estudiantes) + 1) if estudiantes else 101
                persona  = Persona(nombre, correo, nuevo_id)
                nuevo    = Estudiante(persona, matricula)
                estudiantes.append(nuevo)
                guardar_datos(datos_sistema["libros"], estudiantes)
                print(f"Estudiante '{nombre}' registrado correctamente.")

                _cerrar_formulario()
                btn_menu = widgets.Button(description="VOLVER AL MENÚ", button_style="info", layout=widgets.Layout(width="200px"))
                btn_menu.on_click(lambda _2: [btn_menu.close(), mostrar_menu()])
                display(btn_menu)

            except ValueError as err:
                print(f"ERROR: {err}")
            except Exception as err:
                print(f"ERROR inesperado: {err}")

    btn_guardar.on_click(guardar)
    btn_cancelar.on_click(lambda _: [_cerrar_formulario(), widget_prestamo()])
    display(campo_nombre, campo_correo, campo_matricula, btn_guardar, btn_cancelar, salida)


def seleccionar_estudiante():
    """Permite elegir un estudiante existente para continuar el préstamo."""
    limpiar_pantalla_widgets()
    imprimir_titulo("SELECCIONAR ESTUDIANTE")

    estudiantes = datos_sistema["estudiantes"]
    opciones    = [
        (f"{e.get_persona().get_nombre()} – Libros: {e.get_libros_prestados()}/{MAX_LIBROS_PRESTADOS}", i)
        for i, e in enumerate(estudiantes)
    ]

    dropdown   = widgets.Dropdown(options=opciones, description="Estudiante:", layout=widgets.Layout(width="480px"))
    btn_ok     = widgets.Button(description="CONTINUAR", button_style="primary")
    btn_volver = widgets.Button(description="VOLVER",    button_style="info")

    def continuar(_):
        idx = dropdown.value
        dropdown.close(); btn_ok.close(); btn_volver.close()
        seleccionar_libro(estudiantes[idx])

    btn_ok.on_click(continuar)
    btn_volver.on_click(lambda _: [dropdown.close(), btn_ok.close(), btn_volver.close(), widget_prestamo()])
    display(dropdown, btn_ok, btn_volver)


def seleccionar_libro(estudiante: Estudiante):
    """Permite elegir un libro disponible y confirmar el préstamo."""
    limpiar_pantalla_widgets()
    imprimir_titulo("SELECCIONAR LIBRO")
    print(f"Estudiante: {estudiante.get_persona().get_nombre()}")

    libros_disp = [l for l in datos_sistema["libros"] if l.esta_disponible()]

    if not libros_disp:
        print("\nNo hay libros disponibles en este momento.")
        btn_agregar = widgets.Button(description="AGREGAR LIBRO",  button_style="success", layout=widgets.Layout(width="200px"))
        btn_menu    = widgets.Button(description="VOLVER AL MENÚ", button_style="info",    layout=widgets.Layout(width="200px"))
        btn_agregar.on_click(lambda _: [btn_agregar.close(), btn_menu.close(), widget_agregar_libro()])
        btn_menu.on_click(lambda _: [btn_agregar.close(), btn_menu.close(), mostrar_menu()])
        display(btn_agregar, btn_menu)
        return

    print(f"\nLibros disponibles: {len(libros_disp)}")
    print("-" * 40)

    opciones    = [(f"{i+1}. {l.get_titulo()} | {l.get_categoria()} | {l.get_genero()}", i) for i, l in enumerate(libros_disp)]
    dropdown    = widgets.Dropdown(options=opciones, description="Libro:", layout=widgets.Layout(width="580px"))
    btn_prestar = widgets.Button(description="CONFIRMAR PRÉSTAMO",    button_style="success", layout=widgets.Layout(width="200px"))
    btn_cambiar = widgets.Button(description="ELEGIR OTRO ESTUDIANTE", button_style="warning", layout=widgets.Layout(width="200px"))
    btn_menu    = widgets.Button(description="VOLVER AL MENÚ",         button_style="info",    layout=widgets.Layout(width="200px"))

    def _cerrar():
        dropdown.close(); btn_prestar.close(); btn_cambiar.close(); btn_menu.close()

    def confirmar(_):
        libro = libros_disp[dropdown.value]
        _cerrar()
        limpiar_pantalla_widgets()

        if not estudiante.puede_prestar():
            imprimir_titulo("PRÉSTAMO RECHAZADO")
            btn_retry = widgets.Button(description="INTENTAR CON OTRO LIBRO", button_style="warning", layout=widgets.Layout(width="220px"))
            btn_m     = widgets.Button(description="VOLVER AL MENÚ",           button_style="info",    layout=widgets.Layout(width="160px"))
            btn_retry.on_click(lambda _2: [btn_retry.close(), btn_m.close(), seleccionar_libro(estudiante)])
            btn_m.on_click(lambda _2: [btn_retry.close(), btn_m.close(), mostrar_menu()])
            display(btn_retry, btn_m)
            return

        if datos_sistema["prestamos"].registrar_prestamo(estudiante, libro):
            guardar_datos(datos_sistema["libros"], datos_sistema["estudiantes"])

        btn_nuevo = widgets.Button(description="NUEVO PRÉSTAMO", button_style="warning", layout=widgets.Layout(width="180px"))
        btn_m     = widgets.Button(description="VOLVER AL MENÚ", button_style="info",    layout=widgets.Layout(width="180px"))
        btn_nuevo.on_click(lambda _2: [btn_nuevo.close(), btn_m.close(), widget_prestamo()])
        btn_m.on_click(lambda _2: [btn_nuevo.close(), btn_m.close(), mostrar_menu()])
        display(btn_nuevo, btn_m)

    btn_prestar.on_click(confirmar)
    btn_cambiar.on_click(lambda _: [_cerrar(), widget_prestamo()])
    btn_menu.on_click(lambda _: [_cerrar(), mostrar_menu()])
    display(dropdown, btn_prestar, btn_cambiar, btn_menu)


# ─────────────────────────────────────────────
# WIDGETS: DEVOLUCIÓN
# ─────────────────────────────────────────────

def widget_devolucion():
    """Muestra los préstamos activos y permite registrar una devolución."""
    limpiar_pantalla_widgets()
    imprimir_titulo("REGISTRAR DEVOLUCIÓN")

    prestamos = datos_sistema["prestamos"]
    activos   = prestamos.get_prestamos_activos()

    if not activos:
        print("No hay préstamos activos en este momento.")
        _btn_volver_simple()
        return

    opciones  = [
        (f"Cód:{p['codigo_prestamo']} – {p['libro'].get_titulo()} – {p['estudiante'].get_persona().get_nombre()}", p["codigo_prestamo"])
        for p in activos
    ]
    dropdown   = widgets.Dropdown(options=opciones, description="Préstamo:", layout=widgets.Layout(width="580px"))
    btn_dev    = widgets.Button(description="REGISTRAR DEVOLUCIÓN", button_style="warning")
    btn_volver = widgets.Button(description="VOLVER",               button_style="info")

    def devolver(_):
        codigo = dropdown.value
        dropdown.close(); btn_dev.close(); btn_volver.close()
        limpiar_pantalla_widgets()

        if prestamos.registrar_devolucion(codigo):
            guardar_datos(datos_sistema["libros"], datos_sistema["estudiantes"])

        btn_menu = widgets.Button(description="VOLVER AL MENÚ", button_style="info")
        btn_menu.on_click(lambda _2: [btn_menu.close(), mostrar_menu()])
        display(btn_menu)

    btn_dev.on_click(devolver)
    btn_volver.on_click(lambda _: [dropdown.close(), btn_dev.close(), btn_volver.close(), mostrar_menu()])
    display(dropdown, btn_dev, btn_volver)


# ─────────────────────────────────────────────
# WIDGETS: CATÁLOGO
# ─────────────────────────────────────────────

def widget_catalogo():
    """Muestra todos los libros del catálogo con su estado."""
    limpiar_pantalla_widgets()
    imprimir_titulo("CATÁLOGO DE LIBROS")

    libros = datos_sistema["libros"]
    if not libros:
        print("El catálogo está vacío.")
    else:
        for i, libro in enumerate(libros, start=1):
            print(f"\n___ Libro #{i} ___")
            print(libro.mostrar_info())

    _btn_volver_simple()


# ─────────────────────────────────────────────
# WIDGETS: AGREGAR LIBRO
# ─────────────────────────────────────────────

def widget_agregar_libro():
    """Formulario para agregar un nuevo libro al catálogo."""
    limpiar_pantalla_widgets()
    imprimir_titulo("AGREGAR NUEVO LIBRO")

    campo_titulo    = widgets.Text(placeholder="Título del libro", description="Título:",    layout=widgets.Layout(width="420px"))
    campo_categoria = widgets.Text(placeholder="Categoría",        description="Categoría:", layout=widgets.Layout(width="420px"))
    campo_genero    = widgets.Text(placeholder="Género",           description="Género:",    layout=widgets.Layout(width="420px"))
    btn_guardar     = widgets.Button(description="GUARDAR LIBRO",  button_style="success")
    btn_volver      = widgets.Button(description="VOLVER AL MENÚ", button_style="info")
    salida          = widgets.Output()

    def _cerrar_formulario():
        campo_titulo.close(); campo_categoria.close(); campo_genero.close()
        btn_guardar.close(); btn_volver.close()

    def guardar(_):
        with salida:
            clear_output(wait=True)
            titulo    = campo_titulo.value.strip()
            categoria = campo_categoria.value.strip()
            genero    = campo_genero.value.strip()

            if titulo and categoria and genero:
                nuevo_libro = Libro(titulo, categoria, genero)
                datos_sistema["libros"].append(nuevo_libro)
                guardar_datos(datos_sistema["libros"], datos_sistema["estudiantes"])
                print(f"Libro '{titulo}' agregado al catálogo.")
                campo_titulo.value = campo_categoria.value = campo_genero.value = ""
            else:
                print("ERROR: Todos los campos son obligatorios.")

    btn_guardar.on_click(guardar)
    btn_volver.on_click(lambda _: [_cerrar_formulario(), mostrar_menu()])
    display(campo_titulo, campo_categoria, campo_genero, btn_guardar, btn_volver, salida)


# ─────────────────────────────────────────────
# WIDGETS: ELIMINAR LIBRO
# ─────────────────────────────────────────────

def widget_eliminar_libro():
    """Permite eliminar un libro disponible del catálogo."""
    limpiar_pantalla_widgets()
    imprimir_titulo("ELIMINAR LIBRO")

    libros = datos_sistema["libros"]

    if not libros:
        print("No hay libros registrados.")
        _btn_volver_simple()
        return

    disponibles = [(i, l) for i, l in enumerate(libros) if l.esta_disponible()]
    if not disponibles:
        print("No hay libros disponibles para eliminar (todos están prestados).")
        _btn_volver_simple()
        return

    opciones   = [(f"{l.get_titulo()} | {l.get_categoria()} | {l.get_genero()}", idx) for idx, l in disponibles]
    dropdown   = widgets.Dropdown(options=opciones, description="Libro:", layout=widgets.Layout(width="580px"))
    btn_elim   = widgets.Button(description="ELIMINAR",       button_style="danger")
    btn_volver = widgets.Button(description="VOLVER AL MENÚ", button_style="info")
    salida     = widgets.Output()

    def _cerrar_principales():
        dropdown.close(); btn_elim.close(); btn_volver.close()

    def eliminar(_):
        with salida:
            clear_output(wait=True)
            libro = libros[dropdown.value]
            print(f"¿Está seguro de eliminar el libro '{libro.get_titulo()}'?")

            btn_si    = widgets.Button(description="SÍ, ELIMINAR",   button_style="danger")
            btn_no    = widgets.Button(description="NO, CANCELAR",   button_style="primary")
            btn_menu2 = widgets.Button(description="VOLVER AL MENÚ", button_style="info")

            def confirmar_si(_2):
                _cerrar_principales()
                btn_si.close(); btn_no.close(); btn_menu2.close()
                libros.remove(libro)
                guardar_datos(libros, datos_sistema["estudiantes"])
                print(f"Libro '{libro.get_titulo()}' eliminado correctamente.")

                btn_otro = widgets.Button(description="ELIMINAR OTRO",  button_style="warning", layout=widgets.Layout(width="180px"))
                btn_fin  = widgets.Button(description="VOLVER AL MENÚ", button_style="info",    layout=widgets.Layout(width="180px"))
                btn_otro.on_click(lambda _3: [btn_otro.close(), btn_fin.close(), widget_eliminar_libro()])
                btn_fin.on_click(lambda _3: [btn_otro.close(), btn_fin.close(), mostrar_menu()])
                display(btn_otro, btn_fin)

            def confirmar_no(_2):
                btn_si.close(); btn_no.close(); btn_menu2.close()
                print("Eliminación cancelada.")

            btn_si.on_click(confirmar_si)
            btn_no.on_click(confirmar_no)
            btn_menu2.on_click(lambda _2: [btn_si.close(), btn_no.close(), btn_menu2.close(), mostrar_menu()])
            display(btn_si, btn_no, btn_menu2)

    btn_elim.on_click(eliminar)
    btn_volver.on_click(lambda _: [_cerrar_principales(), mostrar_menu()])
    display(dropdown, btn_elim, btn_volver, salida)


# ─────────────────────────────────────────────
# WIDGETS: ELIMINAR ESTUDIANTE
# ─────────────────────────────────────────────

def widget_eliminar_estudiante():
    """Permite eliminar un estudiante sin préstamos activos."""
    limpiar_pantalla_widgets()
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    estudiantes = datos_sistema["estudiantes"]

    if not estudiantes:
        print("No hay estudiantes registrados.")
        _btn_volver_simple()
        return

    opciones   = [
        (f"{e.get_persona().get_nombre()} – Matrícula: {e.get_matricula()} – Préstamos: {e.get_libros_prestados()}", i)
        for i, e in enumerate(estudiantes)
    ]
    dropdown   = widgets.Dropdown(options=opciones, description="Estudiante:", layout=widgets.Layout(width="580px"))
    btn_elim   = widgets.Button(description="ELIMINAR",       button_style="danger")
    btn_volver = widgets.Button(description="VOLVER AL MENÚ", button_style="info")
    salida     = widgets.Output()

    def _cerrar_principales():
        dropdown.close(); btn_elim.close(); btn_volver.close()

    def eliminar(_):
        with salida:
            clear_output(wait=True)
            estudiante        = estudiantes[dropdown.value]
            prestamos_activos = datos_sistema["prestamos"].prestamos_activos_de_estudiante(estudiante)

            if prestamos_activos:
                print(
                    f"El estudiante {estudiante.get_persona().get_nombre()} tiene "
                    f"{len(prestamos_activos)} préstamo(s) activo(s).\n"
                    "Debe devolver todos los libros antes de eliminar la cuenta."
                )
                btn_ok = widgets.Button(description="ENTENDIDO", button_style="info")
                btn_ok.on_click(lambda _2: [btn_ok.close(), widget_eliminar_estudiante()])
                display(btn_ok)
                return

            print(f"¿Está seguro de eliminar al estudiante '{estudiante.get_persona().get_nombre()}'?")

            btn_si    = widgets.Button(description="SÍ, ELIMINAR",   button_style="danger")
            btn_no    = widgets.Button(description="NO, CANCELAR",   button_style="primary")
            btn_menu2 = widgets.Button(description="VOLVER AL MENÚ", button_style="info")

            def confirmar_si(_2):
                _cerrar_principales()
                btn_si.close(); btn_no.close(); btn_menu2.close()
                estudiantes.remove(estudiante)
                guardar_datos(datos_sistema["libros"], estudiantes)
                print(f"Estudiante '{estudiante.get_persona().get_nombre()}' eliminado correctamente.")

                btn_otro = widgets.Button(description="ELIMINAR OTRO",  button_style="warning", layout=widgets.Layout(width="200px"))
                btn_fin  = widgets.Button(description="VOLVER AL MENÚ", button_style="info",    layout=widgets.Layout(width="200px"))
                btn_otro.on_click(lambda _3: [btn_otro.close(), btn_fin.close(), widget_eliminar_estudiante()])
                btn_fin.on_click(lambda _3: [btn_otro.close(), btn_fin.close(), mostrar_menu()])
                display(btn_otro, btn_fin)

            def confirmar_no(_2):
                btn_si.close(); btn_no.close(); btn_menu2.close()
                print("Eliminación cancelada.")

            btn_si.on_click(confirmar_si)
            btn_no.on_click(confirmar_no)
            btn_menu2.on_click(lambda _2: [btn_si.close(), btn_no.close(), btn_menu2.close(), mostrar_menu()])
            display(btn_si, btn_no, btn_menu2)

    btn_elim.on_click(eliminar)
    btn_volver.on_click(lambda _: [_cerrar_principales(), mostrar_menu()])
    display(dropdown, btn_elim, btn_volver, salida)


# ─────────────────────────────────────────────
# PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    """Punto de entrada del sistema de biblioteca."""
    limpiar_pantalla()
    print("\n" + "=" * 54)
    print("    SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL        ")
    print("       Universidad Técnica de Machala               ")
    print("=" * 54 + "\n")

    admin = Admin(Persona("Juan Salazar", "admin@utmachala.edu.ec", 1))
    if not admin.inicio_sesion():
        return

    libros, estudiantes = cargar_datos()

    if not libros:
        libros = [Libro(titulo, categoria, genero) for titulo, categoria, genero in LIBROS_DEFAULT]

    datos_sistema["libros"]      = libros
    datos_sistema["estudiantes"] = estudiantes
    datos_sistema["prestamos"]   = Prestamo()

    mostrar_menu()


if __name__ == "__main__":
    main()
