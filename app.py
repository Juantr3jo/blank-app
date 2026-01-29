import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# ================= CONFIG =================
ZONA_HORARIA = pytz.timezone("America/Santiago")
ARCHIVO = "diario_trading.csv"

st.set_page_config(
    page_title="Diario de Trading",
    page_icon="📓",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.caption("Registro simple y estable para estrategias W y M.")

ahora = datetime.now(ZONA_HORARIA)

# ================= OPCIONES =================
PATRONES = ["W", "M"]
SETUPS = ["Ruptura de base", "Segundo impulso", "Tercer impulso"]
EJECUCIONES = ["Agresivo", "Conservador"]
DIRECCIONES = ["Largo", "Corto"]
RESULTADOS = ["Win", "Loss", "BE"]

# ================= COLUMNAS =================
COLUMNAS = [
    "fecha",
    "hora",
    "patron",
    "setup",
    "ejecucion",
    "direccion",
    "entrada",
    "salida",
    "resultado",
    "comentario"
]

# ================= CARGA SEGURA =================
if os.path.exists(ARCHIVO):
    df = pd.read_csv(ARCHIVO)
    for col in COLUMNAS:
        if col not in df.columns:
            df[col] = ""
    df = df[COLUMNAS]
else:
    df = pd.DataFrame(columns=COLUMNAS)

# ================= FORMULARIO =================
st.subheader("📝 Nuevo trade")

with st.form("nuevo_trade"):

    fecha = st.date_input("Fecha", value=ahora.date())
    hora = st.time_input(
        "Hora (Santiago)",
        value=ahora.time().replace(second=0, microsecond=0)
    )

    patron = st.selectbox("Patrón", PATRONES)
    setup = st.selectbox("Setup", SETUPS)
    ejecucion = st.selectbox("Ejecución", EJECUCIONES)
    direccion = st.selectbox("Dirección", DIRECCIONES)

    entrada = st.number_input("Precio de entrada", format="%.2f")
    salida = st.number_input("Precio de salida", format="%.2f")

    resultado = st.selectbox("Resultado", RESULTADOS)
    comentario = st.text_area("Comentario (opcional)")

    guardar = st.form_submit_button("💾 Guardar trade")

if guardar:
    nueva_fila = {
        "fecha": fecha.isoformat(),
        "hora": hora.strftime("%H:%M"),
        "patron": patron,
        "setup": setup,
        "ejecucion": ejecucion,
        "direccion": direccion,
        "entrada": entrada,
        "salida": salida,
        "resultado": resultado,
        "comentario": comentario
    }

    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(ARCHIVO, index=False)
    st.success("✅ Trade guardado")

# ================= HISTORIAL =================
st.subheader("📊 Historial")

if df.empty:
    st.info("No hay trades registrados.")
else:
    st.dataframe(df, use_container_width=True)

# ================= ELIMINAR =================
st.subheader("🗑️ Eliminar trade")

if not df.empty:
    df_reset = df.reset_index(drop=True)

    opciones = [
        f"{i} | {row['fecha']} | {row['patron']} | {row['setup']}"
        for i, row in df_reset.iterrows()
    ]

    idx = st.selectbox(
        "Selecciona un trade",
        range(len(opciones)),
        format_func=lambda x: opciones[x]
    )

    if st.button("❌ Eliminar trade"):
        df = df.drop(df.index[idx])
        df.to_csv(ARCHIVO, index=False)
        st.success("🗑️ Trade eliminado")
        st.experimental_rerun()

# ================= DESCARGA =================
st.subheader("⬇️ Exportar")

st.download_button(
    "Descargar CSV",
    df.to_csv(index=False),
    file_name="diario_trading.csv",
    mime="text/csv"
)
