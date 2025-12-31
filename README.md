# 💍 Dream Wedding Planner v2.0

Un sistema completo de planificación y gestión de bodas desarrollado con Python y Streamlit. Sistema inteligente que gestiona recursos, valida restricciones y encuentra horarios disponibles automáticamente.

---

## ✨ Características Principales

### 🎯 Funcionalidades Core

| Módulo | Descripción | Estado |
|--------|-------------|--------|
| **Dashboard** | Panel de control con métricas en tiempo real | ✅ Implementado |
| **Planificador** | Creación y gestión completa de bodas | ✅ Implementado |
| **Validación de Restricciones** | Sistema automático de validación | ✅ Implementado |
| **Búsqueda de Horarios** | Encuentra horarios disponibles automáticamente | ✅ Implementado |
| **Calculadora** | Estimador de presupuestos personalizados | ✅ Implementado |
| **Gestión de Recursos** | Control completo del inventario | ✅ Implementado |
| **Temas Predefinidos** | 6 estilos de boda personalizables | ✅ Implementado |
| **Persistencia** | Guardado/carga automática en JSON | ✅ Implementado |

---

## 🏗️ Arquitectura del Sistema

### Dominio: Planificación de Bodas

El sistema gestiona tres componentes principales:

#### 1️⃣ **Eventos (Bodas)**
Representan las celebraciones que necesitan ser planificadas:
- Tienen fecha y hora de inicio/fin
- Requieren recursos específicos
- Tienen un presupuesto asociado
- Número de invitados
- Tipo de boda (Pequeña, Mediana, Grande, Personalizada)

**Ejemplo:**
```
Boda: "María & Juan"
Fecha: 15/06/2025 14:00 - 22:00
Invitados: 150
Tipo: Mediana
Presupuesto: $45,000
```

#### 2️⃣ **Recursos**
Inventario de activos necesarios para realizar bodas:

**Tipos de recursos:**
- 🏛️ **Ceremonia**: Lugares para la ceremonia (Jardín, Salón, Capilla, Playa)
- 🎉 **Recepción**: Lugares para la recepción (Salón, Terraza, Jardín Exterior, Carpa)
- 👥 **Personal**: Equipo humano (Coordinador, Fotógrafo, DJ, Chef, Meseros, etc.)
- 🍰 **Catering**: Servicios de comida (Chef, Meseros, Pastelero)
- 🎨 **Decoración**: Florista y elementos decorativos

**Propiedades:**
- ID único
- Nombre descriptivo
- Tipo (Enum)
- Capacidad
- Precio
- Disponibilidad
- Eventos asignados (historial)

#### 3️⃣ **Restricciones**
Reglas que gobiernan cómo los recursos pueden combinarse:

##### 🔗 **Co-requisito (Inclusión)**
Un recurso REQUIERE otro recurso para funcionar.

**Restricciones implementadas:**

```python
Restricción 1: Co-requisito
├── Recurso Principal: Chef Ejecutivo (ID: 9)
└── Recurso Requerido: Equipo de Meseros (ID: 10)
    Razón: El Chef no puede operar sin meseros que sirvan la comida
```

**Ejemplo de validación:**
- ✅ **VÁLIDO**: Seleccionar "Chef Ejecutivo" + "Equipo de Meseros"
- ❌ **INVÁLIDO**: Seleccionar solo "Chef Ejecutivo" sin "Equipo de Meseros"
- ✅ **VÁLIDO**: No seleccionar ninguno de los dos

##### ⛔ **Exclusión Mutua**
Dos recursos NO pueden usarse juntos en el mismo evento.

**Restricciones implementadas:**

```python
Restricción 2: Exclusión
├── Recurso A: Jardín para Ceremonia (ID: 1)
└── Recurso B: Salón Principal (ID: 2)
    Razón: Ambos espacios comparten staff y no pueden operarse simultáneamente

Restricción 3: Exclusión
├── Recurso A: Capilla Privada (ID: 3)
└── Recurso B: Playa Privada (ID: 4)
    Razón: Logística de transporte - solo uno puede usarse por evento
```

