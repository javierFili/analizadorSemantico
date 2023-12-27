import math
from structure.exceptions.EvalException import EvalException
from structure.exceptions.NodeException import NodeException
from structure.exceptions.ParseException import ParseException
from structure.value.Operation import Operation
from structure.operation.Divide import Divide
from structure.operation.Exponent import Exponent
from structure.operation.Minus import Minus
from structure.operation.Times import Times


class Factorial(Operation):
  # Initialize the node
  def __init__(self):
    super(Factorial, self).__init__()
    self.weight = 4
    self.symbol = '!'
    self.arity = 1

  # Add a child to the node
  def addChild(self, child):
    if self.left is None:
      self.left = child
      child.parent = self
    else:
      raise NodeException('Node already has one child.')

  # Remove a child from the node
  def removeChild(self):
    if self.left is not None:
      c = self.left
      self.left = None
      c.parent = None
      return c
    else:
      raise NodeException('Node has no children to remove.')

  # Evaluate the node
  def evaluate(self):
    if self.left is not None and self.right is None:
      cvalue = self.left.evaluate()
      # Right now factorial is only defined for the natural numbers
      if cvalue >= 0 and cvalue == int(cvalue):
        return math.factorial(cvalue)
      else:
        raise EvalException('Cannot compute the factorial of negative numbers or non-integers.')
    else:
      raise NodeException('Node does not have enough children.')


# Return an object of the correct type given the symbol representing an operation
def getOperation(operation_symbol):
  if operation_symbol == '+':
    return Plus()
  elif operation_symbol == '-':
    return Minus()
  elif operation_symbol == '*':
    return Times()
  elif operation_symbol == '/':
    return Divide()
  elif operation_symbol == '^':
    return Exponent()
  elif operation_symbol == '!':
    return Factorial()
  else:
    raise ParseException('Unknown operation "' + operation_symbol + '"')


class Plus(Operation):
  # Initialize the node
  def __init__(self):
    super(Plus, self).__init__()
    self.weight = 1
    self.symbol = '+'

  # Evaluate the node
  def evaluate(self):
    if self.left and self.right:
      return self.left.evaluate() + self.right.evaluate()
    else:
      raise NodeException('Node does not have enough children.')
