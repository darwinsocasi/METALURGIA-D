import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Metalúrgica Data", page_icon="⛏️", layout="wide")

st.title("⛏️ Metalúrgica Data - Panel de Análisis y Simulación")
st.write("Plataforma interactiva para la gestión de datos minero-metalúrgicos (MINEM 2021-2025).")

# Verificar si la carpeta datasets existe y listar archivos disponibles
datasets_path = "datasets"
if os.path.exists(datasets_path):
    st.sidebar.success("📂 Carpeta 'datasets' conectada correctamente.")
    archivos = os.listdir(datasets_path)
    archivo_seleccionado = st.sidebar.selectbox("Selecciona un dataset:", archivos)

    if archivo_seleccionado:
        st.info( visualizing file info... )
        st.write(f"Archivo activo: **{archivo_seleccionado}**")
else:
    st.warning("⚠️ No se encontró la carpeta 'datasets' en la raíz del repositorio.")

st.markdown("---")
st.caption("Desarrollado para la gestión de confiabilidad y analítica industrial.")
