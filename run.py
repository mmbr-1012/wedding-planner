# PUNTO DE ENTRADA ÚNICO - Dream Wedding Planner v2.0

import subprocess
import sys
import os
import json
import webbrowser
from threading import Timer


# ──────────────────────────────────────────────
# UTILIDADES
# ──────────────────────────────────────────────

def mostrar_banner():
    print("\n" + "=" * 60)
    print("💍  DREAM WEDDING PLANNER v2.0")
    print("=" * 60)
    print("\n🎯 Sistema Inteligente de Planificación de Bodas")
    print("   ✨ Gestión de recursos y eventos")
    print("   ✅ Validación automática de restricciones")
    print("   🔍 Búsqueda inteligente de horarios")
    print("\n" + "=" * 60)


def crear_archivo_configuracion():
    config_file = "config.json"
    if not os.path.exists(config_file):
        print("\n📄 Creando archivo de configuración...")
        config = {
            "empresa": "Dream Wedding Planner",
            "version": "2.0.0",
            "moneda": "USD",
            "notificaciones": True,
            "max_invitados": 500,
            "impuestos": 16.0,
            "deposito_confirmacion": 30.0,
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print("✅ Archivo de configuración creado")
    else:
        print("\n✅ Archivo de configuración existente")


def verificar_puerto(puerto: int = 8501) -> bool:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resultado = sock.connect_ex(("localhost", puerto))
    sock.close()
    if resultado == 0:
        print(f"\n⚠️  El puerto {puerto} está ocupado — Streamlit usará otro automáticamente")
        return False
    return True


def abrir_navegador(url: str = "http://localhost:8501"):
    try:
        webbrowser.open(url)
    except Exception:
        pass  # No es crítico


# ──────────────────────────────────────────────
# LANZADOR DE STREAMLIT
# ──────────────────────────────────────────────

def iniciar_streamlit():
    """
    Lanza Streamlit apuntando a Style/app.py.

    Se busca el ejecutable de streamlit en tres lugares, en orden:
      1. Mismo directorio que el intérprete de Python activo  (entornos venv / conda)
      2. Comando 'streamlit' disponible en el PATH del sistema
      3. Módulo Python:  python -m streamlit  (fallback universal)
    """
    app_path = os.path.join("Style", "app.py")

    # ── Verificar que el archivo de entrada existe ──
    if not os.path.exists(app_path):
        print(f"\n❌ No se encontró '{app_path}'")
        print("   Asegúrate de ejecutar run.py desde la raíz del proyecto.")
        sys.exit(1)

    args_streamlit = [
        "run", app_path,
        "--server.headless", "true",
        "--server.port", "8501",
    ]

    # ── Opción 1: ejecutable junto al intérprete activo ──
    scripts_dir = os.path.dirname(sys.executable)          # carpeta Scripts/ o bin/
    exe_nombre  = "streamlit.exe" if sys.platform == "win32" else "streamlit"
    exe_local   = os.path.join(scripts_dir, exe_nombre)

    if os.path.isfile(exe_local):
        cmd = [exe_local] + args_streamlit
        origen = f"ejecutable local ({exe_local})"
    else:
        # ── Opción 2: 'streamlit' en el PATH ──
        import shutil
        if shutil.which("streamlit"):
            cmd = ["streamlit"] + args_streamlit
            origen = "comando 'streamlit' del PATH"
        else:
            # ── Opción 3: python -m streamlit ──
            cmd = [sys.executable, "-m", "streamlit"] + args_streamlit
            origen = f"módulo Python ({sys.executable} -m streamlit)"

    print(f"\n🚀 Iniciando servidor usando {origen}...")
    print(f"   Comando: {' '.join(cmd)}\n")

    # Abrir el navegador 3 s después de lanzar el proceso
    Timer(3, abrir_navegador).start()

    # subprocess.run bloquea hasta que el usuario presione Ctrl+C
    resultado = subprocess.run(cmd)

    if resultado.returncode not in (0, 1):          # 1 = salida normal de Streamlit
        print(f"\n⚠️  Streamlit terminó con código {resultado.returncode}")


# ──────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────

def main():
    try:
        mostrar_banner()
        crear_archivo_configuracion()
        verificar_puerto()
        iniciar_streamlit()

    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
        print("   ¡Gracias por usar Dream Wedding Planner!\n")

    except FileNotFoundError as e:
        print(f"\n❌ Archivo no encontrado: {e}")
        print("   Verifica que todos los archivos del proyecto estén presentes.")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("\n🔧 Pasos para solucionar:")
        print("   1. Ejecuta este script desde la carpeta raíz del proyecto")
        print("   2. Comprueba que Python 3.8+ está instalado")
        print("   3. Reinstala dependencias:  pip install -r requirements.txt")
        print("   4. Verifica que existen las carpetas  Logic/  y  Style/")


if __name__ == "__main__":
    main()