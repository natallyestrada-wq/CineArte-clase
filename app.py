import streamlit as st

st.set_page_config(
    page_title="Cine Arte",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.sidebar.image("assets/logo.png")

pag = st.navigation(
    [
        st.Page("pages/inicio.py", title="Inicio", icon="🏠"),
        st.Page("pages/explorar.py", title="Explorar", icon="🔍"),
        st.Page("pages/jugar.py", title="Jugar", icon="🎮"),
        st.Page("pages/mi_cine.py", title="Mi Cine", icon="🎬"),
    ],
    position="top",
)


pag.run()
