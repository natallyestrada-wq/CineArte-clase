import streamlit as st

## INICIALIZACIÓN DE VARIABLES DE SESIÓN
if "ver_mas_tarde" not in st.session_state:
    st.session_state["ver_mas_tarde"] = [] 
if "ya_vistas" not in st.session_state:
    st.session_state["ya_vistas"] = []

st.title("Página de Inicio")

st.write(
    "Este es un espacio para explorar películas y descubrir tus nuevas historias favoritas "
    "a través del cine."
)

st.caption("Creado con Python, Streamlit e información de Kaggle por Cindy Estrada")


# if st.button("Este es un botón de ejemplo"):
#     st.write("¡Has hecho clic en el botón!")


st.divider()

# 3 Secciones: Explorar, Jugar y Mi Cine
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Explorar")
    st.write(
        "Descubre nuevas películas y series para disfrutar. "
        "Explora diferentes géneros, directores y actores."
    )

    if st.button("Ir a Explorar"):
        st.switch_page("pages/explorar.py")

with col2:
    st.subheader("Jugar")
    st.write(
        "Participa en juegos y trivias relacionadas con el cine. "
        "Pon a prueba tus conocimientos y gana premios."
    )

    if st.button("Ir a Jugar"):
        st.switch_page("pages/jugar.py")

with col3:
    st.subheader("Mi Cine")
    st.write(
        "Guarda tus películas favoritas y crea listas personalizadas. "
        "Sigue tus preferencias y descubre nuevas recomendaciones."
    )

    if st.button("Ir a Mi Cine"):
        st.switch_page("pages/mi_cine.py")


st.subheader("Películas guardadas para ver más tarde:")
st.write(st.session_state['ver_mas_tarde'])
st.subheader("Películas marcadas como ya vistas:")
st.write(st.session_state['ya_vistas'])
