import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import os
import pytz

# ---------------- CONFIGURACIÓN GENERAL ----------------
ZONA_HORARIA = pytz.timezone("America/Santiago")
ARCHIVO_DATOS = "diario_trading.csv"

st.set_page_config(
    page_title="📓 Diario de Trading",
    page_icon="📈",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.caption("Sistema personal para mejorar decisiones, disciplina y estrategia.")

# ---------------- FECHA Y HORA (SANTIAGO) ----------------
ahora_santiago = datetime.now(ZONA_HORARIA)

# ---------------- CARGA / INICIALIZACIÓN DE DATOS ----------------
columnas = [
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
]

if os.path.exists(ARCHIVO_DATOS):
    df = pd.read_csv(ARCHIVO_DATOS)
else:
    df = pd.DataFrame(columns=columnas)

# ---------------- FORMULARIO ----------------
st.subheader("📝 Registrar nueva operación")

with st.form("form_diario"):

    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input(
            "📅 Fecha",
            value=ahora_santiago.date()
        )

    with col2:
        hora = st.time_input(
            "⏰ Hora (Santiago)",
            value=ahora_santiago.time().replace(second=0, microsecond=0)
        )

    mercado = st.text_input("Mercado (Forex, Futuros, Crypto)")
    instrumento = st.text_input("Instrumento (EURUSD, SP500, BTC, etc)")

    col3, col4 = st.columns(2)

    with col3:
        direccion = st.selectbox("Dirección", ["Largo", "Corto"])

    with col4:
        tipo_orden = st.text_input("Tipo de orden (Market, Limit, etc)")

    riesgo_beneficio = st.text_input("Riesgo / Beneficio (ej: 1:2)")
    resultado = st.text_input("Resultado (pips, ticks o $)")
    comision = st.text_input("Comisión / Spread")

    estrategia = st.text_input("Estrategia utilizada")
    motivo_entrada = st.text_area("Motivo de la entrada")

    emociones_positivas = st.text_input("Emociones positivas")
    emociones_negativas = st.text_input("Emociones negativas")

    errores = st.text_area("Errores detectados")
    comentarios = st.text_area("Comentarios adicionales")

    guardar = st.form_submit_button("💾 Guardar operación")

# ---------------- GUARDADO ----------------
if guardar:
    nueva_operacion = {
        "fecha": fecha.isoformat(),
        "hora": hora.strftime("%H:%M"),
        "mercado": mercado.strip(),
        "instrumento": instrumento.strip(),
        "direccion": direccion,
        "tipo_orden": tipo_orden.strip(),
        "riesgo_beneficio": riesgo_beneficio.strip(),
        "resultado": resultado.strip(),
        "comision": comision.strip(),
        "estrategia": estrategia.strip(),
        "motivo_entrada": motivo_entrada.strip(),
        "emociones_positivas": emociones_positivas.strip(),
        "emociones_negativas": emociones_negativas.strip(),
        "errores": errores.strip(),
        "comentarios": comentarios.strip()
    }

    df = pd.concat([df, pd.DataFrame([nueva_operacion])], ignore_index=True)
    df.to_csv(ARCHIVO_DATOS, index=False)

    st.success("✅ Operación guardada correctamente")

# ---------------- HISTORIAL ----------------
st.subheader("📊 Historial de operaciones")

if df.empty:
    st.info("Aún no hay operaciones registradas.")
else:
    st.dataframe(df, use_container_width=True)

# ---------------- DESCARGA ----------------
st.subheader("⬇️ Exportar diario")

st.download_button(
    label="📥 Descargar diario en CSV",
    data=df.to_csv(index=False),
    file_name="diario_trading.csv",
    mime="text/csv"
)
