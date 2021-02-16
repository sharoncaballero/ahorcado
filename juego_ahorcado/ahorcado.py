import random
from gestor_archivos.manager_de_configuracion import cargar_configuracion
from gestor_archivos.navegador import buscar_palabras_de_longitud, salvar_resultados

def consultar_participantes():
    """Pide al usuario ingresar el numero de participantes y verifique que este correcto"""
    max_usuarios = cargar_configuracion("MAX_USUARIOS", 10)
    while True:
        numero_participantes = input("Ingrese numero de jugadores. El numero no debe ser mayor que "+str(max_usuarios) + ": ")
        if numero_participantes.isdigit():
            numero_participantes = int(numero_participantes)
            if 0 < numero_participantes <= max_usuarios:
                return numero_participantes

def consultar_nombres(numero_participantes):
    """Pide al ususario ingresar el nombre de los jugadores y verifica que sean correctos"""
    nombres_participantes = []
    for i in range(numero_participantes):
        nombre_incorrecto = True
        while nombre_incorrecto:
            nombre_jugador = input("Ingrese nombre del jugador "+str(i+1)+". Este solo puede tener letras o espacios:\n")
            if nombre_jugador.replace(" ", "").isalpha():
                if nombre_jugador in nombres_participantes:
                    print("El nombre ya fue ingresado")
                elif nombre_jugador == "Programa":
                    print("Ese nombre esta reservado")
                else:
                    nombres_participantes.append(nombre_jugador)
                    nombre_incorrecto = False
    return nombres_participantes

def mezclar_jugadores(nombres_participantes):
    """Mezcla e informa el orden de los jugadores"""
    print("----------- Bienvenido/s al juego! -------------------")
    random.shuffle(nombres_participantes)
    contador = 0
    for nombre in nombres_participantes:
        contador = contador + 1
        print("Jugador", str(contador)+":", nombre)
    print("."*54)

def consultar_longitud(numero_participantes, tabla_de_longitud):
    """Consulta la longitud deseada de letras que debe tener la palabra
    asegurandose que sea posible realizarse el juego
    """
    long_palabra_min = cargar_configuracion("LONG_PALABRA_MIN", 5)
    while True:
        longitud = input("Ingrese longitud de las palabras a adivinar. Debe ser mayor que "+str(long_palabra_min)+": ")
        if longitud.isdigit():
            longitud = int(longitud)
            if long_palabra_min <= longitud:
                if tabla_de_longitud.get(longitud, 0) >= numero_participantes:
                     return longitud

def ingresar_letra(palabra):
    """Pide una letra y lo valida"""
    while True:
        letra = input("Ingrese una letra: ")
        if letra.isalpha() and len(letra) == 1:
            letra = letra.lower()
            if letra in palabra:
                print("Esa letra ya esta incluida.")
            else:
                return letra
        else:
            print("Caracter incorrecto intente otro.")

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
def descripcion_fin_partida(nombres_participantes, palabras, palabras_ocultas,  puntaje, partidas):
    """"""
    titulo = "| NOMBRE      | PALABRA       | PALABRA OCULTA | PUNTAJE | ACIERTOS | DESACIERTOS | #PARTIDAS |\n"
    print(titulo)
    filas = []
    for i,nombre in enumerate(nombres_participantes):
        fila = "| " + nombre[:12] + " "*(12-len(nombre[:12]))
        fila = fila + "| " + palabras[i][:14] + " "*(14-len(palabras[i][:14]))
        fila = fila + "| " + palabras_ocultas[i][:15] + " "*(15-len(palabras_ocultas[i][:15]))
        fila = fila + "| " + str(puntaje[nombre]["puntos"])[:8] + " "*(8-len(str(puntaje[nombre]["puntos"])[:8]))
        fila = fila + "| " + str(puntaje[nombre]["aciertos"])[:9] + " "*(9-len(str(puntaje[nombre]["aciertos"])[:9]))
        fila = fila + "| " + str(puntaje[nombre]["desaciertos"])[:12] + " "*(12-len(str(puntaje[nombre]["desaciertos"])[:12]))
        fila = fila + "| " + str(partidas)[:10] + " "*(10 - len(str(partidas)[:10]))+"|"
        filas.append((puntaje[nombre]["puntos"], fila))
    filas = sorted(filas,key=lambda x:x[0],reverse=True)
    filas = "\n".join([x for _,x in filas])
    print(filas)
    print("."*83)


