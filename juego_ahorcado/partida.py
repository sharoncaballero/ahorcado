from juego_ahorcado.validar_entrada import ingresar_letra

def reemplazar_letra(palabra, palabra_oculta, letra):
    """Esta funcion indica si la letra es parte de la palabra y en ese caso lo agrega en la palabra oculta."""
    palabra_nueva = list(palabra_oculta)
    adivino = False

    for posicion,letra_palabra in enumerate(palabra):
        if letra_palabra == letra:
            adivino=True
            palabra_nueva[posicion] = letra

    palabra_nueva = ''.join(palabra_nueva)
    return palabra_nueva, adivino

def partida(nombres_participantes,palabras,palabras_ocultas,max_desaciertos,puntos_aciertos,puntos_desaciertos,puntos_adivina):
    """Bucle correspondiente a una partida entera"""

    puntaje = {nombre: {"puntos": 0, "aciertos": 0, "desaciertos": 0} for nombre in nombres_participantes}

    jugadores_vivos = len(nombres_participantes)

    total_jugadores = len(nombres_participantes)

    while jugadores_vivos != 0:

        for i in range(total_jugadores):
            # El turno de un jugador
            nombre = nombres_participantes[i]

            # Veo si tiene llego al limite de desaciertos
            if puntaje[nombre]['desaciertos'] != max_desaciertos:
                print("Turno", nombre)
                print("Cantidad de Aciertos= ", puntaje[nombre]["aciertos"])
                print("Cantidad de Desaciertos= ", puntaje[nombre]["desaciertos"])
                print("Cantidad de Puntos= ", puntaje[nombre]["puntos"])
                print("Intentos restantes= ", max_desaciertos-puntaje[nombre]['desaciertos'])
                print(palabras_ocultas[i])

                #Pido una letra al usuario
                letra = ingresar_letra(palabras_ocultas[i])

                #Veo si adivina o no y como queda la palabra oculta
                palabra_nueva, adivino = reemplazar_letra(palabras[i], palabras_ocultas[i], letra)

                #Cambio la palabra oculta por la nueva palabra oculta
                palabras_ocultas[i] = palabra_nueva

                # Actualizo puntaje dependiendo si adivino o no
                if adivino:
                    print("Correcto", palabras_ocultas[i])
                    puntaje[nombre]["puntos"] = puntaje[nombre]["puntos"] + puntos_aciertos
                    puntaje[nombre]["aciertos"] = puntaje[nombre]["aciertos"] + 1
                    if "_" not in palabras_ocultas[i]:
                        print("------------------------------ GANASTE!!!!! ---------------------------------------")
                        puntaje[nombre]["puntos"] = puntaje[nombre]["puntos"] + puntos_adivina
                        return puntaje, nombre

                else:
                    puntaje[nombre]["puntos"] = puntaje[nombre]["puntos"] - puntos_desaciertos
                    puntaje[nombre]["desaciertos"] = puntaje[nombre]["desaciertos"] + 1
                    print("Incorrecto tienes", max_desaciertos-puntaje[nombre]['desaciertos'], "intentos restantes")

                    if puntaje[nombre]['desaciertos'] == max_desaciertos:
                        jugadores_vivos = jugadores_vivos - 1
                print("."*54+"\n")

    # Cuando todos pierden gana el Programa
    print("------------------------------Los he derrotado a todos!!---------------------------")
    return puntaje, "Programa"