**Ejemplo de validación:**
- ✅ **VÁLIDO**: Seleccionar "Jardín para Ceremonia"
- ✅ **VÁLIDO**: Seleccionar "Salón Principal"
- ❌ **INVÁLIDO**: Seleccionar "Jardín para Ceremonia" + "Salón Principal"

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes)

### Paso 1: Clonar o Descargar

```bash
git clone https://github.com/tu-usuario/dream-wedding-planner.git
cd dream-wedding-planner
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de requirements.txt:**
```
streamlit>=1.28.0
pandas>=2.0.0
```

### Paso 3: Ejecutar la Aplicación

**Opción A: Usando run.py (Recomendado)**
```bash
python run.py
```

**Opción B: Directamente con Streamlit**
```bash
streamlit run app.py
```

### Paso 4: Abrir en Navegador
La aplicación se abrirá automáticamente en `http://localhost:8501`

---

## 📂 Estructura del Proyecto

```
dream-wedding-planner/
│
├── Logic/                      # Módulo principal de lógica
│   ├── __init__.py            # Inicialización del paquete
│   ├── models.py              # Modelos de datos (Evento, Recurso, Restriccion)
│   ├── config.py              # Configuración (Temas, Paquetes, Colores)
│   ├── wedding_manager.py    # Gestor principal del sistema
│   ├── budget_calculator.py  # Calculadora de presupuestos
│   └── data_handler.py       # Persistencia de datos (JSON/CSV)
│
├── data/                      # Datos persistentes
│   └── weddings.json         # Base de datos de eventos y recursos
│
├── app.py                    # Interfaz de usuario (Streamlit)
├── run.py                    # Script de ejecución
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── .gitignore               # Archivos ignorados por Git
```

---

## 💻 Uso del Sistema

### 1. Dashboard Principal
- Visualiza estadísticas en tiempo real
- Ve próximas bodas programadas
- Acceso rápido a funciones principales

### 2. Crear Nueva Boda
1. Selecciona un paquete (Pequeña/Mediana/Grande)
2. Completa información de los novios
3. Selecciona fecha, hora y duración
4. Elige recursos (ceremonia, recepción, personal)
5. El sistema valida automáticamente:
   - ✅ Disponibilidad de recursos
   - ✅ Restricciones de co-requisitos
   - ✅ Restricciones de exclusión
   - ✅ Validez de fechas
6. Confirma la boda

**Si hay conflictos:**
- El sistema muestra el error específico
- Ofrece buscar horario alternativo automáticamente

### 3. Buscar Horario Disponible
- Selecciona los recursos que necesitas
- Define la duración del evento
- El sistema busca el próximo horario disponible
- Crea la boda directamente desde ahí

### 4. Calculadora de Presupuesto
- Selecciona servicios y recursos
- Calcula automáticamente:
  - Subtotal
  - Impuestos (16%)
  - Total
- Genera detalles completos del presupuesto

### 5. Explorar Temas
- Visualiza 6 temas predefinidos
- Ve colores, estilos y precios
- Selecciona para crear boda con ese tema

### 6. Gestión de Recursos
- Lista completa de recursos
- Filtros por tipo y disponibilidad
- Ve qué eventos tiene asignado cada recurso
- Estadísticas de ocupación

---

## 🎓 Ejemplos de Uso

### Ejemplo 1: Crear Boda Básica

```python
from Logic import DreamWeddingPlanner
from datetime import datetime, timedelta

planner = DreamWeddingPlanner()

# Crear boda
exito, mensaje, evento_id = planner.crear_evento(
    nombre="Boda Ana & Carlos",
    inicio=datetime(2025, 6, 15, 14, 0),
    fin=datetime(2025, 6, 15, 22, 0),
    recursos=[1, 13, 5, 6, 8],  # Jardín, Salón Recepción, Coordinador, Fotógrafo, DJ
    presupuesto=35000,
    num_invitados=120
)

print(f"Evento ID: {evento_id}")
print(mensaje)
```

