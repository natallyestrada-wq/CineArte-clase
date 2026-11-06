## PREPARACIÓN DEL ENTORNO

import streamlit as st
import pandas as pd

from src.datos import cargar_pelis

pelis = cargar_pelis()


# INTRODUCCIÓN A LA PÁGINA
st.title("Página de Explorar")
st.write(
    "Bienvenido a la página de explorar. "
    "Aquí puedes descubrir nuevas películas y series para disfrutar."
)

# FILTROS
titulo_buscar = st.text_input(
    "Buscar por título", placeholder="Escribe el título de la película..."
)

col1, col2, col3 = st.columns(3)

with col1:
    genero_buscar = st.text_input("🎭 Género", placeholder="Ej. Drama")
with col2:
    directores_buscar = st.text_input("🎬 Directores", placeholder="Ej. Christian Bale")
with col3:
    reparto_buscar = st.text_input("👥 Reparto", placeholder="Ej. Leonardo")


# ['id', 'title', 'release_date', 'runtime', 'adult', 'original_title', 'overview',
# 'popularity', 'poster_path', 'tagline', 'genres', 'keywords', 'directors', 'writers',
# 'averageRating', 'numVotes', 'cast']

filtros = {  # filtros necesarios para aplicar al dataframe
    "title": titulo_buscar,
    "genres": genero_buscar,
    "directors": directores_buscar,
    "cast": reparto_buscar,
}

for columna, termino_busqueda in filtros.items():

    if termino_busqueda:
        pelis_filtradas = pelis[
            pelis[columna].str.contains(
                termino_busqueda.strip(), case=False, regex=False
            )
        ]

## PRESENTACIÓN DE LA TABLA

st.dataframe(pelis_filtradas)


## DETALLES DE UNA PELI SELECCIONADA


## GRÁFICOS
