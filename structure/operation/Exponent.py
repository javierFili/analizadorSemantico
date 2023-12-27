from structure.exceptions.NodeException import NodeException
from structure.value.Operation import Operation

class Exponent(Operation):
  # Initialize the node
  def __init__(self):
    super(Exponent, self).__init__()
    self.weight = 3
    self.symbol = '^'

  # Evaluate the node
  def evaluate(self):
    if self.left and self.right:
      lvalue = self.left.evaluate()
      rvalue = self.right.evaluate()
      # Exponents are dumb and mean when negative numbers are involved
      if lvalue < 0:
        if rvalue == int(rvalue):
          return lvalue ** rvalue
        else:
          # The answer will be complex
          return (lvalue + 0j) ** rvalue
      else:
        return lvalue ** rvalue
    else:
      raise NodeException('Node does not have enough children.')
