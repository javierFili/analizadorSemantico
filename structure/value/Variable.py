from structure.value.Value import Value
from structure.exceptions.EvalException import EvalException
from structure.tree.Node import Node


class Variable(Node):
  # Initialize the node
  def __init__(self, name=''):
    super(Variable, self).__init__()
    self.name = str(name)
    self.value = Value()

  # Simplify the node
  def simplify(self):
    return self

  # Evaluate the node
  def evaluate(self):
    try:
      return self.value.evaluate()
    except:
      raise EvalException('Cannot evaluate expressions that contain uninitialized variables.')

  # Set the value of the variable
  def set(self, value):
    if isinstance(value, Value):
      self.value = value
    else:
      self.value = Value(value)

  # Unset the value of the variable
  def unset(self):
    self.value = Value()

  # Compare two variables
  def __eq__(self, other):
    if type(other) == type(self):
      if self.name == other.name:
        if self.value == other.value:
          return True
        else:
          return False
      else:
        return False
    else:
      return False

  # The length of the value
  def __len__(self):
    return len(self.name)

  # Return a string representation of the value
  def __str__(self):
    try:
      self.value.evaluate()
      return '{' + self.name + '=' + str(self.value) + '}'
    except:
      return self.name
