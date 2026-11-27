import random

import streamlit as st
from src.datos import cargar_pelis, filtlar_pelis
from src.estado_cine import (
    guardar_para_ver_mas_tarde,
    inicializar_estado_cine,
    marcar_como_vista,
    registrar_partida,
)


## CARGA DE DATOS
pelis = (
    cargar_pelis()
    .drop_duplicates(subset="id", keep="first")
    .set_index("id", drop=False)
)

inicializar_estado_cine()
st.session_state.pop("peliculas_filtradas_juego", None)
st.session_state.pop("duelo_peliculas", None)
if "peliculas_filtradas_juego_ids" not in st.session_state:
    st.session_state["peliculas_filtradas_juego_ids"] = None
if "duelo_peliculas_ids" not in st.session_state:
    st.session_state["duelo_peliculas_ids"] = None


## PARTE VISUAL
st.title("Página de jugar")

st.write("Bienvenido a la página de juegos")


## FILTROS
opciones_duracion = {   # Opciones de duración
    "🏃 Menos de 30 minutos":[0,30],
    "⏳ Hasta hora y media":[31,90],
    "⏰ Más de hora y media":[91,600],
    "🦦 Sin preferencia":[None, None]
}

duracion_buscar = st.radio("Escoge la duración de tu película",
                           opciones_duracion.keys(),
                           index= 3
                           )

duracion_min = opciones_duracion[duracion_buscar][0]
duracion_max = opciones_duracion[duracion_buscar][1]

#----------------------------
opciones_valoracion = [  # Opciones de valoración
    "⭐ Películas muy bien valoradas",
    "🧐 Películas poco populares",
    "🤯 Poco populares y bien valoradas",
    "🤷 Sin preferencia"
]

valoracion_buscar = st.radio("¿Qué tipo de valoración prefieres?",
                             opciones_valoracion)
if valoracion_buscar == "⭐ Películas muy bien valoradas":
    rating_min = 8
    popularidad_max = None
elif valoracion_buscar == "🧐 Películas poco populares":
    popularidad_max = 40
    rating_min = None
elif valoracion_buscar == "🤯 Poco populares y bien valoradas":
    popularidad_max = 40
    rating_min = 8
elif valoracion_buscar == "🤷 Sin preferencia":
    rating_min = None
    popularidad_max = None

#----------------
excluir_mas_18 = st.checkbox("Quiero excluir películas para adultos")

# ---------------
opciones_experiencia = {         # Opciones de experiencia cinematográfica
    "💥 Acción y adrenalina": [
        "Action", "Adventure", "War", "Thriller"
    ],
    "🔍 Misterio y secretos": [
        "Mystery", "Crime", "Thriller"
    ],
    "👽 Mundos extraordinarios": [
        "Science Fiction", "Fantasy", "Adventure", "Animation"
    ],
    "😭 Emociones a flor de piel": [
        "Drama", "Romance", "History", "Music"
    ],
    "🗺️ Aventura y exploración": [
        "Adventure", "Western", "History", "War"
    ],
    "😂 Risas y diversión": [
        "Comedy", "Family", "Animation"
    ],
    "👻 Miedo y oscuridad": [
        "Horror", "Mystery", "Thriller"
    ],
    "🤯 Mentes sorprendidas": [
        "Science Fiction", "Mystery", "Thriller", "Drama"
    ],
    "🎬 Historias reales y del mundo": [
        "Documentary", "History", "War", "Music"
    ]
}


experiencias_seleccionadas = st.pills(
    "¿Qué tipo de experiencia buscas?",
    opciones_experiencia.keys(),
    selection_mode= "multi",
    width="stretch"
)

generos_seleccionados = [
    genero
    for experiencia in experiencias_seleccionadas
    for genero in opciones_experiencia[experiencia]
]


