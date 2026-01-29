import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# ---------------- CONFIGURACIÓN ----------------
ZONA_HORARIA = pytz.timezone("America/Santiago")
ARCHIVO_DATOS = "diario_trading.csv"

st.set_page_config(
    page_title="📓 Diario de Trading",
    page_icon="📈",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.caption("Sistema estructurado para medir edge real en W y M.")

ahora = datetime.now(ZONA_HORARIA)

# ---------------- MODELOS NORMALIZADOS ----------------
PATRONES = ["W", "M"]

SETUPS = [
    "Ruptura de base",
    "Segundo impulso",
    "Tercer impulso"
]

EJECUCIONES = ["Agresivo", "Conservador"]

DIRECCIONES = ["Largo", "Corto"]

MERCADOS = ["Futuros", "Forex", "Crypto", "Índices"]

RESULTADOS = ["Win", "Loss", "BE"]

EMOCIONES = [
    "Calma",
    "Confianza",
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

# ---------------- CARGA DE DATOS ----------------
columnas = [
    "fecha",
    "hora",
    "mercado",
    "instrumento",
    "patron",
    "setup",
    "ejecucion",
    "direccion",
    "precio_entrada",
    "precio_salida",
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
st.subheader("📝 Registrar trade")

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
        instrumento = st.text_input("Instrumento (ES, NQ, EURUSD…)")

    col5, col6 = st.columns(2)
    with col5:
        patron = st.selectbox("Patrón", PATRONES)
    with col6:
        setup = st.selectbox("Setup", SETUPS)

    col7, col8 = st.columns(2)
    with col7:
        ejecucion = st.selectbox("Tipo de ejecución", EJECUCIONES)
    with col8:
        direccion = st.selectbox("Dirección", DIRECCIONES)

    col9, col10 = st.columns(2)
    with col9:
        precio_entrada = st.number_input("Precio de entrada", format="%.2f")
    with col10:
        precio_salida = st.number_input("Precio de salida", format="%.2f")

    col11, col12 = st.columns(2)
    with col11:
        resultado = st.selectbox("Resultado", RESULTADOS)
    with col12:
        riesgo_beneficio = st.selectbox(
            "Riesgo / Beneficio",
            ["1:1", "1:1.5", "1:2", "1:3", "1:4+"]
        )

    col13, col14 = st.columns(2)
    with col13:
        emocion_principal = st.selectbox("Emoción dominante", EMOCIONES)
    with col14:
        error_principal = st.selectbox("Error principal", ERRORES)

    comentarios = st.text_area(
        "Comentarios (opcional)",
        placeholder="Contexto rápido del trade"
    )

    guardar = st.form_submit_button("💾 Guardar trade")

# ---------------- GUARDADO ----------------
if guardar:
    nueva_fila = {
        "fecha": fecha.isoformat(),
        "hora": hora.strftime("%H:%M"),
        "mercado": mercado,
        "instrumento": instrumento,
        "patron": patron,
        "setup": setup,
        "ejecucion": ejecucion,
        "direccion": direccion,
        "precio_entrada": precio_entrada,
        "precio_salida": precio_salida,
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
st.subheader("📊 Historial de trades")

if df.empty:
    st.info("Aún no hay trades registrados.")
else:
    st.dataframe(df, use_container_width=True)

# ---------------- EXPORTAR ----------------
st.subheader("⬇️ Exportar datos")

st.download_button(
    "📥 Descargar diario (CSV)",
    df.to_csv(index=False),
    file_name="diario_trading.csv",
    mime="text/csv"
)
st.subheader("🗑️ Eliminar trade (corrección de errores)")

if not df.empty:

    df_reset = df.reset_index(drop=True)

    opciones = [
        f"#{i} | {row.get('fecha','')} | {row.get('instrumento','')}"
        for i, row in df_reset.iterrows()
    ]

    trade_idx = st.selectbox(
        "Selecciona el trade a eliminar",
        options=list(range(len(opciones))),
        format_func=lambda x: opciones[x]
    )

    confirmar = st.checkbox("Confirmar eliminación (acción irreversible)")

    if st.button("❌ Eliminar trade seleccionado") and confirmar:
        df = df.drop(df.index[trade_idx])
        df.to_csv(ARCHIVO_DATOS, index=False)
        st.success("✅ Trade eliminado correctamente")
        st.experimental_rerun()

else:
    st.info("No hay trades para eliminar.")

