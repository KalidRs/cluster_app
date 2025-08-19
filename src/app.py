import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
from pathlib import Path

# Configuración de la página
st.set_page_config(page_title="Análisis de Luminarias", layout="wide")
st.title("📊 Distribución de Luminarias por Cluster")

# --- SOLUCIÓN CLAVE: Ruta compatible con local y cloud ---
current_dir = Path(__file__).parent.absolute()
json_path = os.path.join(current_dir, "..", "data", "luminarias.json")

# Verificación del archivo (crítico para debug)
if not os.path.exists(json_path):
    st.error(f"❌ Error: Archivo no encontrado en la ruta: {json_path}")
    st.stop()  # Detiene la ejecución si no existe el archivo
else:
    st.success(f"✅ Archivo encontrado correctamente en: {json_path}")

# Cargar datos con manejo de errores
@st.cache_data
def load_data():
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return pd.DataFrame()  # Retorna DataFrame vacío en caso de error

df = load_data()

# Verificar si los datos se cargaron
if df.empty:
    st.warning("No hay datos para mostrar. Verifica el archivo JSON.")
    st.stop()

# Interpretaciones de clusters
cluster_interpretation = {
    0: "Luminarias de alto consumo y baja eficiencia",
    1: "Luminarias eficientes con buen estado",
    2: "Luminarias con problemas de conectividad y mantenimiento"
}

# Procesamiento de datos
df["cluster_desc"] = df["cluster"].map(cluster_interpretation)
cluster_counts = df["cluster_desc"].value_counts()

# Mostrar datos
st.subheader("Conteo por cluster")
st.dataframe(cluster_counts)

# Crear gráfica con verificación
if not cluster_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    bars = cluster_counts.plot(
        kind="bar", 
        color=["red", "green", "blue"],
        ax=ax
    )
    ax.set_title("Distribución de Luminarias por Cluster", fontsize=16)
    ax.set_xlabel("Tipo de Cluster", fontsize=12)
    ax.set_ylabel("Cantidad de Luminarias", fontsize=12)
    plt.xticks(rotation=25, ha='right')
    
    # Etiquetas de valores
    for bar in bars.patches:
        ax.annotate(
            f"{int(bar.get_height())}", 
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha='center', va='bottom', fontsize=10
        )
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("No hay datos suficientes para generar el gráfico.")