## Aplicado de filtros
duelo_actual = st.session_state["duelo_peliculas_ids"]
if duelo_actual is None or duelo_actual["ganadora"] is not None:
    texto_boton = "Iniciar duelos" if duelo_actual is None else "Jugar otra partida"
    if st.button(texto_boton):
        df_filtrado = filtlar_pelis(
            pelis.copy(),
            duracion_min=duracion_min,
            duracion_max=duracion_max,
            rating_min=rating_min,
            popularidad_max=popularidad_max,
            mayor_18=excluir_mas_18,
            generos=generos_seleccionados,
        )
        ids_filtrados = [int(movie_id) for movie_id in df_filtrado["id"].tolist()]
        st.session_state["peliculas_filtradas_juego_ids"] = ids_filtrados

        if len(ids_filtrados) < 4:
            st.session_state["duelo_peliculas_ids"] = None
            st.warning("Se necesitan al menos 4 películas para completar las 3 rondas.")
        else:
            pareja_inicial = random.sample(ids_filtrados, 2)
            st.session_state["duelo_peliculas_ids"] = {
                "ronda": 1,
                "pareja": pareja_inicial,
                "usadas": pareja_inicial.copy(),
                "peliculas_ids": pareja_inicial.copy(),
                "ganadora": None,
            }
            st.rerun()

ids_filtrados = st.session_state["peliculas_filtradas_juego_ids"]
df_filtrado = (
    pelis.loc[ids_filtrados].copy()
    if ids_filtrados is not None
    else pelis.iloc[0:0].copy()
)

st.divider()
st.subheader("Duelo de películas")

if st.session_state["duelo_peliculas_ids"] is not None:
    duelo = st.session_state["duelo_peliculas_ids"]

    if duelo["ganadora"] is None:
        st.write(f"Ronda {duelo['ronda']} de 3: elige tu película favorita")
        columnas_duelo = st.columns(2)

        for posicion, (columna, id_pelicula) in enumerate(
            zip(columnas_duelo, duelo["pareja"])
        ):
            pelicula = pelis.loc[id_pelicula]
            with columna:
                poster_path = pelicula["poster_path"]
                if isinstance(poster_path, str) and poster_path.strip():
                    st.image(
                        f"https://image.tmdb.org/t/p/w500{poster_path}",
                        width="stretch",
                    )

                st.subheader(pelicula["title"])
                st.caption(f"⭐ {pelicula['averageRating']}")
                if isinstance(pelicula["genres"], str):
                    st.write(f"🎭 {pelicula['genres']}")
                if isinstance(pelicula["overview"], str):
                    st.write(pelicula["overview"])

                if st.button(
                    "Elegir esta película",
                    key=f"duelo_ronda_{duelo['ronda']}_opcion_{posicion}",
                ):
                    if duelo["ronda"] == 3:
                        duelo["ganadora"] = id_pelicula
                        registrar_partida(
                            duelo["peliculas_ids"],
                            id_pelicula,
                        )
                    else:
                        candidatos = [
                            movie_id
                            for movie_id in df_filtrado.index
                            if movie_id not in duelo["usadas"]
                        ]
                        nueva_pelicula = random.choice(candidatos)
                        duelo["pareja"] = [id_pelicula, nueva_pelicula]
                        duelo["usadas"].append(nueva_pelicula)
                        duelo["peliculas_ids"].append(nueva_pelicula)
                        duelo["ronda"] += 1

                    st.session_state["duelo_peliculas_ids"] = duelo
                    st.rerun()
    else:
        ganadora = pelis.loc[duelo["ganadora"]]
        st.success("¡Tenemos una ganadora!")

        col_foto, col_detalles = st.columns([1, 2])
        with col_foto:
            poster_path = ganadora["poster_path"]
            if isinstance(poster_path, str) and poster_path.strip():
                st.image(
                    f"https://image.tmdb.org/t/p/w500{poster_path}",
                    width="stretch",
                )

        with col_detalles:
            st.subheader(ganadora["title"])
            if isinstance(ganadora["overview"], str):
                st.write(ganadora["overview"])
            st.write(f"📅 Estreno: {ganadora['release_date']}")
            st.write(f"⭐ Calificación: {ganadora['averageRating']}")
            st.write(f"🎭 Géneros: {ganadora['genres']}")
            st.write(f"👤 Dirección: {ganadora['directors']}")
            st.write(f"👥 Reparto: {ganadora['cast']}")

        id_ganadora = ganadora["id"]
        col_vistas, col_pendientes = st.columns(2)

        with col_vistas:
            if st.button("Guardar como vista"):
                marcar_como_vista(id_ganadora)
                st.success("Película guardada en la lista de vistas.")

        with col_pendientes:
            if st.button("Guardar para ver más tarde"):
                guardar_para_ver_mas_tarde(id_ganadora)
                st.success("Película guardada para ver más tarde.")
