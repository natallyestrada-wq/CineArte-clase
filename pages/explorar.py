## PREPARACIÓN DEL ENTORNO

import streamlit as st
import pandas as pd

from src.datos import cargar_pelis

## CARGA DE DATOS
pelis = cargar_pelis()

## INICIALIZACIÓN DE VARIABLES DE SESIÓN
if "ver_mas_tarde" not in st.session_state:
    st.session_state["ver_mas_tarde"] = [] 
if "ya_vistas" not in st.session_state:
    st.session_state["ya_vistas"] = []

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


filtros = {  # filtros necesarios para aplicar al dataframe
    "title": titulo_buscar,
    "genres": genero_buscar,
    "directors": directores_buscar,
    "cast": reparto_buscar,
}

pelis_filtradas = pelis.copy()

for columna, termino_busqueda in filtros.items():

    if termino_busqueda:
        pelis_filtradas = pelis_filtradas[
            pelis_filtradas[columna].str.contains(
                termino_busqueda.strip(), case=False, regex=False
            )
        ]

## PRESENTACIÓN DE LA TABLA
st.divider()
st.subheader(f"Películas encontradas: {len(pelis_filtradas):,}")

nombres_columnas = {
    "title": "🎬 Película",
    "release_date": "📅 Lanzamiento",
    "averageRating": "⭐ Rating",
    "genres": "🎭 Géneros",
    "directors": "👤 Directores",
    "cast": "👥 Reparto",
}

tabla_mostrar = pelis_filtradas[['id','title', 'release_date', 'averageRating',
   'genres', 'directors', 'cast']].rename(columns=nombres_columnas)

evento = st.dataframe(tabla_mostrar,
                      on_select = "rerun",
                      selection_mode="single-row",
                      column_config={'id': None},
                      hide_index=True
                      )
  

## PRSENTACIÓN DE LOS DETALLES DE LA PELÍCULA SELECCIONADA
if evento["selection"]["rows"]:
    st.divider()
    peli_seleccionada = pelis_filtradas.iloc[evento['selection']['rows'][0]]
    col1, col2 = st.columns([1,2])

    with col1:
        url_poster = f"https://image.tmdb.org/t/p/w500{peli_seleccionada['poster_path']}"
        st.image(url_poster, width="stretch")
    with col2:
        st.subheader(peli_seleccionada["title"])
        st.caption(peli_seleccionada["tagline"])
        st.write(f"📝 Sinopsis: {peli_seleccionada['overview']}")

        st.write(f"📅 Lanzamiento: {peli_seleccionada['release_date']}")
        st.write(f"⭐ Rating: {peli_seleccionada['averageRating']}")
        st.write(f"🎭 Géneros: {peli_seleccionada['genres']}")
        st.write(f"👤 Directores: {peli_seleccionada['directors']}")
        st.write(f"👥 Reparto: {peli_seleccionada['cast']}")

        bot1, bot2 = st.columns(2)
        with bot1:
            if st.button("Guardar para ver"):
                st.session_state['ver_mas_tarde'].append(peli_seleccionada["id"])
                st.success(f"✅ Guardada {peli_seleccionada['title']} para ver más tarde.")
        with bot2:
            if st.button("Ya la vi"):
                st.session_state['ya_vistas'].append(peli_seleccionada["id"])
                st.success(f"✅ Marcada {peli_seleccionada['title']} como ya vista.")
    st.divider()
    st.subheader("Películas guardadas para ver más tarde:")
    st.write(st.session_state['ver_mas_tarde'])
    st.subheader("Películas marcadas como ya vistas:")
    st.write(st.session_state['ya_vistas'])
                

else:
    st.info("👆 Selecciona una película para ver sus detalles.")

# ['id', 'title', 'release_date', 'runtime', 'adult', 'original_title', 'overview',
# 'popularity', 'poster_path', 'tagline', 'genres', 'keywords', 'directors', 'writers',
# 'averageRating', 'numVotes', 'cast']


## DETALLES DE UNA PELI SELECCIONADA


## GRÁFICOS
