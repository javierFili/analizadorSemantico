from estructura.Arbol import Arbol

"""
 * Existen elementos compuesto : (2*3) , (2-1).. para ser compuesto valido debe contener: un signo matematico, +,-,/,*.
 * Existen elementos simples  : 1 , * , - ,+..
 * Para que un arbol este listo semanticamente, no debe contener nodos con elementos compuestos, si no que sean elementos simples.
 * 
"""


def agrega_parentesis(expresion, izq, der):
  # cadena_modificada = expresion[:i - 1] + "(" + expresion[i - 1:i + 2] + ")" + expresion[i + 2:]
  cadena_modificada = expresion[:izq] + "(" + expresion[izq:der + 1] + ")" + expresion[der + 1:]
  return cadena_modificada


def jerarquizar_operaciones(expresion):
  i = 0
  termina = len(expresion)
  while i + 1 < termina:
    i += 1
    termina = len(expresion)
    if (expresion[i] == '*'):
      posicion_parentesis_izq = i - 1
      posicion_parentesis_der = i + 1
      while (i + 1 < len(expresion)):
        i += 1
        if (expresion[i] == '*'):
          posicion_parentesis_der = i + 1
        elif (expresion[i] == '+' or expresion[i] == '-' or expresion[i] == '/'):
          break
      expresion = agrega_parentesis(expresion, posicion_parentesis_izq,
                                    posicion_parentesis_der)  # agregamos () en un 3*2 = (3*2)
      i = posicion_parentesis_der + 1
    elif (expresion[i] == '/'):
      posicion_parentesis_izq = i - 1
      posicion_parentesis_der = i + 1
      while (i + 1 < len(expresion)):
        i += 1
        if (expresion[i] == '/'):
          posicion_parentesis_der = i + 1
        elif (expresion[i] == '+' or expresion[i] == '-' or expresion[i] == '*'):
          break
      expresion = agrega_parentesis(expresion, posicion_parentesis_izq,
                                    posicion_parentesis_der)  # agregamos () en un 3*2 = (3*2)
      i = posicion_parentesis_der + 1
  return expresion


"""
elemento= 4+(3*3)+2
elemento_izquierda = 4
elemento_derecha = (3*3)
elemento = 2
"""


def obtener_elemento(funcion):
  if funcion == '':
    return ('', False, "")  # podriamos mandar none, cuando ya se termino.
  """if len(funcion) == 5 and funcion[0] == '(' and funcion[4] == ')':
    funcion = funcion.replace('(', "")
    funcion = funcion.replace(')', "")"""

  if funcion[0].isdigit():
    j = 0
    while j < len(funcion) and funcion[j].isdigit():
      j += 1
    res = funcion[:j]
    funcion = funcion[j:]
    return (res, True, funcion)
  else:
    cantidad_parentisis = 0
    inicio = 0
    final = 0
    for i in range(len(funcion)):
      if funcion[i] == '(':
        if inicio != 0:
          inicio = i
          cantidad_parentisis = 1
        cantidad_parentisis += 1
      elif funcion[i] == ')':
        final = i
        cantidad_parentisis -= 1
      if cantidad_parentisis == 0:
        break

    elementos_con_parentesis = funcion[1:final]
    funcion = funcion[final + 1:]
    return (elementos_con_parentesis, False, funcion)


# falta la implementacion del arbol ojito:
def constructor_de_Arbol_recursivo(arbol, funcion):
  if funcion == "":
    return arbol
  es_simple_o_compuesto_izquieda = obtener_elemento(funcion)
  # quizas este corte este mal posicionado, ojito
  funcion = es_simple_o_compuesto_izquieda[2]
  if len(funcion) >= 2:
    arbol.value = funcion[0]
    funcion = funcion[1:]
  es_simple_o_compuesto_derecha = obtener_elemento(funcion)
  print("IZ:", es_simple_o_compuesto_izquieda[0])
  print("De:", es_simple_o_compuesto_derecha[0])
  # ambos compuestos
  if (not es_simple_o_compuesto_izquieda[1] and not es_simple_o_compuesto_derecha[1]):
    # arbol = Arbol("")
    if arbol.value == "":
      constructor_de_Arbol_recursivo(arbol, es_simple_o_compuesto_izquieda[0])

    else:
      arbol.left = Arbol("")
      constructor_de_Arbol_recursivo(arbol.left, es_simple_o_compuesto_izquieda[0])
      arbol.right = Arbol("")
      constructor_de_Arbol_recursivo(arbol.right, es_simple_o_compuesto_derecha[0])
    # es compuesto, asi que trabajamos sobre ese elemento compuesto.
  # la izquierda es compuesta, la derecha es simple.
  if (not es_simple_o_compuesto_izquieda[1] and es_simple_o_compuesto_derecha[1]):
    # arbol.value = funcion[0]
    # arbol.left = Arbol("")
    arbol.right = Arbol(es_simple_o_compuesto_derecha[0])
    arbol.left = Arbol("")
    constructor_de_Arbol_recursivo(arbol.left, es_simple_o_compuesto_izquieda[0])

  # la izquieda es simple, la derecha es compuesta.
  if (not es_simple_o_compuesto_derecha[1] and es_simple_o_compuesto_izquieda[1]):
    # arbol.value = funcion[0]
    arbol.right = Arbol("")
    arbol.left = Arbol(es_simple_o_compuesto_izquieda[0])
    constructor_de_Arbol_recursivo(arbol.right, funcion)
  if (es_simple_o_compuesto_derecha[1] and es_simple_o_compuesto_izquieda[1]):
    # no es compuesto, asi que forma el arbol aqui mismo. y este es el caso base.
    izq = es_simple_o_compuesto_izquieda[0]
    der = es_simple_o_compuesto_derecha[0]
    arbol.left = Arbol(izq)
    arbol.right = Arbol(der)
  return arbol


def constructor_de_Arbol(funcion_matematica):
  arbol = Arbol("")
  arbol = constructor_de_Arbol_recursivo(arbol, funcion_matematica)
  arr = [((300, 500), arbol.value, (300, 500))]
  imprimir_arbol(arbol, 300, 500, arr)
  return arr


def imprimir_arbol(arbol, x, y, arreglo):
  # la primer vez el arreglo es vacio.
  if arbol is not None:
    arr = arreglo[len(arreglo) - 1]
    x1 = arr[2][0]
    y1 = arr[2][1]
    arreglo.append(((x, y), arbol.value, (x1, y1)))
    imprimir_arbol(arbol.left, x - 60, y - 60, arreglo)
    imprimir_arbol(arbol.right, x + 60, y - 60, arreglo)


if __name__ == '__main__':
  funcion_matematica = '4+3*4-3*4+4+3*4+5*3'
  # funcion_matematica = "3*4+4" #daa
  # funcion_matematica = "3*4+5*3" # daaa
  # funcion_matematica = '4+3*4-3*4+4+3*4+5*3'
  funcion_matematica = funcion_matematica.replace(" ", "")
  expresion_jerarquizada = jerarquizar_operaciones(funcion_matematica)
  # print(expresion_jerarquizada)
  arbol = constructor_de_Arbol(expresion_jerarquizada)
  print(arbol)
