import os
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Metalúrgica Data - Panel Analítico", page_icon="⛏️", layout="wide"
)

st.title("⛏️ Metalúrgica Data - Panel de Análisis y Simulación")
st.markdown(
    "Plataforma interactiva para la gestión, análisis y visualización de"
    " datos minero-metalúrgicos (MINEM 2021-2025)."
)

# Directorio de datasets
datasets_path = "datasets"

if os.path.exists(datasets_path):
  st.sidebar.success("📂 Carpeta 'datasets' conectada correctamente.")
  archivos = os.listdir(datasets_path)

  # Filtrar formatos compatibles
  archivos_validos = [
      f for f in archivos if f.endswith((".csv", ".xlsx", ".xls"))
  ]

  if archivos_validos:
    archivo_seleccionado = st.sidebar.selectbox(
        "Selecciona un dataset disponible:", archivos_validos
    )

    if archivo_seleccionado:
      ruta_archivo = os.path.join(datasets_path, archivo_seleccionado)
      st.info(f"Visualizando información del archivo: {archivo_seleccionado}")

      try:
        # Cargar datos según la extensión del archivo
        if archivo_seleccionado.endswith(".csv"):
          df = pd.read_csv(ruta_archivo)
        else:
          df = pd.read_excel(ruta_archivo)

        # Métricas generales del dataset
        col1, col2, col3 = st.columns(3)
        with col1:
          st.metric("Registros (Filas)", f"{df.shape[0]:,}")
        with col2:
          st.metric("Variables (Columnas)", df.shape[1])
        with col3:
          st.metric("Valores Nulos", int(df.isnull().sum().sum()))

        # Vista previa de los datos
        st.subheader("📋 Vista Previa del Dataset")
        st.dataframe(df.head(50), use_container_width=True)

        # Estadísticas descriptivas
        st.subheader("📊 Estadísticas Descriptivas")
        st.write(df.describe())

        # Sección de gráficos interactivos rápidos
        columnas_num = df.select_dtypes(
            include=["float64", "int64"]
        ).columns.tolist()
        if len(columnas_num) >= 1:
          st.subheader("📈 Visualización Interactiva de Tendencias")
          col_x = st.selectbox("Selecciona la variable para el Eje X:", df.columns)
          col_y = st.selectbox(
              "Selecciona la variable numérica para el Eje Y:", columnas_num
          )

          try:
            st.line_chart(df[[col_x, col_y]].set_index(col_x))
          except Exception:
            st.bar_chart(df[[col_x, col_y]].set_index(col_x))

      except Exception as e:
        st.error(
            f"Ocurrió un error al procesar el archivo seleccionado: {e}"
        )
  else:
    st.sidebar.warning(
        "No se encontraron archivos compatibles (.csv, .xlsx) en la carpeta"
        " 'datasets'."
    )
else:
  st.warning(
      "⚠️ No se encontró la carpeta 'datasets' en la raíz del repositorio."
      " Asegúrate de subirla."
  )

st.markdown("---")
st.caption(
    "Desarrollado para la ingeniería de confiabilidad, optimización de"
    " procesos y analítica industrial | IASEMP"
)
