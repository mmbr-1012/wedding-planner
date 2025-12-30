💍 Dream Wedding Planner

Un sistema completo de planificación y gestión de bodas desarrollado con Python y Streamlit. Perfecto para organizadores de bodas profesionales o parejas que planean su día especial.

✨ Características
🎯 Módulos Principales
Módulo	Descripción	Icono
Dashboard	Panel de control con métricas en tiempo real	📊
Calculadora	Estimador de presupuestos personalizados	💰
Planificador	Creación y gestión de bodas	💒
Temas	6 estilos de boda predefinidos	🎨
Calendario	Agenda interactiva de eventos	📅
Recursos	Gestión de locaciones y personal	🏛️
Estadísticas	Análisis y reportes	📈
Configuración	Personalización del sistema	⚙️
💼 Paquetes Predefinidos
Boda Pequeña ($15,000): 50-80 personas, ceremonia íntima

Boda Mediana ($30,000): 80-150 personas, ceremonia premium

Boda Grande ($60,000): 150-300 personas, experiencia de lujo

🎨 Estilos de Boda
Romántico Vintage - Flores vintage, candelabros

Boho Chic - Macramé, elementos naturales

Moderno Minimalista - Líneas limpias, geometrías

Glamour - Cristales, espejos, brillos

Rústico - Madera natural, hierro

Playero - Conchas, arena, velas

🚀 Comenzar
Prerrequisitos
Python 3.8+

pip (gestor de paquetes de Python)

Instalación
Clonar repositorio

bash
git clone https://github.com/tu-usuario/wedding-planner.git
cd wedding-planner
Instalar dependencias

bash
pip install -r requirements.txt
Ejecutar aplicación

bash
streamlit run run.py
Abrir en navegador

text
http://localhost:8501
Archivo requirements.txt
txt
streamlit==1.32.0
pandas==2.2.0
plotly==5.19.0

📁 Estructura del Proyecto
text
wedding-planner/
├── app_streamlit.py          # Aplicación principal (Streamlit)
├── wedding_manager.py        # Lógica de negocio y gestión
├── budget_calculator.py      # Cálculo de presupuestos
├── data_handler.py           # Manejo de datos (JSON)
├── config.py                 # Configuraciones y temas
├── __init__.py              # Inicialización del paquete
├── requirements.txt         # Dependencias de Python
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados por Git

🛠️ Tecnologías
Tecnología	Versión	Uso
Streamlit	1.32+	Interfaz web interactiva
Python	3.8+	Backend y lógica
Pandas	2.2+	Manipulación de datos
Plotly	5.19+	Gráficos interactivos
JSON	-	Persistencia de datos

📊 Funcionalidades Técnicas
Gestión de Datos
✅ Persistencia en archivos JSON

✅ Sistema de backup automático

✅ Validación de restricciones

✅ Manejo de conflictos de recursos

Interfaz de Usuario
✅ Dashboard con métricas en tiempo real

✅ Calculadora de presupuesto paso a paso

✅ Selector de temas con vista previa

✅ Calendario interactivo

✅ Tablas de recursos filtrables

Lógica de Negocio
✅ Sistema de restricciones entre recursos

✅ Validación de disponibilidad

✅ Cálculo automático de costos

✅ Gestión de estados (pendiente, confirmado, etc.)

🤝 Contribuir
Las contribuciones son bienvenidas. Por favor sigue estos pasos:

Fork el proyecto

Crea una rama (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request
