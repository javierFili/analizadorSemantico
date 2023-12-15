from estructura.Arbol import Arbol
import re

"""
 * Existen elementos compuesto : (2*3) , (2-1).. para ser compuesto valido debe contener: un signo matematico, +,-,/,*.
 * Existen elementos simples  : 1 , * , - ,+..
 * Para que un arbol este listo semanticamente, no debe contener nodos con elementos compuestos, si no que sean elementos simples.
 * 
"""


def constructor_de_Arbol(funcion):
  funcion = funcion.replace(" ", "")
  arbol = Arbol("")
  constructor_de_Arbol_recursivo(arbol, funcion)


def obtener_elemento(funcion):
  elemento_simple = False
  for i in range(len(funcion)):
    if funcion[0].isdigit():
      elemento_simple = True
    else:
      break
  if elemento_simple:
    res = funcion[i:]
    funcion = funcion[:i]
    return (res, True, funcion)
  elementos_con_parentesis = re.search(r'\([^)]*\)', funcion)
  elementos_con_parentesis = elementos_con_parentesis.group()
  elementos_con_parentesis = elementos_con_parentesis[1:]
  elementos_con_parentesis = elementos_con_parentesis[:-1]
  if (len(elementos_con_parentesis) >= 3):
    funcion = funcion.replace(elementos_con_parentesis, '')
    funcion = funcion.replace("()", "")
    return (elementos_con_parentesis, False, funcion)


def obtener_signo(raiz):
  signo = raiz[0]
  raiz = raiz[1:]
  return (signo, raiz)


def constructor_de_Arbol_recursivo(raiz, funcion):
  izq = obtener_elemento(funcion)
  if not izq[1]:
    funcion = izq[2]
    raiz.left = Arbol(izq[0])
    singo = obtener_signo(funcion)
    raiz.value = singo[0]
    funcion = singo[1]
    constructor_de_Arbol_recursivo(raiz.left, funcion)
  else:
    funcion = izq[2]
    raiz.left = Arbol(izq[0])
    raiz.value = obtener_signo(funcion)
    raiz.right = Arbol(funcion[:1])

  der = obtener_elemento(raiz)
  if not der[1]:
    signo = obtener_signo(raiz)
    raiz.value = signo
    raiz.right = Arbol(der[0])
    constructor_de_Arbol_recursivo(raiz.right)


if __name__ == '__main__':
  funcion_matematica = '(4+2)*(3−2)*3'
  arbol_semantico = constructor_de_Arbol(funcion_matematica)
  print(arbol_semantico)
