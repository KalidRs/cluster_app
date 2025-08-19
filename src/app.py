import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Análisis de Luminarias", layout="wide")
st.title("📊 Distribución de Luminarias por Cluster")

# Ruta al JSON (ajusta según tu estructura de archivos)
json_path = "../data/luminarias.json"

# Cargar datos
@st.cache_data  # Cachear para mejor rendimiento
def load_data():
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

df = load_data()

# Interpretaciones de clusters
cluster_interpretation = {
    0: "Luminarias de alto consumo y baja eficiencia",
    1: "Luminarias eficientes con buen estado",
    2: "Luminarias con problemas de conectividad y mantenimiento"
}

# Mapear clusters y contar
df["cluster_desc"] = df["cluster"].map(cluster_interpretation)
cluster_counts = df["cluster_desc"].value_counts()

# Mostrar datos en Streamlit
st.subheader("Conteo por cluster")
st.dataframe(cluster_counts)

# Crear gráfica con Matplotlib
fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
bars = cluster_counts.plot(
    kind="bar", 
    color=["red", "green", "blue"],
    ax=ax
)
ax.set_title("Distribución de Luminarias por Cluster", fontsize=16)
ax.set_xlabel("Tipo de Cluster", fontsize=12)
ax.set_ylabel("Cantidad de Luminarias", fontsize=12)
plt.xticks(rotation=25, ha='right')  # Rotar etiquetas para mejor legibilidad

# Añadir etiquetas de valor en cada barra
for bar in bars.patches:
    ax.annotate(
        f"{int(bar.get_height())}", 
        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
        ha='center', va='bottom', fontsize=10
    )

plt.tight_layout()

# Mostrar gráfica en Streamlit
st.pyplot(fig)
plt.close(fig)  # Liberar memoria