def partida(nombres_participantes,palabras,palabras_ocultas,max_desaciertos,puntos_aciertos,puntos_desaciertos,puntos_adivina):
    """"""
    puntaje = {nombre: {"puntos": 0, "aciertos": 0, "desaciertos": 0} for nombre in nombres_participantes}
    vidas = {nombre:max_desaciertos for nombre in nombres_participantes}
    jugadores_vivos = len(nombres_participantes)
    while jugadores_vivos != 0:
        for i in range(len(nombres_participantes)):
            nombre = nombres_participantes[i]
            if vidas[nombre] > 0:
                print("Turno", nombre)
                print("Cantidad de Aciertos= ", puntaje[nombre]["aciertos"])
                print("Cantidad de Desaciertos= ", puntaje[nombre]["desaciertos"])
                print("Cantidad de Puntos= ", puntaje[nombre]["puntos"])
                print(palabras_ocultas[i])
                letra = ingresar_letra(palabras_ocultas[i])
                palabras_ocultas[i], adivino = reemplazar_letra(palabras[i], palabras_ocultas[i], letra)
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
    return puntaje, "Programa"

def volver_a_jugar():
    """"""
    while True:
        letra = input("Desea volver a jugar?     si / no: ")
        if letra == "si":
            return True
        elif letra == "no":
            return False
        print("Opcion incorrecta")

def reordenar_jugadores(nombres_participantes,ganador,puntaje_historico):

    jugadores =[(puntaje_historico[nombre]['puntos'], nombre) for nombre in nombres_participantes if nombre != ganador]
    jugadores = sorted(jugadores,key=lambda x:x[0],reverse=True)
    if ganador != 'Programa':
        jugadores = [ganador] + [x for _, x in jugadores]
    return jugadores



def jugar(tabla_de_longitud):
    puntos_adivina = cargar_configuracion("PUNTOS_ADIVINA", 30)
    max_desaciertos = cargar_configuracion("MAX_DESACIERTOS", 7)
    puntos_aciertos = cargar_configuracion("PUNTOS_ACIERTOS", 2)
    puntos_desaciertos = cargar_configuracion("PUNTOS_DESACIERTOS", 1)
    numero_participantes = consultar_participantes()
    nombres_participantes = consultar_nombres(numero_participantes)
    mezclar_jugadores(nombres_participantes)

    partidas = 1
    puntaje_historico = {}
    seguir_jugando = True

    while seguir_jugando:
        longitud = consultar_longitud(numero_participantes, tabla_de_longitud)

        palabras = buscar_palabras_de_longitud(longitud)
        palabras = random.sample(palabras, numero_participantes)
        palabras_ocultas = ["_"*longitud for i in range(numero_participantes)]
        puntaje,ganador = partida(nombres_participantes, palabras, palabras_ocultas,max_desaciertos,puntos_aciertos,puntos_desaciertos,puntos_adivina)

        if partidas == 1:
            puntaje_historico = puntaje
            for pos,nombre in enumerate(nombres_participantes):
                puntaje_historico[nombre]['palabras'] = [palabras[pos]]
        else:
            for x in puntaje_historico:
                for y in ['puntos','aciertos','desaciertos']:
                    puntaje_historico[x][y] = puntaje_historico[x][y] + puntaje[x][y]
            for pos,nombre in enumerate(nombres_participantes):
                puntaje_historico[nombre]['palabras'] = puntaje_historico[nombre]['palabras'] + [palabras[pos]]
        descripcion_fin_partida(nombres_participantes, palabras, palabras_ocultas,  puntaje_historico,partidas)
        seguir_jugando = volver_a_jugar()
        nombres_participantes = reordenar_jugadores(nombres_participantes,ganador,puntaje_historico)
        partidas = partidas + 1

    salvar_resultados(nombres_participantes,puntaje_historico)

