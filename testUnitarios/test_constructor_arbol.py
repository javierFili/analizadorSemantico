import unittest
from estructura import ConstructorArbol


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

if __name__ == '__main__':
  unittest.main()
