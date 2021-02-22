def cargar_configuracion(nombre, defecto):
    """Busca una determinada configuracion en eel archivo de
     configuraciones en el caso que no sea correcta devuelve el defecto
     """
    with open("configuracion/configuracion.txt", "r") as archivo:
        for linea in archivo:
            lista = linea.replace("\n", "").split(" ")
            if len(lista) >= 2 and nombre == lista[0] and lista[1].isdigit():
                return int(lista[1])
    return defecto