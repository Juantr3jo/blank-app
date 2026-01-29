import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# ---------------- CONFIG ----------------
ZONA_HORARIA = pytz.timezone("America/Santiago")
ARCHIVO_DATOS = "diario_trading.csv"

st.set_page_config(
    page_title="📓 Diario de Trading",
    page_icon="📈",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.caption("Registro estructurado para mejorar disciplina, edge y estrategia.")

ahora = datetime.now(ZONA_HORARIA)

# ---------------- MODELOS NORMALIZADOS ----------------
ESTRATEGIAS = [
    "WM_EXTREMO"
]

EMOCIONES = [
    "Confianza",
    "Calma",
    "Neutral",
    "FOMO",
    "Miedo",
    "Ansiedad",
    "Impaciencia"
]

ERRORES = [
    "Sin error",
    "Entrada anticipada",
    "Entrada tardía",
    "Stop mal colocado",
    "Mover stop",
    "No respetar plan",
    "Sobreoperar"
]

RESULTADOS = ["Win", "Loss", "BE"]

DIRECCIONES = ["Largo", "Corto"]

MERCADOS = ["Futuros", "Forex", "Crypto", "Índices"]

# ---------------- CARGA DATOS ----------------
columnas = [
    "fecha",
    "hora",
    "mercado",
    "instrumento",
    "direccion",
    "estrategia",
    "resultado",
    "riesgo_beneficio",
    "emocion_principal",
    "error_principal",
    "comentarios"
]

if os.path.exists(ARCHIVO_DATOS):
    df = pd.read_csv(ARCHIVO_DATOS)
else:
    df = pd.DataFrame(columns=columnas)

# ---------------- FORMULARIO ----------------
st.subheader("📝 Nueva operación")

with st.form("form_trading"):

    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input("Fecha", value=ahora.date())

    with col2:
        hora = st.time_input(
            "Hora (Santiago)",
            value=ahora.time().replace(second=0, microsecond=0)
        )

    col3, col4 = st.columns(2)

    with col3:
        mercado = st.selectbox("Mercado", MERCADOS)

    with col4:
        instrumento = st.text_input("Instrumento (ej: ES, NQ, EURUSD)")

    col5, col6 = st.columns(2)

    with col5:
        direccion = st.selectbox("Dirección", DIRECCIONES)

    with col6:
        estrategia = st.selectbox("Estrategia", ESTRATEGIAS)

    col7, col8 = st.columns(2)

    with col7:
        resultado = st.selectbox("Resultado", RESULTADOS)

    with col8:
        riesgo_beneficio = st.selectbox(
            "Riesgo / Beneficio",
            ["1:1", "1:1.5", "1:2", "1:3", "1:4+"]
        )

    col9, col10 = st.columns(2)

    with col9:
        emocion_principal = st.selectbox("Emoción dominante", EMOCIONES)

    with col10:
        error_principal = st.selectbox("Error principal", ERRORES)

    comentarios = st.text_area(
        "Comentarios (opcional, solo contexto)",
        placeholder="Ej: entrada válida pero ejecutada tarde"
    )

    guardar = st.form_submit_button("💾 Guardar trade")

# ---------------- GUARDAR ----------------
if guardar:
    nueva_fila = {
        "fecha": fecha.isoformat(),
        "hora": hora.strftime("%H:%M"),
        "mercado": mercado,
        "instrumento": instrumento,
        "direccion": direccion,
        "estrategia": estrategia,
        "resultado": resultado,
        "riesgo_beneficio": riesgo_beneficio,
        "emocion_principal": emocion_principal,
        "error_principal": error_principal,
        "comentarios": comentarios
    }

    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(ARCHIVO_DATOS, index=False)

    st.success("✅ Trade guardado correctamente")

# ---------------- HISTORIAL ----------------
st.subheader("📊 Historial")

if df.empty:
    st.info("Aún no hay trades registrados.")
else:
    st.dataframe(df, use_container_width=True)

# ---------------- DESCARGA ----------------
st.subheader("⬇️ Exportar")

st.download_button(
    "📥 Descargar diario (CSV)",
    df.to_csv(index=False),
    file_name="diario_trading.csv",
    mime="text/csv"
)
