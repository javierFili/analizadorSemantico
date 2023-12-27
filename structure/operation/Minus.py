from structure.exceptions.NodeException import NodeException
from structure.value.Operation import Operation

class Minus(Operation):
  # Initialize the node
  def __init__(self):
    super(Minus, self).__init__()
    self.weight = 1
    self.symbol = '-'

  # Evaluate the node
  def evaluate(self):
    if self.left and self.right:
      return self.left.evaluate() - self.right.evaluate()
    else:
      raise NodeException('Node does not have enough children.')
