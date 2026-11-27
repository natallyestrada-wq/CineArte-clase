from datetime import datetime

import streamlit as st


def inicializar_estado_cine():
    valores_iniciales = {
        "ver_mas_tarde": [],
        "ya_vistas": [],
        "fechas_vistas": {},
        "partidas_jugadas": 0,
        "peliculas_jugadas": [],
        "historial_partidas": [],
    }

    for clave, valor in valores_iniciales.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def marcar_como_vista(id_pelicula):
    inicializar_estado_cine()
    if id_pelicula not in st.session_state["ya_vistas"]:
        st.session_state["ya_vistas"].append(id_pelicula)

    st.session_state["fechas_vistas"].setdefault(
        id_pelicula,
        datetime.now().isoformat(timespec="seconds"),
    )
    st.session_state["ver_mas_tarde"] = [
        pelicula_id
        for pelicula_id in st.session_state["ver_mas_tarde"]
        if pelicula_id != id_pelicula
    ]


def guardar_para_ver_mas_tarde(id_pelicula):
    inicializar_estado_cine()
    if id_pelicula not in st.session_state["ver_mas_tarde"]:
        st.session_state["ver_mas_tarde"].append(id_pelicula)

    st.session_state["ya_vistas"] = [
        pelicula_id
        for pelicula_id in st.session_state["ya_vistas"]
        if pelicula_id != id_pelicula
    ]
    st.session_state["fechas_vistas"].pop(id_pelicula, None)


def quitar_de_vistas(id_pelicula):
    inicializar_estado_cine()
    st.session_state["ya_vistas"] = [
        pelicula_id
        for pelicula_id in st.session_state["ya_vistas"]
        if pelicula_id != id_pelicula
    ]
    st.session_state["fechas_vistas"].pop(id_pelicula, None)


def quitar_de_ver_mas_tarde(id_pelicula):
    inicializar_estado_cine()
    st.session_state["ver_mas_tarde"] = [
        pelicula_id
        for pelicula_id in st.session_state["ver_mas_tarde"]
        if pelicula_id != id_pelicula
    ]


def registrar_partida(peliculas_ids, ganadora_id):
    inicializar_estado_cine()
    ids_unicos = list(dict.fromkeys(int(pelicula_id) for pelicula_id in peliculas_ids))
    ganadora_id = int(ganadora_id)

    st.session_state["historial_partidas"].append(
        {
            "fecha": datetime.now().isoformat(timespec="seconds"),
            "peliculas_ids": ids_unicos,
            "ganadora_id": ganadora_id,
        }
    )

    for pelicula_id in ids_unicos:
        if pelicula_id not in st.session_state["peliculas_jugadas"]:
            st.session_state["peliculas_jugadas"].append(pelicula_id)

    st.session_state["partidas_jugadas"] += 1
