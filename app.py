import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Diario de Trading", layout="centered")

CSV_FILE = "diario_trading.csv"

# -------------------------------
# CREAR CSV SI NO EXISTE
# -------------------------------
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=[
        "fecha",
        "mercado",
        "sesion",
        "tipo_dia",
        "dia_operable",
        "noticias",
        "ubicacion_precio",
        "temporalidad_extremo",
        "estructura",
        "variante",
        "estructura_completa",
        "impulsos",
        "tipo_entrada",
        "momento_entrada",
        "ema_estado",
        "stop_ubicacion",
        "rr",
        "stop_respetado",
        "resultado",
        "rango_pips",
        "disciplina_ok",
        "error_tipo",
        "emocion_antes",
        "emocion_despues",
        "repetir_trade",
        "evaluacion_trade",
        "evaluacion_dia"
    ])
    df_init.to_csv(CSV_FILE, index=False)

# -------------------------------
# APP
# -------------------------------
st.title("📒 Diario de Trading – Sistema M / W")

st.markdown("### 🧠 Contexto del día")

fecha = datetime.now().strftime("%Y-%m-%d")

mercado = st.selectbox("Mercado", ["SP500", "Oro", "Nasdaq"])
sesion = st.selectbox("Sesión", ["Asia", "Londres", "Nueva York"])
tipo_dia = st.selectbox("Tipo de día", [
    "Tendencia fuerte",
    "Tendencia débil",
    "Rango",
    "Distribución / acumulación"
])
dia_operable = st.radio("¿El día era operable según tu plan?", ["Sí", "No"])
noticias = st.radio("¿Había noticias de alto impacto?", ["Sí", "No"])

st.markdown("### 📍 Ubicación del precio")

ubicacion_precio = st.radio(
    "Ubicación del precio",
    ["Precio caro (zona alta)", "Precio barato (zona baja)", "Zona media"]
)

temporalidad_extremo = st.selectbox(
    "Temporalidad del extremo",
    ["Extremo del día", "Extremo de la semana", "Extremo intradía"]
)

st.markdown("### 🔺 Estructura")

estructura = st.radio("Tipo de estructura", ["M", "W"])
variante = st.selectbox("Variante", ["1", "2", "3"])
estructura_completa = st.radio("¿Estructura completa?", ["Sí", "No"])
impulsos = st.selectbox("Número de impulsos previos", ["1", "2", "3", "Más de 3"])

st.markdown("### 🎯 Entrada")

tipo_entrada = st.radio(
    "Tipo de entrada",
    ["Agresiva (ruptura)", "Conservadora (2º impulso)"]
)

momento_entrada = st.selectbox(
    "Momento de entrada",
    ["Ruptura", "Pullback", "Segundo impulso"]
)

st.markdown("### 📉 EMA")

ema_estado = st.radio(
    "Estado de la EMA",
    ["EMA a favor", "EMA neutra", "EMA en contra"]
)

st.markdown("### ⚙️ Gestión del riesgo")

stop_ubicacion = st.selectbox(
    "Ubicación del Stop",
    [
        "Sobre máximo/mínimo de la M/W",
        "Sobre el pullback",
        "Stop estructural amplio"
    ]
)

rr = st.selectbox("Relación Riesgo/Beneficio", ["1:1", "1:2", "1:3", "Mayor a 1:3"])
stop_respetado = st.radio("¿Stop respetado?", ["Sí", "No"])

st.markdown("### 📊 Resultado")

resultado = st.radio("Resultado del trade", ["Ganador", "Perdedor", "Break-even"])
rango_pips = st.selectbox(
    "Rango de pips",
    ["+0 a +5", "+5 a +10", "+10 a +20", "-0 a -5", "-5 a -10", "-10 o más"]
)

st.markdown("### 🧠 Disciplina")

disciplina_ok = st.radio("¿Seguiste la estrategia exactamente?", ["Sí", "No"])

error_tipo = ""
if disciplina_ok == "No":
    error_tipo = st.selectbox(
        "¿Qué falló?",
        [
            "Entré antes de tiempo",
            "No esperé estructura completa",
            "No estaba en extremo",
            "Operé en tendencia fuerte",
            "Operé por ansiedad",
            "Forcé la entrada"
        ]
    )

st.markdown("### 😐 Emoción")

emocion_antes = st.selectbox(
    "Emoción antes del trade",
    ["Tranquilo", "Ansioso", "Acelerado", "Con miedo"]
)

emocion_despues = st.selectbox(
    "Emoción después del trade",
    ["Tranquilo", "Frustrado", "Molesto", "Indiferente"]
)

st.markdown("### 🧾 Evaluación final")

repetir_trade = st.radio("¿Repetirías este trade?", ["Sí", "No"])
evaluacion_trade = st.selectbox(
    "Evaluación del trade",
    ["Trade correcto", "Trade incorrecto", "Trade innecesario"]
)

evaluacion_dia = st.selectbox(
    "Evaluación del día",
    ["Buen día", "Día neutro", "Día NO operable"]
)

# -------------------------------
# GUARDAR
# -------------------------------
if st.button("💾 Guardar trade"):
    nuevo_trade = {
        "fecha": fecha,
        "mercado": mercado,
        "sesion": sesion,
        "tipo_dia": tipo_dia,
        "dia_operable": dia_operable,
        "noticias": noticias,
        "ubicacion_precio": ubicacion_precio,
        "temporalidad_extremo": temporalidad_extremo,
        "estructura": estructura,
        "variante": variante,
        "estructura_completa": estructura_completa,
        "impulsos": impulsos,
        "tipo_entrada": tipo_entrada,
        "momento_entrada": momento_entrada,
        "ema_estado": ema_estado,
        "stop_ubicacion": stop_ubicacion,
        "rr": rr,
        "stop_respetado": stop_respetado,
        "resultado": resultado,
        "rango_pips": rango_pips,
        "disciplina_ok": disciplina_ok,
        "error_tipo": error_tipo,
        "emocion_antes": emocion_antes,
        "emocion_despues": emocion_despues,
        "repetir_trade": repetir_trade,
        "evaluacion_trade": evaluacion_trade,
        "evaluacion_dia": evaluacion_dia
    }

    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([nuevo_trade])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    st.success("✅ Trade guardado correctamente")

# -------------------------------
# VER HISTORIAL
# -------------------------------
st.markdown("---")
st.markdown("### 📊 Historial de trades")

df_hist = pd.read_csv(CSV_FILE)
st.dataframe(df_hist)
