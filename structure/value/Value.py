from structure.tree.Node import Node


class Value(Node):
  # Initialize the node
  def __init__(self, val=''):
    super(Value, self).__init__()
    self.value = str(val)

  # Append a digit to the value
  def append(self, digit):
    self.value = self.value + str(digit)

  # Simplify the node
  def simplify(self):
    return self

  # Evaluate the node
  def evaluate(self):
    return float(self.value)

  # The length of the value
  def __len__(self):
    return len(self.value)

  # See if two values are equal
  def __eq__(self, other):
    if isinstance(other, Value):
      return self.value == other.value
    return False

  # Return a string representation of the value
  def __str__(self):
    return self.value

