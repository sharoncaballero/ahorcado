import random
from gestor_archivos.manager_de_configuracion import cargar_configuracion
from gestor_archivos.navegador import buscar_palabras_de_longitud, salvar_resultados
from juego_ahorcado.partida import partida
from juego_ahorcado.validar_entrada import consultar_participantes, consultar_nombres, \
    consultar_longitud, volver_a_jugar


def mezclar_jugadores(nombres_participantes):
    """Mezcla e informa el orden de los jugadores"""
    print("----------- Bienvenido/s al juego! -------------------")
    random.shuffle(nombres_participantes)
    contador = 0
    for nombre in nombres_participantes:
        contador = contador + 1
        print("Jugador", str(contador)+":", nombre)
    print("."*54)

def reordenar_jugadores(nombres_participantes,ganador,puntaje_historico):
    """Reordena los jugadores por puntaje, poniendo primero al ganador de la ultima partida."""
    jugadores =[(puntaje_historico[nombre]['puntos'], nombre) for nombre in nombres_participantes if nombre != ganador]
    jugadores = sorted(jugadores,key=lambda x:x[0],reverse=True)
    if ganador != 'Programa':
        jugadores = [ganador] + [x for _, x in jugadores]
    return jugadores


def descripcion_fin_partida(nombres_participantes, palabras, palabras_ocultas,  puntaje, partidas):
    """Imprime el resultado final de una partida ordenado por puntaje mas alto a mas bajo"""
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
    filas = "\n".join([x for puntos,x in filas])
    print(filas)
    print("."*83)

def acumular_puntaje(nombres_participantes,puntaje,partidas,puntaje_historico,palabras):
    """Actualiza el puntaje y agrega las palabras que le toco a cada jugador"""
    if partidas == 1:
        puntaje_historico = puntaje
        for pos, nombre in enumerate(nombres_participantes):
            puntaje_historico[nombre]['palabras'] = [palabras[pos]]
    else:
        for x in puntaje_historico:
            for y in ['puntos', 'aciertos', 'desaciertos']:
                puntaje_historico[x][y] = puntaje_historico[x][y] + puntaje[x][y]
        for pos, nombre in enumerate(nombres_participantes):
            puntaje_historico[nombre]['palabras'] = puntaje_historico[nombre]['palabras'] + [palabras[pos]]
    return puntaje_historico

def jugar(tabla_de_longitud):
    """Bucle principal del juego ahorcado"""

    #Cargar Configuracion
    puntos_adivina = cargar_configuracion("PUNTOS_ADIVINA", 30)
    max_desaciertos = cargar_configuracion("MAX_DESACIERTOS", 7)
    puntos_aciertos = cargar_configuracion("PUNTOS_ACIERTOS", 2)
    puntos_desaciertos = cargar_configuracion("PUNTOS_DESACIERTOS", 1)

    #Validar cantidad de jugadores
    numero_participantes = consultar_participantes()

    #Validar nombres de jugadores
    nombres_participantes = consultar_nombres(numero_participantes) #Ej: ['Sharon','Sarah', ...]

    mezclar_jugadores(nombres_participantes)

    partidas = 1
    puntaje_historico = {}
    seguir_jugando = True

    while seguir_jugando:
        # Ingrese longitud...
        longitud = consultar_longitud(numero_participantes, tabla_de_longitud)

        #Buscando TODAS las palabras de largo LONGITUD
        palabras = buscar_palabras_de_longitud(longitud)

        #Elijo al azar 1 para cada jugador
        palabras = random.sample(palabras, numero_participantes)

        #Descomentar para debug
        #print(palabras)


        #Creo la misma cantidad de palabras pero ocultas
        palabras_ocultas = ["_"*longitud for i in range(numero_participantes)]

        #Que empiece el juego
        puntaje,ganador = partida(nombres_participantes, palabras, palabras_ocultas,max_desaciertos,puntos_aciertos,puntos_desaciertos,puntos_adivina)

        puntaje_historico = acumular_puntaje(nombres_participantes, puntaje, partidas, puntaje_historico, palabras)

        descripcion_fin_partida(nombres_participantes, palabras, palabras_ocultas,  puntaje_historico,partidas)

        seguir_jugando = volver_a_jugar()

        nombres_participantes = reordenar_jugadores(nombres_participantes,ganador,puntaje_historico)

        partidas = partidas + 1

    salvar_resultados(nombres_participantes,puntaje_historico)


