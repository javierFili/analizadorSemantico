class Node(object):
  # Initialize the node
  def __init__(self):
    pass

  # Set a variable
  def setVariable(self, name, value):
    return None

  # Evaluate the node
  def evaluate(self):
    return None

  # Return a nice-looking string representing the node
  def toInfixNotation(self):
    return self.__str__()

  # Return a Polish notation string of the node
  def toPolishNotation(self):
    return self.__str__()

  # Return a Reverse Polish notation string of the node
  def toReversePolishNotation(self):
    return self.__str__()

  # Make a string representation of the node
  def __str__(self):
    return 'Empty Node (' + type(self).__name__ + ')'