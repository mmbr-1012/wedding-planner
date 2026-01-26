# Style/styles.py
# Estilos CSS y colores para la interfaz

import streamlit as st
from Logic.config import ColorPaleta, ConfiguracionApp

def aplicar_estilos():
    """Aplica todos los estilos CSS personalizados a la aplicación"""
    st.markdown(f"""
    <style>
        /* ==================== ESTILOS GENERALES ==================== */
        .stApp {{
            background: linear-gradient(135deg, {ColorPaleta.BLANCO_NIEVE.value} 0%, {ColorPaleta.ROSADO_PASTEL.value} 100%);
        }}
        
        /* ==================== TARJETAS ==================== */
        .wedding-card {{
            background-color: {ColorPaleta.BLANCO_NIEVE.value};
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border-left: 6px solid {ColorPaleta.DORADO_OPACO.value};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .wedding-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, {ColorPaleta.BLANCO_NIEVE.value} 0%, {ColorPaleta.ROSADO_PASTEL.value} 100%);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid {ColorPaleta.DORADO_SUAVE.value};
        }}
        
        .package-card {{
            background-color: {ColorPaleta.BLANCO_NIEVE.value};
            border-radius: 15px;
            padding: 25px;
            margin: 15px;
            border: 3px solid {ColorPaleta.ROSADO_PROFUNDO.value};
            box-shadow: 0 4px 8px rgba(0,0,0,0.12);
            transition: all 0.3s ease;
        }}
        
        .package-card:hover {{
            border-color: {ColorPaleta.DORADO_SUAVE.value};
            transform: scale(1.02);
        }}
        
        /* ==================== TÍTULOS ==================== */
        h1 {{
            color: {ColorPaleta.DORADO_OPACO.value} !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            font-weight: 700 !important;
        }}
        
        h2, h3 {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 600 !important;
        }}
        
        /* ==================== BOTONES ==================== */
        .stButton > button {{
            background: linear-gradient(135deg, {ColorPaleta.ROSADO_SUAVE.value} 0%, {ColorPaleta.ROSADO_PROFUNDO.value} 100%);
            color: {ColorPaleta.NEGRO.value} !important;
            font-weight: 600 !important;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, {ColorPaleta.ROSADO_PROFUNDO.value} 0%, {ColorPaleta.ROJO_PASTEL.value} 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        /* ==================== INPUTS ==================== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
        }}
        
        .stSelectbox > div > div {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
        }}
        
        .stMultiSelect > div > div {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
        }}
        
        /* ==================== TEXTO ==================== */
        p, li, span, label {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 500 !important;
        }}
        
        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {ColorPaleta.BLANCO_NIEVE.value} 0%, {ColorPaleta.ROSADO_PASTEL.value} 100%);
        }}
        
        [data-testid="stSidebar"] p {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
        }}
        
        /* Radio buttons en sidebar */
        [data-testid="stSidebar"] .stRadio > label {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 600 !important;
        }}
        
        /* ==================== ALERTAS ==================== */
        .stAlert {{
            border-radius: 10px;
            font-weight: 500;
        }}
        
        .stSuccess {{
            background-color: #d4edda !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            border: 2px solid #28a745 !important;
        }}
        
        .stInfo {{
            background-color: #d1ecf1 !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            border: 2px solid #17a2b8 !important;
        }}
        
        .stWarning {{
            background-color: #fff3cd !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            border: 2px solid #ffc107 !important;
        }}
        
        .stError {{
            background-color: #f8d7da !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            border: 2px solid #dc3545 !important;
        }}
        
        /* ==================== EXPANDER ==================== */
        .streamlit-expanderHeader {{
            background-color: {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
        }}
        
        /* ==================== DATAFRAMES ==================== */
        .dataframe {{
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value} !important;
            border-radius: 10px !important;
        }}
        
        .dataframe th {{
            background-color: {ColorPaleta.ROSADO_PASTEL.value} !important;
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 600 !important;
        }}
        
        /* ==================== TABS ==================== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {ColorPaleta.ROSADO_PASTEL.value};
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 600 !important;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {ColorPaleta.ROSADO_PROFUNDO.value} !important;
        }}
        
        /* ==================== MÉTRICAS ==================== */
        [data-testid="stMetricValue"] {{
            color: {ColorPaleta.DORADO_OPACO.value} !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 600 !important;
        }}
        
        /* ==================== FORMULARIOS ==================== */
        .stForm {{
            background-color: {ColorPaleta.BLANCO_NIEVE.value};
            border: 2px solid {ColorPaleta.ROSADO_PASTEL.value};
            border-radius: 10px;
            padding: 20px;
        }}
        
        /* ==================== CHECKBOX Y RADIO ==================== */
        .stCheckbox > label {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 500 !important;
        }}
        
        .stRadio > label {{
            color: {ColorPaleta.GRIS_OSCURO.value} !important;
            font-weight: 500 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def crear_cabecera_pagina(titulo: str, icono: str = "💍"):
    """Crea una cabecera estilizada para cada página"""
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; margin-bottom: 30px;">
        <h1 style="color: {ColorPaleta.DORADO_OPACO.value}; font-size: 3rem;">
            {icono} {titulo}
        </h1>
        <hr style="border: 2px solid {ColorPaleta.DORADO_SUAVE.value}; width: 50%; margin: 20px auto;">
    </div>
    """, unsafe_allow_html=True)

