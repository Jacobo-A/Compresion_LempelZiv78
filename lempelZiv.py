# Autor: Alejandro Flores Jacobo 
# Fecha: 14-05-2023
# Descripcion: 
# Script aplicar el algoritmo de compresion LempelZiv78 a un archivo.


# ---------------------------[Funcion para extraer los elementos que se repiten]---------------------------


def contennt(s_strings):    
    contenido = [] 

# La función utiliza un bucle "while" para iterar sobre la lista de strings hasta que no queden elementos por procesar. 
# En cada iteración, la función comprueba si el primer elemento de la lista ya está en la lista de contenido. 
# Si es así, la función crea un nuevo string que es la concatenación del primer y segundo elemento de la lista, 
# y luego elimina ambos elementos de la lista original. Este nuevo string se inserta al principio de la lista "s_strings".
    while True:
        try:
            if s_strings[0] in contenido:
                c = s_strings[0] + s_strings[1]
                del s_strings[:2]
                s_strings.insert(0,c)     
            else:          
                # Si el primer elemento de la lista "s_strings" no está en la lista "contenido", 
                # se añade a la lista "contenido" y se elimina de "s_strings".
                contenido.append(s_strings[0])
                s_strings.pop(0)
            if len(s_strings) == 0:
                break
        except IndexError:
            pass
            break
    return contenido
      
# ---------------------------[Funcion para crear el diccionario de content/location]---------------------------
def location(content):
    localizacion = {}  #content/location
    n = len(content)   # Numero de elementos location
    
    formato = "{0:02x}" # Formato Hexadecimal
    try:
        localizacion[''] = formato.format(0)   # Se agrega como primer elemento valor  '': '000'
        for i in range(n):
            localizacion[content[i]] = formato.format(i+1)  # Se anade el contenido con el formato

    except IndexError:
            pass

    return localizacion


# ---------------------------[Codificador/Funcion para crea los codeword]---------------------------
def codeword(location):
    # Obtener la llave del segundo elemento
    llave = list(location.items())[1][0]

    # Obtenemos la longitud mínima de una llave en el diccionario
    longitud_minima = len(llave)

    c = []
    s = ''

    for key in location:
        try:
            s = key[-1]     # Lo utilizamos para producir un error y que omita el primer item del diccionario

            # Luego, la función obtiene los últimos caracteres de la llave (hasta la longitud mínima) y los almacena en la variable s.
            s = key[-longitud_minima:]
            # Si la longitud de la llave es igual a la longitud mínima, la función agrega al inicio del código la cadena vacía en el diccionario location más s.
            if len(key) == longitud_minima: 
                s = location[''] + s
            # Si la longitud de la llave es mayor que la longitud mínima, 
            # la función obtiene la subcadena de la llave que excluye los últimos caracteres (de longitud mínima) 
            # y la utiliza como llave en el diccionario para obtener su respectivo valor. Este valor se concatena con s y se agrega a la lista c.
            else:         
                s = location[key[:-longitud_minima]] + s
            c.append(s)
        except IndexError:
                pass
    return c    # Retorna un string con los codigo concatenados


# ---------------------------[Codificador/Funcion para crea los codeword]---------------------------
def decodeword(location):
    print('location', location)

    indice = list(location.values())[0]     # El indice no indican los caracteres que hay para un solo caracte ej 0 y 1
    print('indice', indice)

    location = modificarDic(location)       # invirte los valor de un diccionario, esto ddbido que se hace uso de la funcion location()

    c = []  # Codigo
    s = ''  # Secuencia
    for key in location:
        try:
            s = location[key][:-1]      # Toma los caractes a excepcion del primero a la derecha
            if indice == s:             # Si el caracter concide con el indice solo el extrar el primer caracter a la derecha
                s = location[key][-1]
                location[key] = s       # Al item actual le remplazamos el valor de la secuencia o  primer caracter
                c.append(s)
            else:                                       # A secuencia de le da el valor de los caracter restantes se concatena: 
                s = location[s] + location[key][-1]     # el valor de la llave s  + con el primer caracter de la llave actual
                location[key] = s       # Al item actual le remplazamos el valor de la secuencia o  primer caracter
                c.append(s)
        except:
            pass
    
    return c
        
def modificarDic(location):  # Inviere los valores de un diccionario a excepcion del primero
    nuevo_diccionario = {}
    primer_item = True

    for clave, valor in location.items():
        if primer_item:
            nuevo_diccionario[clave] = valor
            primer_item = False
        else:
            nuevo_diccionario[valor] = clave
    
    return nuevo_diccionario


# ---------------------------[Archivo de Salida]---------------------------
def crearArchivo(cadena, nombreArchivo):

    # inicializar una cadena vacía para almacenar los caracteres UTF-16
    cadena_utf16 = []

    # iterar sobre la lista de cadenas
    for elem in cadena:
        # extraer el valor hexadecimal
        hex_valor = elem[:-1]
   
        # convertir el valor hexadecimal a un número entero
        int_valor = int(hex_valor, 16)


        # convertir el número entero en un carácter UTF-16
        char_utf16 = chr(int_valor)

        # # agregar el carácter UTF-16 a la cadena resultante
        cadena_utf16.append(char_utf16 + elem[-1])

    # imprimir la cadena resultante
    print(cadena_utf16)
    # Guardar los datos decodificados en un archivo
    with open(nombreArchivo, 'w') as f:
        f.write(''.join(cadena))
        f.close()
        # f.write(''.join(cadena_utf16))
# ---------------------------[Texto de entrada]---------------------------
import base64
 

# Cargar la imagen como bytes
with open("archivo.bin", "rb") as file:
    encoded_string = base64.b64encode(file.read())
    file.close()

cadena = encoded_string.decode('utf-16')  #Obrenemos simbolos de 16 bites en una cadena
# cadena = '010110100101'
s_strings = list(map(str, cadena))      # Secuencia s en string


print(cadena,'\n', len(s_strings))

contenido = contennt(s_strings)    # Lista de elementos que se repiten
print('contenido',contenido)
localizacion = location(contenido)  # Diccionario content/location
print('localizaicon', localizacion)
codigo = codeword(localizacion)     # Cadena con los codigos concatenados
print('codigo', codigo, len(''.join(codigo)))

crearArchivo(codigo, 'archivo_Codificado.lpzv')

#------------------------------------[Decodificacion]-------------------------------------

# Cargar la imagen como bytes
with open("archivo_Codificado.lpzv", "r") as file:
    cadena = file.read()
    file.close()
print('esto',cadena, len(cadena))

# Longitud de cada segmento
longitud_segmento = 3

# Dividir la cadena en segmentos de igual longitud
codigo = [cadena[i:i+longitud_segmento] for i in range(0, len(cadena), longitud_segmento)]

# Mostrar la lista resultante
print(codigo)


localizacion = location(codigo)  # Diccionario content/location
decodificacion = decodeword(localizacion)

decodificacion = ''.join(decodificacion)
print(decodificacion)
# Volver a convertir la cadena de texto en bytes
decodificacion = decodificacion.encode('utf-16')
# Decodificar la cadena codificada en base64
decodificacion = base64.b64decode(decodificacion)

# Guardar los datos decodificados en un archivo
with open('archivo_Decodificado.bin', 'wb') as f:
    f.write(decodificacion)