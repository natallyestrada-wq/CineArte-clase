import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).parent.parent
RUTA_MOVIES = RAIZ / "data" / "movies.csv"


def cargar_pelis():
    df = pd.read_csv(RUTA_MOVIES)
    return df
