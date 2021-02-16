from gestor_archivos.resumir_texto import dividir_texto_en_palabras_correctas, generar_archivo_de_palabras, mezclar_archivos
from juego_ahorcado.ahorcado import jugar

palabras = dividir_texto_en_palabras_correctas("textos/Cuentos.txt")
generar_archivo_de_palabras(palabras, "configuracion/palabras_texto_1.txt")

palabras = dividir_texto_en_palabras_correctas("textos/La araña negra - tomo 1.txt")
generar_archivo_de_palabras(palabras, "configuracion/palabras_texto_2.txt")

palabras = dividir_texto_en_palabras_correctas("textos/Las 1000 Noches y 1 Noche.txt")
generar_archivo_de_palabras(palabras, "configuracion/palabras_texto_3.txt")


tabla_de_longitud,total = mezclar_archivos()
print(tabla_de_longitud,total)

jugar(tabla_de_longitud)