import streamlit as st
from src.datos import cargar_pelis, filtlar_pelis


## CARGA DE DATOS
pelis = cargar_pelis()


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




st.write(duracion_max)
  
df_filtrado = pelis.copy()

if st.button("Filtrar ahora"):
    df_filtrado = filtlar_pelis(df_filtrado, 
                                duracion_min= duracion_min, 
                                duracion_max=duracion_max,
                                rating_min=rating_min,
                                popularidad_max=popularidad_max)
    st.dataframe(df_filtrado)