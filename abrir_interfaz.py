"""
Lanzador de la Interfaz Web de la Biblioteca Virtual
Universidad Técnica de Machala
"""

import os
import sys
import webbrowser
from pathlib import Path

def main():
    ruta_html = Path(__file__).resolve().parent / "biblioteca_ui.html"
    if not ruta_html.exists():
        print(f"Error: No se encontró el archivo {ruta_html}")
        sys.exit(1)

    url = ruta_html.as_uri()
    print("=" * 60)
    print("      BIBLIOTECA VIRTUAL - UNIVERSIDAD TÉCNICA DE MACHALA")
    print("=" * 60)
    print(f"\nAbriendo interfaz interactiva en su navegador predeterminado...")
    print(f"Ubicación: {ruta_html}")
    print("\nCredenciales de Administrador:")
    print("  • Usuario:    admin")
    print("  • Contraseña: 123")
    print("=" * 60 + "\n")
    
    webbrowser.open(url)

if __name__ == "__main__":
    main()