### Ejemplo 2: Buscar Horario Disponible

```python
from datetime import timedelta

# Buscar horario para recursos específicos
horario = planner.buscar_horario_disponible(
    recursos=[2, 14, 5, 6],  # Salón, Terraza VIP, Coordinador, Fotógrafo
    duracion=timedelta(hours=8),
    fecha_inicio=datetime(2025, 7, 1)
)

if horario:
    inicio, fin = horario
    print(f"Horario disponible: {inicio} - {fin}")
else:
    print("No hay horarios disponibles")
```

### Ejemplo 3: Validar Restricciones

```python
# Intentar crear evento que viola restricción
recursos_invalidos = [1, 2]  # Jardín + Salón (exclusión mutua)

es_valido, mensaje = planner.validar_restricciones(recursos_invalidos)
print(f"¿Válido?: {es_valido}")
print(f"Mensaje: {mensaje}")
# Output: ¿Válido?: False
# Mensaje: Violación de exclusión: Jardín y Salón no pueden usarse simultáneamente
```

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.8+ | Lenguaje principal |
| **Streamlit** | 1.28+ | Interfaz web interactiva |
| **Pandas** | 2.0+ | Manipulación de datos |
| **JSON** | Built-in | Persistencia de datos |
| **dataclasses** | Built-in | Modelos de datos |
| **Enum** | Built-in | Tipos enumerados |
| **datetime** | Built-in | Gestión de fechas |

---

## 📊 Características Técnicas Avanzadas

### ✅ Sistema de Validación Robusto
- Validación de restricciones automática
- Detección de conflictos de recursos
- Validación de fechas y rangos
- Manejo de errores descriptivo

### 🔍 Búsqueda Inteligente
- Algoritmo de búsqueda de horarios disponibles
- Considera todas las restricciones
- Búsqueda incremental por hora
- Límite de búsqueda configurable

### 💾 Persistencia Completa
- Guardado automático en JSON
- Carga al iniciar la aplicación
- Exportación a CSV
- Generación de reportes

### 🎨 Interfaz Moderna
- Diseño responsivo
- Colores personalizados
- Animaciones suaves
- Alto contraste para legibilidad

---

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'Logic'"

**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd dream-wedding-planner

# Verifica que existe la carpeta Logic con __init__.py
ls Logic/__init__.py

# Si no existe, créala
touch Logic/__init__.py
```

### Problema: "streamlit: command not found"

**Solución:**
```bash
# Instala streamlit
pip install streamlit

# O reinstala todas las dependencias
pip install -r requirements.txt
```

### Problema: "Las letras no se ven en la interfaz"

**Solución:** Ya corregido en v2.0. Los estilos CSS ahora usan colores con alto contraste:
- Textos en gris oscuro (#2C3E50)
- Títulos en dorado (#D4AF37)
- Fondos en blanco y rosado pastel

---

## 📈 Roadmap Futuro

- [ ] Recursos con cantidad (pools)
- [ ] Eventos recurrentes
- [ ] Calendario visual interactivo
- [ ] Notificaciones por email
- [ ] Generación de contratos PDF
- [ ] Dashboard de analytics avanzado
- [ ] App móvil
- [ ] Sistema de pagos integrado

---

## 👥 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 📧 Contacto

**Dream Wedding Planner Team**
- Email: contact@dreamwedding.com
- Web: www.dreamweddingplanner.com

---

## 🎉 Agradecimientos

Gracias por usar Dream Wedding Planner. ¡Que tu boda sea perfecta! 💍✨

---

**Versión:** 2.0.0  
**Última actualización:** Diciembre 2024  
**Estado:** ✅ Producción