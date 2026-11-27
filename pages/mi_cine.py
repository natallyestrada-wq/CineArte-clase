from collections import Counter

import pandas as pd
import streamlit as st

from src.datos import cargar_pelis
from src.estado_cine import (
    guardar_para_ver_mas_tarde,
    inicializar_estado_cine,
    marcar_como_vista,
    quitar_de_ver_mas_tarde,
    quitar_de_vistas,
)
from src.traduccion import traducir_generos


inicializar_estado_cine()
pelis = (
    cargar_pelis()
    .drop_duplicates(subset="id", keep="first")
    .set_index("id", drop=False)
)


def peliculas_por_ids(ids):
    ids_validos = list(
        dict.fromkeys(movie_id for movie_id in ids if movie_id in pelis.index)
    )
    return pelis.loc[ids_validos] if ids_validos else pelis.iloc[0:0]


def contar_generos(ids):
    peliculas = peliculas_por_ids(ids)
    if peliculas.empty:
        return pd.Series(dtype="int64")

    generos = (
        peliculas["genres"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )
    generos = generos[generos.ne("")]
    return generos.value_counts().head(10)


def mostrar_coleccion(ids, lista):
    ids_validos = peliculas_por_ids(ids).index.tolist()
    if not ids_validos:
        st.info("Esta lista todavía está vacía.")
        return

    for inicio in range(0, len(ids_validos), 2):
        columnas = st.columns(2)
        for columna, movie_id in zip(columnas, ids_validos[inicio : inicio + 2]):
            pelicula = pelis.loc[movie_id]
            with columna:
                with st.container(border=True):
                    poster_path = pelicula["poster_path"]
                    if isinstance(poster_path, str) and poster_path.strip():
                        st.image(
                            f"https://image.tmdb.org/t/p/w500{poster_path}",
                            width="stretch",
                        )

                    st.subheader(pelicula["title"])
                    if isinstance(pelicula["genres"], str):
                        generos = [
                            genero.strip()
                            for genero in pelicula["genres"].split(",")
                            if genero.strip()
                        ]
                        st.caption("🎭 " + ", ".join(traducir_generos(generos)))
                    if pd.notna(pelicula["averageRating"]):
                        st.caption(f"⭐ {pelicula['averageRating']}")

                    with st.expander("Ver sinopsis"):
                        if isinstance(pelicula["overview"], str):
                            st.write(pelicula["overview"])
                        else:
                            st.write("Sin sinopsis disponible.")

                    col_accion, col_quitar = st.columns(2)
                    if lista == "ver_mas_tarde":
                        with col_accion:
                            if st.button(
                                "Marcar como vista",
                                key=f"marcar_vista_{movie_id}",
                            ):
                                marcar_como_vista(movie_id)
                                st.rerun()
                        with col_quitar:
                            if st.button(
                                "Quitar",
                                key=f"quitar_pendiente_{movie_id}",
                            ):
                                quitar_de_ver_mas_tarde(movie_id)
                                st.rerun()
                    else:
                        with col_accion:
                            if st.button(
                                "Mover a pendientes",
                                key=f"mover_pendiente_{movie_id}",
                            ):
                                guardar_para_ver_mas_tarde(movie_id)
                                st.rerun()
                        with col_quitar:
                            if st.button(
                                "Quitar",
                                key=f"quitar_vista_{movie_id}",
                            ):
                                quitar_de_vistas(movie_id)
                                st.rerun()


st.title("Mi Cine")
st.write("Tu colección personal, tus preferencias y el historial de tus duelos.")
st.caption("Estas estadísticas se conservan solo durante la sesión actual.")

vistas_ids = list(
    dict.fromkeys(
        movie_id
        for movie_id in st.session_state["ya_vistas"]
        if movie_id in pelis.index
    )
)
vistas_set = set(vistas_ids)
pendientes_ids = list(
    dict.fromkeys(
        movie_id
        for movie_id in st.session_state["ver_mas_tarde"]
        if movie_id in pelis.index and movie_id not in vistas_set
    )
)
coleccion_total = len(vistas_set | set(pendientes_ids))
porcentaje_visto = (
    len(vistas_ids) / coleccion_total * 100 if coleccion_total else 0
)

peliculas_vistas = peliculas_por_ids(vistas_ids)
calificaciones = pd.to_numeric(
    peliculas_vistas["averageRating"], errors="coerce"
).dropna()
promedio_calificacion = calificaciones.mean() if not calificaciones.empty else None

col_vistas, col_pendientes, col_progreso, col_partidas = st.columns(4)
col_vistas.metric("Películas vistas", len(vistas_ids))
col_pendientes.metric("Por ver", len(pendientes_ids))
col_progreso.metric("Colección vista", f"{porcentaje_visto:.0f}%")
col_partidas.metric("Partidas jugadas", st.session_state["partidas_jugadas"])

if promedio_calificacion is not None:
    st.caption(f"Calificación media de tus películas vistas: {promedio_calificacion:.1f} ⭐")

st.divider()
st.subheader("Tu colección")
tab_pendientes, tab_vistas = st.tabs(["Por ver", "Vistas"])

with tab_pendientes:
    mostrar_coleccion(pendientes_ids, "ver_mas_tarde")

with tab_vistas:
    mostrar_coleccion(vistas_ids, "ya_vistas")

st.divider()
st.subheader("Tus preferencias")
col_generos_vistos, col_generos_pendientes = st.columns(2)

with col_generos_vistos:
    st.markdown("**Géneros de tus películas vistas**")
    generos_vistos = contar_generos(vistas_ids)
    if generos_vistos.empty:
        st.info("Marca películas como vistas para descubrir tus géneros favoritos.")
    else:
        generos_vistos.index = traducir_generos(generos_vistos.index.tolist())
        st.bar_chart(generos_vistos)

with col_generos_pendientes:
    st.markdown("**Géneros de tus películas pendientes**")
    generos_pendientes = contar_generos(pendientes_ids)
    if generos_pendientes.empty:
        st.info("Guarda películas para ver más tarde y aquí verás sus géneros.")
    else:
        generos_pendientes.index = traducir_generos(
            generos_pendientes.index.tolist()
        )
        st.bar_chart(generos_pendientes)

st.divider()
st.subheader("Actividad de visionado")
fechas_vistas = st.session_state["fechas_vistas"]
fechas_registradas = [
    fechas_vistas[movie_id]
    for movie_id in vistas_ids
    if movie_id in fechas_vistas
]
anios_vistos = pd.to_datetime(
    pd.Series(fechas_registradas), errors="coerce"
).dropna().dt.year.value_counts().sort_index()

if anios_vistos.empty:
    st.info("Las películas marcadas como vistas aparecerán aquí por año.")
else:
    st.bar_chart(anios_vistos)

st.divider()
st.subheader("Estadísticas de duelos")
historial = st.session_state["historial_partidas"]
peliculas_jugadas = st.session_state["peliculas_jugadas"]
conteo_ganadoras = Counter(
    partida["ganadora_id"] for partida in historial
)

col_total_duelos, col_peliculas_duelos, col_ganadora_frecuente = st.columns(3)
col_total_duelos.metric("Partidas completadas", st.session_state["partidas_jugadas"])
col_peliculas_duelos.metric(
    "Películas únicas en duelos",
    len(set(peliculas_jugadas)),
)

if conteo_ganadoras:
    id_mas_ganadora, numero_victorias = conteo_ganadoras.most_common(1)[0]
    nombre_mas_ganadora = (
        pelis.loc[id_mas_ganadora, "title"]
        if id_mas_ganadora in pelis.index
        else "Película sin datos"
    )
    col_ganadora_frecuente.metric(
        "Más veces ganadora",
        nombre_mas_ganadora,
        f"{numero_victorias} victorias",
    )
else:
    col_ganadora_frecuente.metric("Más veces ganadora", "—")

generos_ganadores = Counter()
for partida in historial:
    id_ganadora = partida["ganadora_id"]
    if id_ganadora in pelis.index:
        generos = pelis.loc[id_ganadora, "genres"]
        if isinstance(generos, str):
            generos_ganadores.update(
                set(genero.strip() for genero in generos.split(",") if genero.strip())
            )

if generos_ganadores:
    conteo_generos_ganadores = pd.Series(generos_ganadores).sort_values(
        ascending=False
    )
    conteo_generos_ganadores.index = traducir_generos(
        conteo_generos_ganadores.index.tolist()
    )
    st.markdown("**Géneros de tus películas ganadoras**")
    st.bar_chart(conteo_generos_ganadores.head(10))

st.markdown("**Historial de partidas**")
if not historial:
    st.info("Completa un duelo para empezar a crear tu historial.")
else:
    for numero, partida in reversed(list(enumerate(historial, start=1))):
        id_ganadora = partida["ganadora_id"]
        nombre_ganadora = (
            pelis.loc[id_ganadora, "title"]
            if id_ganadora in pelis.index
            else "Película sin datos"
        )
        fecha = pd.to_datetime(partida["fecha"], errors="coerce")
        fecha_texto = fecha.strftime("%d/%m/%Y %H:%M") if pd.notna(fecha) else ""

        with st.expander(f"Partida {numero} · {fecha_texto} · 🏆 {nombre_ganadora}"):
            titulos_jugados = peliculas_por_ids(partida["peliculas_ids"])["title"]
            st.write("Películas enfrentadas: " + ", ".join(titulos_jugados.tolist()))
