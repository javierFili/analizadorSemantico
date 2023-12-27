from structure.value.Value import Value
from structure.value.Variable import Variable
from structure.exceptions.EvalException import EvalException
from structure.exceptions.NodeException import NodeException
from importlib import import_module
from structure.tree.Node import Node


class Operation(Node):
  # Initialize the operation
  def __init__(self):
    super(Operation, self).__init__()
    self.left = None  # Initialize left child to none
    self.right = None  # Initialize right child to none
    self.parent = None  # Initialize parent to none
    self.weight = 0  # Default weight is 0
    self.symbol = '?'  # Default operator symbol is ?
    self.arity = 2  # Default to binary operator

  # Add a child to the node
  def addChild(self, child):
    if self.left is None:
      self.left = child
      child.parent = self
    elif self.right is None:
      self.right = child
      child.parent = self
    else:
      raise NodeException('Node already has two children.')

  # Remove a child from the node
  def removeChild(self):
    if self.right is not None:
      node = self.right
      self.right = None
      node.parent = None
    elif self.left is not None:
      node = self.left
      self.left = None
      node.parent = None
    else:
      raise NodeException('Node has no children to remove.')
    return node

  # Find somewhere in this tree to add a child node. Return false if there are no open spots
  def addWhereOpen(self, child):
    # Can we have another child?
    if self.right is None:
      self.addChild(child)
      return True
    else:
      # Try to add the new child to one of our child nodes
      if isinstance(self.left, Operation) and isinstance(self.right, Operation):
        # Try the left node first
        success = self.left.addWhereOpen(child)
        # Only try the right node if the left node failed
        if not success:
          success = self.right.addWhereOpen(child)
        return success
      # Can we insert into the left node?
      elif isinstance(self.left, Operation):
        return self.left.addWhereOpen(child)
      # What about the right node?
      elif isinstance(self.right, Operation):
        return self.right.addWhereOpen(child)
      # There was nowhere to insert another node
      else:
        return False

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
      # Create a new parent node with the type of the original child
      if child_type == 'Times':
        times_module = import_module("structure.operation.Times")
        Times = times_module.Times
        new_parent = Times
      elif child_type == 'Divide':
        # This operation requires the common factor to be on the same side in both children
        if llgc == rlgc or lrgc == rrgc:
          divide_module = import_module("structure.operation.Divide")
          Divide = divide_module.Divide
          new_parent = Divide
        else:
          return self
      elif child_type == 'Exponent':
        # This operation requires the common factor to be on the same side in both children
        if llgc == rlgc or lrgc == rrgc:
          exponent_module = import_module("structura.operation.Exponent")
          Exponent = exponent_module.Exponent
          new_parent = Exponent()
        else:
          return self
      else:
        return self
      # Create a new child node with the type of the original parent
      if parent_type == 'Plus':
        plus_module = import_module("structure.operation.Plus")
        Plus = plus_module.Plus
        new_child = Plus
      elif parent_type == 'Minus':
        minus_module = import_module("structure.operation.Minus")
        Minus = minus_module.Minus
        new_child = Minus
      elif parent_type == 'Times':
        times_module = import_module("structure.operation.Times")
        Times = times_module.Times
        new_child = Times
      elif parent_type == 'Divide':
        divide_module = import_module("structure.operation.Divide")
        Divide = divide_module.Divide
        new_child = Divide
      else:
        return self
      # Add the differing factors as children
      new_child.addChild(different_left)
      new_child.addChild(different_right)
      # Add the common factor as a child of the times node
      if common_factor_on_left:
        new_parent.addChild(common_factor)
        new_parent.addChild(new_child)
      else:
        new_parent.addChild(new_child)
        new_parent.addChild(common_factor)
      # Return the re-factored node
      return new_parent
    else:
      return self

  # Simplify the node
  def simplify(self):
    simplified = True
    try:
      lvalue = self.left.simplify()
      self.left = lvalue
    except EvalException:
      simplified = False

    try:
      rvalue = self.right.simplify()
      self.right = rvalue
    except EvalException:
      simplified = False

    if simplified:
      return Value(self.evaluate())
    else:
      return self

  # Check whether the node contains a certain variable
  def containsVariable(self, varname):
    # Is the variable in the left child?
    if isinstance(self.left, Variable) and self.left.name == varname:
      return True
    elif not isinstance(self.left, Value):
      return self.left.containsVariable(varname)
    # Is the variable in the right child?
    if isinstance(self.right, Variable) and self.right.name == varname:
      return True
    elif not isinstance(self.right, Value):
      return self.right.containsVariable(varname)
    # Didn't find the variable
    return False

  # Set the value of a variable in this node
  def setVariable(self, name, value):
    # See if the variable exists in the left and/or right subtrees
    # Left side
    if isinstance(self.left, Variable) and self.left.name == name:
      self.left.set(value)
    else:
      self.left.setVariable(name, value)
    # Right side
    if isinstance(self.right, Variable) and self.right.name == name:
      self.right.set(value)
    else:
      self.right.setVariable(name, value)

  # Return the value of this node
  def evaluate(self):
    return None

  # Return an Infix Notation string representing the operation
  def toInfixNotation(self):
    # Unary operators
    if self.arity == 1:
      lstring = self.left.toInfixNotation()
      if isinstance(self.left, Operation) and self.weight > self.left.weight:
        string = '(' + lstring + ')'
      else:
        string = lstring
      string += self.symbol
    # Binary operators
    elif self.arity == 2:
      lstring = self.left.toInfixNotation()
      rstring = self.right.toInfixNotation()
      string = ''
      if isinstance(self.left, Operation) and self.weight > self.left.weight:
        string += '(' + lstring + ')'
      else:
        string += lstring

      string += ' ' + self.symbol + ' '
      if isinstance(self.right, Operation) and self.weight > self.right.weight:
        string += '(' + rstring + ')'
      else:
        string += rstring
    else:
      raise ValueError('Operators with arity other than 1 or 2 cannot be converted to infix notation')

    return string

  # Return a Polish Notation string of the operation
  def toPolishNotation(self):
    if self.arity == 1:
      lstring = self.left.toPolishNotation()
      string = self.symbol + ' '
      if isinstance(self.left, Operation) and self.weight > self.left.weight:
        string += '(' + lstring + ')'
      else:
        # Pull off the operator if the left child has the same type
        if isinstance(self, type(self.left)):
          string += lstring[2:]
        else:
          string += lstring
    else:
      lstring = self.left.toPolishNotation()
      rstring = self.right.toPolishNotation()
      string = self.symbol + ' '
      if isinstance(self.left, Operation) and self.weight > self.left.weight:
        string += '(' + lstring + ')'
      else:
        # Pull off the operator if the left child has the same type
        if isinstance(self, type(self.left)):
          string += lstring[2:]
        else:
          string += lstring
      string += ' '
      if isinstance(self.right, Operation) and self.weight > self.right.weight:
        string += '(' + rstring + ')'
      else:
        # Pull off the operator if the right child has the same type
        if isinstance(self, type(self.right)):
          string += rstring[2:]
        else:
          string += rstring

    return string

  # Return a Reverse Polish Notation string of the operation
  def toReversePolishNotation(self):
    if self.arity == 1:
      lstring = self.left.toReversePolishNotation()
      if isinstance(self.left, Operation) and self.weight > self.left.weight:
        string = '(' + lstring + ')'
      else:
        # Pull off the operator if the left child has the same type
        if type(self) == type(self.left):
          string = lstring[:-2]
        else:
          string = lstring
      string += ' ' + self.symbol
    else:
      lstring = self.left.toReversePolishNotation()
      rstring = self.right.toReversePolishNotation()
      string = ''
      if isinstance(self.left, Operation) and self.weight > self.left.weight:
        string += '(' + lstring + ')'
      else:
        # Pull off the operator if the left child has the same type
        if type(self) == type(self.left):
          string += lstring[:-2]
        else:
          string += lstring
      string += ' '
      if isinstance(self.right, Operation) and self.weight > self.right.weight:
        string += '(' + rstring + ')'
      else:
        # Pull off the operator if the right child has the same type
        if type(self) == type(self.right):
          string += rstring[:-2]
        else:
          string += rstring

      string += ' ' + self.symbol

    return string

  # See if two operation nodes are equal
  def __eq__(self, other):
    if type(other) == type(self):
      return (self.left == other.left) and (self.right == other.right)
    return False

  # Return the length of the node
  def __len__(self):
    left_len = 0
    right_len = 0
    # Get the lengths of the non-None children
    if self.left is not None:
      left_len = len(self.left)
    if self.right is not None:
      right_len = len(self.right)
    # Return the sum of the lengths
    return left_len + right_len

  # Return a string representation of the node
  def __str__(self):
    # Unary operators
    if self.arity == 1:
      return '[ ' + self.left.__str__() + ' ' + self.symbol + ' ]'
    # Binary operatorys
    else:
      return '[ ' + self.left.__str__() + ' ' + self.symbol + ' ' + self.right.__str__() + ' ]'
