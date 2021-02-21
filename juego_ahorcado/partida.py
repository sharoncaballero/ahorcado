from juego_ahorcado.validar_entrada import ingresar_letra

def reemplazar_letra(palabra, palabra_oculta, letra):
    """Esta funcion indica si la letra es parte de la palabra y en ese caso lo agrega en la palabra oculta"""
    palabra_nueva = ""
    adivino = False
    for posicion in range(len(palabra)):
        if palabra[posicion] == letra:
            adivino=True
            palabra_nueva = palabra_nueva + letra
        else:
            palabra_nueva = palabra_nueva + palabra_oculta[posicion]
    return palabra_nueva, adivino

def partida(nombres_participantes,palabras,palabras_ocultas,max_desaciertos,puntos_aciertos,puntos_desaciertos,puntos_adivina):
    """Bucle correspondiente a una partida entera"""

    puntaje = {nombre: {"puntos": 0, "aciertos": 0, "desaciertos": 0} for nombre in nombres_participantes}

    vidas = {nombre:max_desaciertos for nombre in nombres_participantes}

    jugadores_vivos = len(nombres_participantes)

    while jugadores_vivos != 0:

        for i in range(len(nombres_participantes)):
            # El turno de un jugador
            nombre = nombres_participantes[i]

            # Veo si esta con vida
            if vidas[nombre] > 0:
                print("Turno", nombre)
                print("Cantidad de Aciertos= ", puntaje[nombre]["aciertos"])
                print("Cantidad de Desaciertos= ", puntaje[nombre]["desaciertos"])
                print("Cantidad de Puntos= ", puntaje[nombre]["puntos"])
                print(palabras_ocultas[i])
                letra = ingresar_letra(palabras_ocultas[i])
                palabras_ocultas[i], adivino = reemplazar_letra(palabras[i], palabras_ocultas[i], letra)

                # Actualizo puntaje y vidas dependiendo si adivino o no
                if adivino:
                    print("Correcto", palabras_ocultas[i])
                    puntaje[nombre]["puntos"] = puntaje[nombre]["puntos"] + puntos_aciertos
                    puntaje[nombre]["aciertos"] = puntaje[nombre]["aciertos"] + 1
                    if "_" not in palabras_ocultas[i]:
                        print("------------------------------ GANASTE!!!!! ---------------------------------------")
                        puntaje[nombre]["puntos"] = puntaje[nombre]["puntos"] + puntos_adivina
                        return puntaje, nombre

                else:
                    vidas[nombre] = vidas[nombre] - 1
                    print("Incorrecto tienes", vidas[nombre], "vidas")
                    puntaje[nombre]["puntos"] = puntaje[nombre]["puntos"] - puntos_desaciertos
                    puntaje[nombre]["desaciertos"] = puntaje[nombre]["desaciertos"] + 1

                    if vidas[nombre] == 0:
                        jugadores_vivos = jugadores_vivos - 1
                print("."*54+"\n")

    # Cuando todos pierden gana el Programa
    print("------------------------------Los he derrotado a todos!!---------------------------")
    return puntaje, "Programa"

