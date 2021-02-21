from gestor_archivos.manager_de_configuracion import cargar_configuracion

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