def crear_tarjeta_metrica(titulo: str, valor: str, icono: str = "📊"):
    """Crea una tarjeta de métrica personalizada"""
    return f"""
    <div class="metric-card">
        <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">{icono} {titulo}</h3>
        <h1 style="color: {ColorPaleta.GRIS_OSCURO.value};">{valor}</h1>
    </div>
    """

def crear_tarjeta_paquete(nombre: str, precio: float, descripcion: str, items: list):
    """Crea una tarjeta de paquete personalizada"""
    items_html = "".join([f"<li>{item}</li>" for item in items])
    return f"""
    <div class="package-card">
        <h3 style="color: {ColorPaleta.DORADO_OPACO.value};">💎 {nombre}</h3>
        <h2 style="color: {ColorPaleta.GRIS_OSCURO.value};">${precio:,}</h2>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value};"><strong>{descripcion}</strong></p>
        <hr>
        <p style="color: {ColorPaleta.GRIS_OSCURO.value};"><strong>Incluye:</strong></p>
        <ul style="text-align: left; color: {ColorPaleta.GRIS_OSCURO.value};">
            {items_html}
        </ul>
    </div>
    """

def mostrar_mensaje_exito(mensaje: str):
    """Muestra un mensaje de éxito estilizado"""
    st.markdown(f"""
    <div style="background-color: #d4edda; border: 2px solid #28a745; 
                border-radius: 10px; padding: 15px; margin: 10px 0;">
        <p style="color: #155724; font-weight: 600; margin: 0;">✅ {mensaje}</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_mensaje_error(mensaje: str):
    """Muestra un mensaje de error estilizado"""
    st.markdown(f"""
    <div style="background-color: #f8d7da; border: 2px solid #dc3545; 
                border-radius: 10px; padding: 15px; margin: 10px 0;">
        <p style="color: #721c24; font-weight: 600; margin: 0;">❌ {mensaje}</p>
    </div>
    """, unsafe_allow_html=True)

def crear_divisor():
    """Crea un divisor decorativo"""
    st.markdown(f"""
    <hr style="border: none; height: 2px; 
               background: linear-gradient(to right, 
               {ColorPaleta.ROSADO_PASTEL.value}, 
               {ColorPaleta.DORADO_SUAVE.value}, 
               {ColorPaleta.ROSADO_PASTEL.value}); 
               margin: 30px 0;">
    """, unsafe_allow_html=True)