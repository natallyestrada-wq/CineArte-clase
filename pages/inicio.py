import streamlit as st

## INICIALIZACIÓN DE VARIABLES DE SESIÓN
if "ver_mas_tarde" not in st.session_state:
    st.session_state["ver_mas_tarde"] = [] 
if "ya_vistas" not in st.session_state:
    st.session_state["ya_vistas"] = []
if "partidas_jugadas" not in st.session_state:
    st.session_state["partidas_jugadas"] = 0

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


st.divider()
st.subheader("Estadísticas")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Películas guardadas para ver más tarde",
        len(st.session_state["ver_mas_tarde"]),
    )

with col2:
    st.metric("Películas ya vistas", len(st.session_state["ya_vistas"]))

with col3:
    st.metric("Partidas jugadas", st.session_state["partidas_jugadas"])

st.divider()
st.subheader("Sobre mí")

col_foto, col_biografia = st.columns([1, 2])

with col_foto:
    st.image("assets/cindy_estrada.jpeg", width=250)

with col_biografia:
    st.markdown("**Docente · Universidad de Antioquia**")
    st.write("Soy una profesional apasionada por la tecnología, la educación y la ciencia.")
    st.write(
        "Me gusta transformar ideas complejas en experiencias de aprendizaje claras y "
        "significativas. Disfruto aprender constantemente y combinar ciencia, tecnología "
        "y creatividad para resolver problemas."
    )
