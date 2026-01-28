import streamlit as st

st.set_page_config(
    page_title="Mi primera app",
    page_icon="🚀"
)

st.title("🚀 Mi primera app")
st.write("Creada desde una tablet Android, sin instalar nada.")

nombre = st.text_input("¿Cómo te llamas?")

if nombre:
    st.success(f"Bienvenido {nombre}, esto ya es una app real 💥")
    import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="📓 Diario de Trading",
    page_icon="📈",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.write("Registra tus operaciones como un trader profesional.")

ARCHIVO_DATOS = "diario_trading.csv"

# ---------------- CARGA DE DATOS ----------------
if os.path.exists(ARCHIVO_DATOS):
    df = pd.read_csv(ARCHIVO_DATOS)
else:
    df = pd.DataFrame(columns=[
        "fecha",
        "hora",
        "mercado",
        "instrumento",
        "direccion",
        "tipo_orden",
        "riesgo_beneficio",
        "resultado",
        "comision",
        "estrategia",
        "motivo_entrada",
        "emociones_positivas",
        "emociones_negativas",
        "errores",
        "comentarios"
    ])

# ---------------- FORMULARIO ----------------
st.subheader("📝 Nueva operación")

with st.form("form_trading"):
    fecha = st.date_input("Fecha", value=date.today())
    hora = st.time_input("Hora", value=datetime.now().time())

    mercado = st.text_input("Mercado (Forex, Futuros, Crypto, etc)")
    instrumento = st.text_input("Instrumento (EURUSD, SP500, BTC, etc)")

    direccion = st.selectbox("Dirección", ["Largo", "Corto"])
    tipo_orden = st.text_input("Tipo de orden (Market, Limit, etc)")

    riesgo_beneficio = st.text_input("Riesgo / Beneficio (ej: 1:2)")
    resultado = st.text_input("Resultado (pips, ticks o $)")
    comision = st.text_input("Comisión / Spread")

    estrategia = st.text_input("Estrategia")
    motivo_entrada = st.text_area("Motivo de la entrada")

    emociones_positivas = st.text_input("Emociones positivas")
    emociones_negativas = st.text_input("Emociones negativas")

    errores = st.text_area("Errores detectados")
    comentarios = st.text_area("Comentarios adicionales")

    guardar = st.form_submit_button("💾 Guardar operación")

# ---------------- GUARDAR ----------------
if guardar:
    nueva_fila = {
        "fecha": fecha,
        "hora": hora,
        "mercado": mercado,
        "instrumento": instrumento,
        "direccion": direccion,
        "tipo_orden": tipo_orden,
        "riesgo_beneficio": riesgo_beneficio,
        "resultado": resultado,
        "comision": comision,
        "estrategia": estrategia,
        "motivo_entrada": motivo_entrada,
        "emociones_positivas": emociones_positivas,
        "emociones_negativas": emociones_negativas,
        "errores": errores,
        "comentarios": comentarios
    }

    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(ARCHIVO_DATOS, index=False)

    st.success("✅ Operación guardada correctamente")

# ---------------- HISTORIAL ----------------
st.subheader("📊 Historial de operaciones")

if df.empty:
    st.info("Aún no hay operaciones registradas.")
else:
    st.dataframe(df, use_container_width=True)

