
def traducir_generos(generos_en):

    traducciones_generos = {
        "Action": "Acción",
        "Adventure": "Aventura",
        "Animation": "Animación",
        "Comedy": "Comedia",
        "Crime": "Crimen",
        "Documentary": "Documental",
        "Drama": "Drama",
        "Family": "Familiar",
        "Fantasy": "Fantasía",
        "History": "Historia",
        "Horror": "Terror",
        "Music": "Música",
        "Mystery": "Misterio",
        "Romance": "Romance",
        "Science Fiction": "Ciencia Ficción",
        "TV Movie": "Película de TV",
        "Thriller": "Suspenso",
        "War": "Guerra",
        "Western": "Western",
    }

    generos_es = []

    for genero_en in generos_en:

        if genero_en in traducciones_generos.keys():
            genero_es = traducciones_generos[genero_en]
        else:
            genero_es = genero_en

        generos_es.append(genero_es)
    

    return generos_es