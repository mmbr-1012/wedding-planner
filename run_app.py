import subprocess
import sys
import os

def create_directories():
    """Crea las carpetas necesarias si no existen"""
    directories = ["logic", "data"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Carpeta creada/verificada: {directory}/")

def install_requirements():
    """Instala los requisitos necesarios"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError:
        print("⚠️ Error al instalar dependencias. Instalando manualmente...")
        packages = ["streamlit", "pandas", "plotly"]
        for package in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} instalado")
            except:
                print(f"❌ Error instalando {package}")

def check_data_files():
    """Verifica que existan los archivos de datos necesarios"""
    data_files = ["data/wedding_data.json"]
    
    for file in data_files:
        if not os.path.exists(file):
            print(f"⚠️ {file} no encontrado - Creando archivo básico...")
            create_basic_data_file(file)
    
    print("✅ Archivos de datos verificados")

def create_basic_data_file(file_path):
    """Crea un archivo de datos básico"""
    import json
    basic_data = {
        "recursos": [],
        "eventos": [],
        "restricciones": []
    }
    
    with open(file_path, "w") as f:
        json.dump(basic_data, f, indent=2)
    
    print(f"✅ Archivo de datos básico creado: {file_path}")

def run_streamlit():
    """Ejecuta la aplicación Streamlit"""
    print("\n" + "="*50)
    print("🚀 INICIANDO DREAM WEDDING PLANNER")
    print("="*50)
    print("\n🌐 La aplicación se abrirá en tu navegador...")
    print("📱 URL: http://localhost:8501")
    print("\n💡 Si no se abre automáticamente:")
    print("   1. Abre tu navegador web")
    print("   2. Ve a http://localhost:8501")
    print("   3. O presiona Ctrl+Click en el enlace de arriba")
    print("\n🔄 Para detener la aplicación: Ctrl+C")
    print("="*50 + "\n")
    
    subprocess.run(["streamlit", "run", "app_streamlit.py"])

if __name__ == "__main__":
    try:
        # Crear estructura de carpetas
        create_directories()
        
        # Verificar archivos de datos
        check_data_files()
        
        # Instalar dependencias
        install_requirements()
        
        # Ejecutar aplicación
        run_streamlit()
        
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Solución de problemas:")
        print("   1. Asegúrate de tener Python 3.8+ instalado")
        print("   2. Intenta instalar manualmente: pip install streamlit pandas plotly")
        sys.exit(1)