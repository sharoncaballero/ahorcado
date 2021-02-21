
def dividir_texto_en_palabras_correctas(nombre_archivo):
    """Lee un archivo de a una linea y genera una lista ordenada de palabras correctas"""
    caracteres_tildes = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ã": "a", "â": "a"}
    caracteres_borrar = """{}[](),.'"!?¿¡º+*-\t@#$%:;&_=/"""
    for c in caracteres_borrar:
        caracteres_tildes[c] = ""

    palabras = set()
    with open(nombre_archivo, "r", encoding="latin-1") as archivo:
        for line in archivo:
            linea = line.lower()[:-1]
            for letra in caracteres_tildes:
                linea = linea.replace(letra, caracteres_tildes[letra])
            for palabra in linea.split(" "):
                if palabra.isalpha():
                    palabras.add(palabra)

    return sorted(list(palabras))

def generar_archivo_de_palabras(palabras, nombre_archivo):
    """Crea un archivo de texto a partir de una lista de palabras"""
    with open(nombre_archivo, "w") as archivo:
        for palabra in palabras:
            archivo.write(palabra+"\n")

def extraer_palabras(palabras,nombre_archivo):
    """Extrae las palabras de un archivo"""
    with open(nombre_archivo, "r") as archivo:
        for palabra in archivo:
            palabras.add(palabra[:-1])

def mezclar_archivos():
    """Toma las palabras de los tres archivos y genera un nuevo archivo manteniendo el orden alfabético"""
    palabras = set()
    extraer_palabras(palabras, "configuracion/palabras_texto_1.txt")
    extraer_palabras(palabras, "configuracion/palabras_texto_2.txt")
    extraer_palabras(palabras, "configuracion/palabras_texto_3.txt")
    tabla_de_longitud = {}
    for palabra in palabras:
        largo = len(palabra)
        tabla_de_longitud[largo] = tabla_de_longitud.get(largo,0) + 1

    generar_archivo_de_palabras(sorted(list(palabras)),"configuracion/palabras.txt")
    return tabla_de_longitud,len(palabras)

def crear_archivo_de_palabras():
    palabras = dividir_texto_en_palabras_correctas("textos/Cuentos.txt")
    generar_archivo_de_palabras(palabras, "configuracion/palabras_texto_1.txt")

    palabras = dividir_texto_en_palabras_correctas("textos/La araña negra - tomo 1.txt")
    generar_archivo_de_palabras(palabras, "configuracion/palabras_texto_2.txt")

    palabras = dividir_texto_en_palabras_correctas("textos/Las 1000 Noches y 1 Noche.txt")
    generar_archivo_de_palabras(palabras, "configuracion/palabras_texto_3.txt")

    tabla_de_longitud, total = mezclar_archivos()
    print(tabla_de_longitud, total)
    return crear_archivo_de_palabras