import unittest
from estructura import ConstructorArbol

"""
resultado_asi= 
 0: elementos dentro de la parentisis es una cadena
 1: False o True , donde False significa que es elemento compuesto
 2: la funcion recortada
ej: (3+4)*2+2          => 0: 3+4      , 1: False, 2: *2+2
ej: (4*(3+4))*2+2      => 0: 4*(3+4)  , 1: False, 2: *2+2 
ej: (3+4)*(2+2)        => 0: 3+4      , 1: False, 2: *(2+2)
ej: 4+(3*2)-1          => 0: 4        , 1: True , 2: (3*2)-1
"""


class TestJerarquias(unittest.TestCase):

  def test_positivo_obtener_elemento1(self):
    elemento = "(3+4)*2+2"
    esperado0 = "3+4"
    esperado1 = False
    esperado2 = "*2+2"
    res = ConstructorArbol.obtener_elemento(elemento)
    self.assertEqual(res[0], esperado0)
    self.assertEqual(res[1], esperado1)
    self.assertEqual(res[2], esperado2)

  # ojito
  def test_positivo_obtener_elemento2(self):
    elemento = "(40*(13+334))*2+2"
    esperado0 = "40*(13+334)"
    esperado1 = False
    esperado2 = "*2+2"
    res = ConstructorArbol.obtener_elemento(elemento)
    self.assertEqual(res[0], esperado0)
    self.assertEqual(res[1], esperado1)
    self.assertEqual(res[2], esperado2)

  def test_positivo_obtener_elemento3(self):
    elemento = "(3+4)*(2+2)"
    esperado0 = "3+4"
    esperado1 = False
    esperado2 = "*(2+2)"
    res = ConstructorArbol.obtener_elemento(elemento)
    self.assertEqual(res[0], esperado0)
    self.assertEqual(res[1], esperado1)
    self.assertEqual(res[2], esperado2)

  def test_positivo_obtener_elemento4(self):
    elemento = "40+(30*122)-1"
    esperado0 = "40"
    esperado1 = True
    esperado2 = "+(30*122)-1"
    res = ConstructorArbol.obtener_elemento(elemento)
    self.assertEqual(res[0], esperado0)
    self.assertEqual(res[1], esperado1)
    self.assertEqual(res[2], esperado2)

  def test_positivo_obtener_elemento41(self):
    elemento = "400+(30*122)-1"
    esperado0 = "400"
    esperado1 = True
    esperado2 = "+(30*122)-1"
    res = ConstructorArbol.obtener_elemento(elemento)
    self.assertEqual(res[0], esperado0)
    self.assertEqual(res[1], esperado1)
    self.assertEqual(res[2], esperado2)



  # este debe ser simple.
  def test_positivo_obtener_elemento5(self):
    elemento = "(30*211)"
    esperado0 = "30*211"
    esperado1 = False
    esperado2 = ""
    res = ConstructorArbol.obtener_elemento(elemento)
    self.assertEqual(res[0], esperado0)
    self.assertEqual(res[1], esperado1)
    self.assertEqual(res[2], esperado2)


if __name__ == '__main__':
  unittest.main()
