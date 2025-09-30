
import streamlit as st
import pandas as pd
from pathlib import Path

IVA = 0.21

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

def obtener_ruta_imagen(codigo):
    carpeta = Path("imagenes")
    extensiones = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
    for ext in extensiones:
        ruta = carpeta / f"{codigo}{ext}"
        if ruta.exists():
            return str(ruta)
    return None

if "carrito" not in st.session_state:
    st.session_state.carrito = []

df = cargar_datos()
st.title("🗂️ Catálogo de Productos")

familias_dict = {
    1: "Quimicos",
    2: "Celulosas",
    3: "Útiles",
    4: "Desechables",
    5: "Equipamiento",
    6: "Maquinas",
    7: "Alquiler",
    9: "Servicios"
}

if "familia_seleccionada" not in st.session_state:
    st.markdown("## Selecciona una familia para comenzar")
    cols = st.columns(2)
    for idx, (numero, nombre) in enumerate(familias_dict.items()):
        col = cols[idx % 2]
        with col:
            ruta_img = f"imagenes/familia_{numero}.png"
            st.image(ruta_img, use_column_width=True)
            if st.button(nombre, key=f"familia_{numero}"):
                st.session_state.familia_seleccionada = nombre
    st.stop()

# Mostrar productos por subfamilia tras seleccionar familia
familia = st.session_state.familia_seleccionada
subfamilias = df[df["Familia"] == familia]["Subfamilia"].dropna().unique()
subfamilias = sorted([s for s in subfamilias if isinstance(s, str)])
subfamilia_seleccionada = st.selectbox("Selecciona una subfamilia:", subfamilias)

productos = df[(df["Familia"] == familia) & (df["Subfamilia"] == subfamilia_seleccionada)]
st.markdown(f"### Productos en: {familia} / {subfamilia_seleccionada}")

for _, fila in productos.iterrows():
    st.markdown(f"**{fila['Nombre']}**")
    precio_con_iva = float(fila["Precio"])
    precio_sin_iva = precio_con_iva / (1 + IVA)
    st.markdown(f"💶 Precio sin IVA: {precio_sin_iva:.2f} € | 💰 Precio con IVA: {precio_con_iva:.2f} €")

    imagen = obtener_ruta_imagen(fila["Codigo"])
    if imagen:
        st.image(imagen, use_container_width=True)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        cantidad = st.number_input(f"Cantidad ({fila['Codigo']})", min_value=1, max_value=1000, value=1, key=f"cantidad_{fila['Codigo']}")
    with col2:
        tipo = st.selectbox("Formato", ["unidades", "cajas", "paquetes"], key=f"tipo_{fila['Codigo']}")
    with col3:
        if st.button("➕ Añadir al pedido", key=f"add_{fila['Codigo']}"):
            st.session_state.carrito.append({
                "Codigo": fila["Codigo"],
                "Nombre": fila["Nombre"],
                "Cantidad": cantidad,
                "Tipo": tipo,
                "Precio": precio_con_iva
            })
            st.success(f"{cantidad} {tipo} de '{fila['Nombre']}' añadido al pedido.")
    st.markdown("---")

# Mostrar resumen del carrito
if st.session_state.carrito:
    st.markdown("## 🛒 Resumen del Pedido")
    total = 0
    for item in st.session_state.carrito:
        subtotal = item["Cantidad"] * item["Precio"]
        total += subtotal
        st.markdown(f"- {item['Cantidad']} {item['Tipo']} de **{item['Nombre']}** → {subtotal:.2f} €")
    st.markdown(f"**Total del pedido: {total:.2f} € (IVA incluido)**")
else:
    st.info("No hay productos en el pedido.")
