def buscar_palabras_de_longitud(longitud):
    """Busca palabras con la longitud dada"""
    lista = []
    with open("configuracion/palabras.txt", "r") as archivo:
        for linea in archivo:
            if len(linea[:-1]) == longitud:
                lista.append(linea[:-1])
    return lista

def salvar_resultados(nombres_participantes,puntaje_historico):
    titulo = "nombre del jugador, total de aciertos, total de desaciertos, puntaje total, palabras\n"
    jugadores = [(puntaje_historico[nombre]['puntos'],nombre)  for nombre in puntaje_historico]
    jugadores = sorted(jugadores,key=lambda x:x[0],reverse=True)
    with open("configuracion/partida.csv","w") as archivo:
        archivo.write(titulo)
        for puntos,nombre in jugadores:
            fila = nombre+","+str(puntaje_historico[nombre]['aciertos'])+","+str(puntaje_historico[nombre]['desaciertos'])+","+str(puntos)+","
            for palabra in puntaje_historico[nombre]['palabras']:
                fila = fila + " " + palabra
            archivo.write(fila+"\n")