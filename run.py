# run.py
# PUNTO DE ENTRADA ÚNICO - Dream Wedding Planner v2.0

import subprocess
import sys
import os
import webbrowser
from threading import Timer

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: Python {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def verificar_estructura():
    """Verifica y crea la estructura de carpetas necesaria"""
    print("\n📂 Verificando estructura de carpetas...")
    
    carpetas_requeridas = {
        "data": "Datos persistentes (JSON)",
        "Logic": "Lógica de negocio",
        "Style": "Interfaz visual"
    }
    
    todo_ok = True
    
    for carpeta, descripcion in carpetas_requeridas.items():
        if not os.path.exists(carpeta):
            if carpeta == "data":
                os.makedirs(carpeta)
                print(f"✅ Carpeta '{carpeta}/' creada ({descripcion})")
            else:
                print(f"❌ ERROR: No se encontró la carpeta '{carpeta}/' ({descripcion})")
                todo_ok = False
        else:
            print(f"✅ Carpeta '{carpeta}/' encontrada")
    
    # Verificar archivos críticos en Logic
    archivos_logic = [
        "__init__.py", "models.py", "config.py", 
        "wedding_manager.py", "budget_calculator.py", "data_handler.py"
    ]
    
    for archivo in archivos_logic:
        path = os.path.join("Logic", archivo)
        if not os.path.exists(path):
            print(f"⚠️  ADVERTENCIA: Archivo 'Logic/{archivo}' no encontrado")
    
    # Verificar archivos críticos en Style
    archivos_style = ["__init__.py", "app.py", "styles.py", "components.py", "pages.py"]
    
    for archivo in archivos_style:
        path = os.path.join("Style", archivo)
        if not os.path.exists(path):
            print(f"⚠️  ADVERTENCIA: Archivo 'Style/{archivo}' no encontrado")
    
    return todo_ok

def verificar_dependencias():
    """Verifica e instala dependencias necesarias"""
    print("\n📦 Verificando dependencias...")
    
    dependencias = {
        "streamlit": "Interfaz web",
        "pandas": "Manipulación de datos"
    }
    
    for paquete, descripcion in dependencias.items():
        try:
            __import__(paquete.replace('-', '_'))
            print(f"✅ {paquete} instalado ({descripcion})")
        except ImportError:
            print(f"⬇️  Instalando {paquete}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", paquete],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✅ {paquete} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error instalando {paquete}")
                return False
    
    return True

def crear_archivo_configuracion():
    """Crea archivo de configuración si no existe"""
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
            "deposito_confirmacion": 30.0
        }
        
        import json
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Archivo de configuración creado")
    else:
        print("\n✅ Archivo de configuración existente")

def crear_init_files():
    """Crea archivos __init__.py si no existen"""
    init_paths = [
        os.path.join("Logic", "__init__.py"),
        os.path.join("Style", "__init__.py")
    ]
    
    for path in init_paths:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                carpeta = os.path.dirname(path)
                f.write(f"# {carpeta} package\n")
            print(f"✅ Creado {path}")

def abrir_navegador():
    """Abre el navegador automáticamente"""
    try:
        webbrowser.open("http://localhost:8501")
    except:
        pass  # No es crítico si falla

def mostrar_banner():
    """Muestra el banner de inicio"""
    print("\n" + "="*60)
    print("💍  DREAM WEDDING PLANNER v2.0")
    print("="*60)
    print("\n🎯 Sistema Inteligente de Planificación de Bodas")
    print("   ✨ Gestión de recursos y eventos")
    print("   ✅ Validación automática de restricciones")
    print("   🔍 Búsqueda inteligente de horarios")
    print("\n" + "="*60)

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    print("\n📋 INSTRUCCIONES:")
    print("   • La aplicación se abrirá automáticamente en tu navegador")
    print("   • URL: http://localhost:8501")
    print("   • Para detener: Presiona Ctrl+C en esta ventana")
    print("\n🔧 Si hay problemas:")
    print("   1. Verifica que tienes Python 3.8 o superior")
    print("   2. Asegúrate de tener todas las carpetas (Logic/, Style/, data/)")
    print("   3. Reinstala dependencias: pip install -r requirements.txt")
    print("="*60 + "\n")

def verificar_puerto():
    """Verifica si el puerto 8501 está disponible"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8501))
    sock.close()
    
    if result == 0:
        print("\n⚠️  ADVERTENCIA: El puerto 8501 está ocupado")
        print("   Streamlit usará otro puerto automáticamente")
        return False
    return True

def main():
    """Función principal de ejecución"""
    
    try:
        # Mostrar banner
        mostrar_banner()
        
        # Verificar Python
        if not verificar_python():
            sys.exit(1)
        
        # Verificar estructura
        if not verificar_estructura():
            print("\n❌ ERROR: Estructura de carpetas incompleta")
            print("💡 Asegúrate de tener las carpetas Logic/ y Style/")
            sys.exit(1)
        
        # Crear archivos __init__.py
        crear_init_files()
        
        # Verificar dependencias
        if not verificar_dependencias():
            print("\n❌ ERROR: No se pudieron instalar las dependencias")
            print("💡 Intenta ejecutar: pip install streamlit pandas")
            sys.exit(1)
        
        # Crear archivo de configuración
        crear_archivo_configuracion()
        
        # Verificar puerto
        verificar_puerto()
        
        # Mostrar instrucciones
        mostrar_instrucciones()
        
        # Abrir navegador después de 3 segundos
        print("🚀 Iniciando servidor...")
        Timer(3, abrir_navegador).start()
        
        # Ejecutar Streamlit
        subprocess.run([
            "streamlit", "run", 
            os.path.join("Style", "app.py"),
            "--server.headless", "true"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
        print("   ¡Gracias por usar Dream Wedding Planner!\n")
    
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Archivo no encontrado - {e}")
        print("💡 Verifica que todos los archivos estén presentes")
    
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        print("\n🔧 Solución de problemas:")
        print("   1. Verifica que tengas Python 3.8+")
        print("   2. Reinstala dependencias: pip install -r requirements.txt")
        print("   3. Verifica permisos de escritura en la carpeta")
        print("   4. Revisa que las carpetas Logic/ y Style/ existan")

if __name__ == "__main__":
    main()