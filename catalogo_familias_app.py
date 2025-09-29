
import streamlit as st
import pandas as pd
from pathlib import Path

# Cargar datos desde Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("Artículos con familia.xlsx")
    df = df.rename(columns={
        "CÓDIGO": "Codigo",
        "NOMBRE": "Nombre",
        "PRECIO": "Precio",
        "FAMILIA": "Familia",
        "SUBFAMILIA": "Subfamilia"
    })
    df["Familia"] = df["Familia"].fillna("Sin familia")
    df["Subfamilia"] = df["Subfamilia"].fillna("Otros")
    return df

df = cargar_datos()

st.title("🗂️ Catálogo de Productos por Familias")

familias = df["Familia"].dropna().unique()
familia_seleccionada = st.selectbox("Selecciona una familia:", sorted(familias))

if familia_seleccionada:
    subfamilias = df[df["Familia"] == familia_seleccionada]["Subfamilia"].dropna().unique()
    subfamilia_seleccionada = st.selectbox("Selecciona una subfamilia:", sorted(subfamilias))

    if subfamilia_seleccionada:
        productos = df[(df["Familia"] == familia_seleccionada) & (df["Subfamilia"] == subfamilia_seleccionada)]
        st.markdown(f"### Productos en: {familia_seleccionada} / {subfamilia_seleccionada}")

        for _, fila in productos.iterrows():
            st.markdown(f"**{fila['Nombre']}** - {fila['Precio']:.2f} €")
