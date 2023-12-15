import unittest
from estructura import ConstructorArbol


class TestJerarquias(unittest.TestCase):
  def test_suma_agrega_parentisis0(self):
    expresion = '4+3*3+2'
    resultado = '4+(3*3)+2'
    self.assertEqual(ConstructorArbol.agrega_parentesis(expresion, 2, 4), resultado)

  def test_suma_agrega_parentisis01(self):
    expresion = '4+3*3*2'
    resultado = '4+(3*3*2)'
    self.assertEqual(ConstructorArbol.agrega_parentesis(expresion, 2, 6), resultado)

  def test_suma_agrega_parentisis02(self):
    expresion = '4*3*3+2'
    resultado = '(4*3*3)+2'
    self.assertEqual(ConstructorArbol.agrega_parentesis(expresion, 0, 4), resultado)

  def test_suma_agrega_parentisis2(self):
    expresion = '4+3*3+2'
    resultado = '4+(3*3)+2'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)

  def test_suma_agrega_parentisis3(self):
    expresion = '4+3*3*2'
    resultado = '4+(3*3*2)'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)

  def test_suma_agrega_parentisis4(self):
    expresion = '4*3*3+2'
    resultado = '(4*3*3)+2'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)

  def test_suma_agrega_parentisis4(self):
    expresion = '4+3*3+2*3'
    resultado = '4+(3*3)+(2*3)'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)

  def test_suma_agrega_parentisis41(self):
    expresion = '4+3*3+2*3+4/3'
    resultado = '4+(3*3)+(2*3)+(4/3)'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)

  def test_suma_agrega_parentisis43(self):
    expresion = '4+3*3+2/3'
    resultado = '4+(3*3)+(2/3)'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)

  def test_suma_agrega_parentisis42(self):
    expresion = '4+3*3+2*3-3-2+3/4'
    resultado = '4+(3*3)+(2*3)-3-2+(3/4)'
    self.assertEqual(ConstructorArbol.jerarquizar_operaciones(expresion), resultado)


if __name__ == '__main__':
  unittest.main()
