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