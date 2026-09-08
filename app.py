import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Metalúrgica Data - Panel Analítico", page_icon="⛏️", layout="wide"
)

st.title("⛏️ Metalúrgica Data - Panel de Análisis y Simulación")
st.markdown(
    "Plataforma interactiva para la gestión, análisis y visualización de"
    " datos minero-metalúrgicos (MINEM 2021-2025)."
)

datasets_path = "datasets"

if os.path.exists(datasets_path):
  st.sidebar.success("📂 Carpeta 'datasets' conectada correctamente.")

  # Listar subcarpetas dentro de datasets
  elementos = os.listdir(datasets_path)
  subcarpetas = [
      e
      for e in elementos
      if os.path.isdir(os.path.join(datasets_path, e)) and not e.startswith(".")
  ]

  if subcarpetas:
    subfolder_seleccionada = st.sidebar.selectbox(
        "📁 Selecciona la categoría de proceso:", subcarpetas
    )

    ruta_subfolder = os.path.join(datasets_path, subfolder_seleccionada)
    archivos_en_subfolder = os.listdir(ruta_subfolder)

    archivos_validos = [
        f
        for f in archivos_en_subfolder
        if f.lower().endswith((".csv", ".xlsx", ".xls"))
    ]

    if archivos_validos:
      archivo_seleccionado = st.sidebar.selectbox(
          "📊 Selecciona el dataset:", archivos_validos
      )

      if archivo_seleccionado:
        ruta_archivo = os.path.join(ruta_subfolder, archivo_seleccionado)
        st.info(
            f"Visualizando: **{subfolder_seleccionada}** /"
            f" *{archivo_seleccionado}*"
        )

        try:
          if archivo_seleccionado.lower().endswith(".csv"):
            df = pd.read_csv(ruta_archivo)
          else:
            df = pd.read_excel(ruta_archivo)

          col1, col2, col3 = st.columns(3)
          with col1:
            st.metric("Registros (Filas)", f"{df.shape[0]:,}")
          with col2:
            st.metric("Variables (Columnas)", df.shape[1])
          with col3:
            st.metric("Valores Nulos", int(df.isnull().sum().sum()))

          st.subheader("📋 Vista Previa del Dataset")
          st.dataframe(df.head(50), use_container_width=True)

          st.subheader("📊 Estadísticas Descriptivas")
          st.write(df.describe())

          columnas_num = df.select_dtypes(
              include=["float64", "int64"]
          ).columns.tolist()
          if len(columnas_num) >= 1:
            st.subheader("📈 Visualización Interactiva de Tendencias")
            col_x = st.selectbox(
                "Selecciona la variable para el Eje X:", df.columns
            )
            col_y = st.selectbox(
                "Selecciona la variable numérica para el Eje Y:", columnas_num
            )

            try:
              st.line_chart(df[[col_x, col_y]].set_index(col_x))
            except Exception:
              st.bar_chart(df[[col_x, col_y]].set_index(col_x))

        except Exception as e:
          st.error(f"Ocurrió un error al procesar el archivo: {e}")
    else:
      st.sidebar.warning(
          f"La carpeta '{subfolder_seleccionada}' no contiene archivos .csv o"
          " .xlsx compatibles directamente."
      )
  else:
    st.sidebar.warning(
        "No se encontraron subcarpetas de categorías en 'datasets'."
    )
else:
  st.warning("⚠️ No se encontró la carpeta 'datasets' en la raíz del repositorio.")

st.markdown("---")
st.caption(
    "Desarrollado para la ingeniería de confiabilidad y analítica industrial |"
    " IASEMP"
)
