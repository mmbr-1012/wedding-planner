# PUNTO DE ENTRADA

import subprocess
import sys
import os
import webbrowser
from threading import Timer

def verificar_estructura():
    """Verifica y crea la estructura de carpetas necesaria"""
    print("📁 Creando estructura de carpetas...")
    
    # Carpeta para datos
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Carpeta 'data/' creada")
    
    # Carpeta para el paquete (debería existir)
    if not os.path.exists("Logic"):
        print("❌ ERROR: No se encontró la carpeta 'Logic/'")
        print("💡 Asegúrate de que todos los archivos del módulo estén en su lugar")
        return False
    
    print("✅ Estructura verificada")
    return True

def verificar_dependencias():
    """Verifica e instala dependencias necesarias"""
    print("📦 Verificando dependencias...")
    
    requerimientos = ["streamlit", "pandas"]
    
    for paquete in requerimientos:
        try:
            __import__(paquete.replace('-', '_'))
            print(f"✅ {paquete} ya está instalado")
        except ImportError:
            print(f"⬇️ Instalando {paquete}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
                print(f"✅ {paquete} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error instalando {paquete}")
                return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def crear_archivo_configuracion():
    """Crea archivo de configuración si no existe"""
    config_file = "config.json"
    if not os.path.exists(config_file):
        print("📄 Creando archivo de configuración...")
        config = {
            "empresa": "Dream Wedding Planner",
            "version": "1.0.0",
            "moneda": "USD",
            "notificaciones": True,
            "max_invitados": 500
        }
        
        import json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Archivo de configuración creado")
    else:
        print("✅ Archivo de configuración ya existe")

def abrir_navegador():
    """Abre el navegador automáticamente"""
    try:
        webbrowser.open("http://localhost:8501")
    except:
        print("⚠️ No se pudo abrir el navegador automáticamente")

def mostrar_ayuda():
    """Muestra mensaje de ayuda"""
    print("\n" + "="*50)
    print("💍 DREAM WEDDING PLANNER")
    print("="*50)
    print("\n🚀 Iniciando aplicación...")
    print("🌐 La aplicación se abrirá en tu navegador")
    print("📌 Para detener: Ctrl+C")
    print("\n🔧 Si encuentras problemas:")
    print("   1. Asegúrate de tener Python 3.8+")
    print("   2. Ejecuta: pip install streamlit pandas")
    print("   3. Verifica que todos los archivos estén presentes")
    print("="*50 + "\n")

def main():
    """Función principal de ejecución"""
    
    try:
        # Mostrar ayuda
        mostrar_ayuda()
        
        # Verificar estructura
        if not verificar_estructura():
            sys.exit(1)
        
        # Verificar dependencias
        if not verificar_dependencias():
            sys.exit(1)
        
        # Crear archivo de configuración
        crear_archivo_configuracion()
        
        # Abrir navegador después de 2 segundos
        Timer(2, abrir_navegador).start()
        
        # Ejecutar Streamlit
        print("\n⏳ Iniciando servidor Streamlit...")
        subprocess.run(["streamlit", "run", "app.py"])
        
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("\n💡 Solución de problemas:")
        print("   - Verifica que tengas permisos de escritura")
        print("   - Intenta ejecutar como administrador")
        print("   - Revisa que los archivos no estén corruptos")

if __name__ == "__main__":
    main()