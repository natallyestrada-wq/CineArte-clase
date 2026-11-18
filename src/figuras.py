import plotly.express as px
import streamlit as st
from src.traduccion import traducir_generos

def cant_por_genero(df):

    df_conteo = df["genres"].str.split(",").explode().str.strip().value_counts().reset_index().apply(traducir_generos)

    #st.dataframe(df_conteo)

    grafico = px.bar(df_conteo,
                y="genres",
                x= "count",
                title="🎭 Cantidad de películas por género",
                labels={"genres": "", "count": "Cantidad de películas"},
                color="count",
                color_continuous_scale="Jet",
                # color = "count",
                # color_discrete_map=
                )
    grafico.update_layout(coloraxis_showscale = False)
    
    # grafico.update_traces(marker_color="darkorange")

    return grafico

def cant_por_anho(df):
    grafico = px.histogram(df,
                           x = "release_date",
                           title="🗓️ Cantidad de películas por año",
                           labels={"release_date": "Año de lanzamiento"},
                           
                           )
    grafico.update_layout(hovermode = "x unified")
    grafico.update_yaxes(title_text="Cantidad de películas")
    grafico.update_traces(marker_color="thistle")

    return grafico

# ['id', 'title', 'release_date', 'runtime', 'adult', 'original_title', 'overview',
# 'popularity', 'poster_path', 'tagline', 'genres', 'keywords', 'directors', 'writers',
# 'averageRating', 'numVotes', 'cast']

def popularidad_por_calificacion(df):

    df = df[
        df["popularity"] < 512
    ]

    grafico = px.scatter(df,
                         x = 'popularity',
                         y = 'averageRating',
                         hover_name= "title",
                         title="🌟 Popularidad vs. Calificación",
                         labels={'popularity':"Popularidad", 'averageRating': "Calificación"},
                         color="averageRating",
                         color_continuous_scale="Rainbow"
                         )
    grafico.update_layout(coloraxis_showscale = False)

    return grafico