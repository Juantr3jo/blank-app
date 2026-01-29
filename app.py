import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# ================== CONFIGURACIÓN ==================
ZONA_HORARIA = pytz.timezone("America/Santiago")
ARCHIVO_DATOS = "diario_trading.csv"

st.set_page_config(
    page_title="📓 Diario de Trading",
    page_icon="📈",
    layout="centered"
)

st.title("📓 Diario de Trading")
st.caption("Sistema estructurado para medir rendimiento real de estrategias W y M.")

ahora = datetime.now(ZONA_HORARIA)

# ================== MODELOS ==================
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

