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

generos_seleccionados = []
for experiencia in experiencias_seleccionadas:
    generos_seleccionados.append(opciones_experiencia[experiencia])

st.code(generos_seleccionados)
st.code(type(generos_seleccionados))


## Aplicado de filtros
df_filtrado = pelis.copy()

if st.button("Filtrar ahora"):
    df_filtrado = filtlar_pelis(df_filtrado, 
                                duracion_min= duracion_min, 
                                duracion_max=duracion_max,
                                rating_min=rating_min,
                                popularidad_max=popularidad_max,
                                mayor_18= excluir_mas_18,
                                #generos=generos_seleccionados
                                )
    st.subheader(f"Total de coincidencias {len(df_filtrado)}")
    st.dataframe(df_filtrado)