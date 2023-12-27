from structure.exceptions.NodeException import NodeException
from structure.operation.Exponent import Exponent
from structure.operation.Minus import Minus
from structure.value.Operation import Operation


class Divide(Operation):
  # Initialize the node
  def __init__(self):
    super(Divide, self).__init__()
    self.weight = 2
    self.symbol = '/'

  # Evaluate the node
  def evaluate(self):
    if self.left and self.right:
      return self.left.evaluate() / self.right.evaluate()
    else:
      raise NodeException('Node does not have enough children.')

  # Try to factor the node
  def factor(self):
    # Factor the children first (if possibe)
    # Left child
    try:
      self.left = self.left.factor()
    except:
      pass
    # Right child
    try:
      self.right = self.right.factor()
    except:
      pass
    # Currently we only know how to factor sums of multiplications since both are commutative
    parent_type = type(self).__name__
    parent_weight = self.weight
    child_type = type(self.left).__name__
    # Make sure the children are both operations, both the same type, and have a greater weight
    if isinstance(self.left, Operation) and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
      if child_type != 'Exponent':
        return super(Divide, self).factor()
      else:
        # Get grandchildren
        llgc = self.left.left
        lrgc = self.left.right
        rlgc = self.right.left
        rrgc = self.right.right
        common_factor_on_left = False
        # Find the common factor (if any)
        if llgc == rlgc:
          common_factor = llgc
          common_factor_on_left = True
          different_left = lrgc
          different_right = rrgc
        elif llgc == rrgc:
          common_factor = llgc
          common_factor_on_left = True
          different_left = lrgc
          different_right = rlgc
        elif lrgc == rlgc:
          common_factor = lrgc
          different_left = llgc
          different_right = rrgc
        elif lrgc == rrgc:
          common_factor = lrgc
          different_left = llgc
          different_right = rlgc
        else:
          return self
        # If the common factor is on the right, normal factoring rules apply
        if not common_factor_on_left:
          return super(Divide, self).factor()
        # Create a new parent node with the type of the original child
        if child_type == 'Exponent':
          # This operation requires the common factor to be on the same side in both children
          if llgc == rlgc or lrgc == rrgc:
            new_parent = Exponent()
          else:
            return self
        else:
          return self
        # Since this is a multiplication, we need to convert to addition of the exponents
        new_child = Minus()
        # Add the differing factors as children
        new_child.addChild(different_left)
        new_child.addChild(different_right)
        # Add the common factor as a child of the times node
        new_parent.addChild(common_factor)
        new_parent.addChild(new_child)
        # Return the re-factored node
        return new_parent
    else:
      return self
