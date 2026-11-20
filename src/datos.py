import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).parent.parent
RUTA_MOVIES = RAIZ / "data" / "movies.csv"


def cargar_pelis():
    df = pd.read_csv(RUTA_MOVIES)
    return df

def filtlar_pelis(df, 
                  titulo = None, 
                  generos = None, 
                  directores = None, 
                  reparto = None,
                  duracion_min = None,
                  duracion_max = None,
                  rating_min = None,
                  popularidad_max = None
                  ):

    # Filtros por texto
    filtros = {  # filtros necesarios para aplicar al dataframe
        "title": titulo,
        "genres": generos,
        "directors": directores,
        "cast": reparto,
    }

    for columna, termino_busqueda in filtros.items():

        if termino_busqueda:
            df = df[
                df[columna].str.contains(
                    termino_busqueda.strip(), case=False, regex=False
                )
            ]

    # Filtros por tiempo
    if duracion_min is not None:
        df = df[
            df["runtime"] >= duracion_min
        ]

    if duracion_max is not None:
        df = df[
            df["runtime"] <= duracion_max
        ]

    if rating_min is not None:
        df = df[
            df["averageRating"] >= rating_min
        ]
    if popularidad_max is not None:
        df = df[
            df["popularity"] <= popularidad_max
        ]


    return df