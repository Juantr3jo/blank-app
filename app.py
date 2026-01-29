import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# ================= CONFIGURACIÓN =================
ZONA_HORARIA = pytz.timezone("America/Santiago")
ARCHIVO = "diario_trading.csv"

st.set_page_config(
    page_title="Diario de Trading",
    page_icon="📓",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.caption("Registro simple y automático basado en diferencia de precio.")

ahora = datetime.now(ZONA_HORARIA)

# ================= OPCIONES =================
PATRONES = ["W", "M"]
SETUPS = ["Ruptura de base", "Segundo impulso", "Tercer impulso"]
EJECUCIONES = ["Agresivo", "Conservador"]
DIRECCIONES = ["Largo", "Corto"]

# ================= COLUMNAS =================
COLUMNAS = [
    "fecha",
    "hora",
    "patron",
    "setup",
    "ejecucion",
    "direccion",
    "precio_entrada",
    "precio_salida",
    "resultado_trade",
    "cantidad_resultado",
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

    precio_entrada = st.number_input("Precio de entrada", format="%.2f")
    precio_salida = st.number_input("Precio de salida", format="%.2f")

    comentario = st.text_area("Comentario (opcional)")

    guardar = st.form_submit_button("💾 Guardar trade")

# ================= LÓGICA DE CÁLCULO =================
def calcular_resultado(entrada, salida, direccion):
    if direccion == "Largo":
        diferencia = salida - entrada
    else:
        diferencia = entrada - salida

    if diferencia > 0:
        return "Ganador", round(diferencia, 2)
    elif diferencia < 0:
        return "Perdedor", round(diferencia, 2)
    else:
        return "BE", 0.0

# ================= GUARDADO =================
if guardar:
    resultado_trade, cantidad_resultado = calcular_resultado(
        precio_entrada,
        precio_salida,
        direccion
    )

    nueva_fila = {
        "fecha": fecha.isoformat(),
        "hora": hora.strftime("%H:%M"),
        "patron": patron,
        "setup": setup,
        "ejecucion": ejecucion,
        "direccion": direccion,
        "precio_entrada": precio_entrada,
        "precio_salida": precio_salida,
        "resultado_trade": resultado_trade,
        "cantidad_resultado": cantidad_resultado,
        "comentario": comentario
    }

    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(ARCHIVO, index=False)

    st.success(
        f"✅ Trade {resultado_trade} | Resultado: {cantidad_resultado}"
    )

# ================= HISTORIAL =================
st.subheader("📊 Historial")

if df.empty:
    st.info("No hay trades registrados.")
else:
    st.dataframe(df, use_container_width=True)

# ================= ELIMINAR TRADE =================
st.subheader("🗑️ Eliminar trade (corrección de errores)")

if not df.empty:
    df_reset = df.reset_index(drop=True)

    opciones = [
        f"{i} | {row['fecha']} | {row['patron']} | {row['setup']} | {row['resultado_trade']} ({row['cantidad_resultado']})"
        for i, row in df_reset.iterrows()
    ]

    idx = st.selectbox(
        "Selecciona un trade",
        range(len(opciones)),
        format_func=lambda x: opciones[x]
    )

    confirmar = st.checkbox("Confirmo que deseo eliminar este trade")

    if st.button("❌ Eliminar trade") and confirmar:
        df = df.drop(df.index[idx])
        df.to_csv(ARCHIVO, index=False)
        st.success("🗑️ Trade eliminado correctamente")
        st.experimental_rerun()

# ================= EXPORTAR =================
st.subheader("⬇️ Exportar datos")

st.download_button(
    "Descargar CSV",
    df.to_csv(index=False),
    file_name="diario_trading.csv",
    mime="text/csv"
)
