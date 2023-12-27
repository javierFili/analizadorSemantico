import copy
from structure.tree.Tokenizer import Tokenizer
from structure.value.Operation import Operation
from structure.value.Value import Value
from structure.value.Variable import Variable
from structure.exceptions.EvalException import EvalException
from structure.tree.Node import Node


class Tree(Node):
  # Initialize the tree
  def __init__(self):
    super(Tree, self).__init__()
    self.root = None

  def viewTree(self, tree, screen_width, screen_height, data_tree, node_width, node_height, position):
    x = screen_width + position * screen_width
    y = screen_height + position * screen_height
    x_base = screen_width
    y_base = screen_height
    if hasattr(tree, 'value'):
      print(tree.value)
      data_tree.append(((x, y), tree.value, (x_base, y_base)))
    elif tree:
      self.viewTree(tree.left, x - screen_width / 2, y - screen_height, data_tree, node_width, node_height,
                    2 * position)

      if hasattr(tree, 'symbol'):
        print(tree.symbol)
        data_tree.append(((x, y), tree.symbol, (x_base, y_base)))

      self.viewTree(tree.right, x + screen_width / 2, y - screen_height, data_tree, node_width, node_height,
                    2 * position + 1)

  # view_tree(tree, data_tree,300,600,300,600,4)
  def view_tree(self, tree, data_tree, x, y, x_base, y_base, nivel):
    if hasattr(tree, 'value'):
      print(tree.value)
      data_tree.append(((x, y), tree.value, (x_base, y_base)))
    elif tree:
      self.view_tree(tree.left, data_tree, x - (nivel) * 40, y - 60, x, y, nivel - 1)
      if hasattr(tree, 'symbol'):
        data_tree.append(((x, y), tree.symbol, (x_base, y_base)))
        print(tree.symbol)
      self.view_tree(tree.right, data_tree, x + (nivel) * 40, y - 60, x, y, nivel - 1)

  def viewTreeUI(self):
    screen_width = 800
    screen_height = 600
    nivel = self.get_size()
    node_width = screen_width / 32  # 32 nodes on level botton
    node_height = screen_height / nivel
    data_tree = []
    # self.viewTree(self.root, screen_width / 2, screen_height, data_tree, node_width, node_height, nivel)
    self.view_tree(self.root, data_tree, 600, 600, 600, 600, nivel)
    return data_tree

  def get_size(self):
    size = 0
    return self.get_size_tree(self.root, size)

  def get_size_tree(self, tree, size):
    if tree is None or hasattr(tree, 'value'):
      return size
    size += 1
    return max(self.get_size_tree(tree.left, size), self.get_size_tree(tree.right, size))

  # Parse a string expression
  def parse(self, expression):
    # TODO: This function should be able to detect the type of notation and choose the correct parser
    self.parseInfixNotation(expression)

  # Parse a string expression written using Infix Notation
  def parseInfixNotation(self, expression):
    # Tokenize the expression
    tokenizer = Tokenizer(expression)
    # Iterate over the tokens
    tokenIndex = 0
    token = 0
    curr_value = None
    subtree_root = Operation()
    prev_op = None
    curr_op = None
    self.root = Operation()
    paren_stack = []
    while token is not None:
      tokenIndex += 1
      token = tokenizer.getToken()
      # No tokens left
      if token is None:
        # If there are no operations, the current value must be the entire tree
        if len(subtree_root) == 0:
          subtree_root = curr_value
        elif curr_value is not None and len(subtree_root) < 2:
          subtree_root.addChild(curr_value)
        break
      # Parse the token
      if token == Tokenizer.OPENPAREN:
        paren_stack.append(copy.deepcopy(subtree_root))
        subtree_root = Operation()
        prev_op = Operation()
        curr_op = Operation()
      elif token == Tokenizer.CLOSEPAREN:
        paren_op = paren_stack.pop()
        # Insert the parenthetical expression in the tree
        if len(paren_op) < 2:
          paren_op.addChild(subtree_root)
        else:
          paren_op.addWhereOpen(subtree_root)
        # Re-root the tree and continue parsing
        subtree_root = paren_op
        prev_op = subtree_root
      elif isinstance(token, Variable) or isinstance(token, Value):
        if curr_value is None:
          curr_value = token
          if (tokenizer.peekToken() is None or tokenizer.peekToken() == Tokenizer.CLOSEPAREN) and prev_op is not None:
            prev_op.addChild(curr_value)
            curr_value = None
        # else:
        #	raise ParseException("Too many values at token " + str(tokenIndex))
      elif isinstance(token, Operation):
        if curr_value == None and subtree_root.symbol == '?':
          token.addChild(subtree_root.left)
          subtree_root = token
          prev_op = token
        elif prev_op is not None and len(prev_op) > 0:
          if curr_value != None:
            prev_op.addChild(curr_value)
            curr_value = None
          curr_op = token
          # Determine parent-child relationship based on operation weights
          # If the next node is heavier than the current one (e.g. * v. +), add it as a child of the current node and make the current node the root of the tree
          if curr_op.weight > prev_op.weight:
            c = prev_op.removeChild()
            prev_op.addChild(curr_op)
            curr_op.addChild(c)
            subtree_root = prev_op
          # If the current and next nodes have the same weight, add the next node as a child of the current one -- note that this is the same as what we do when the next node is heavier BUT we do NOT re-root the tree
          elif curr_op.weight == prev_op.weight:
            c = prev_op.removeChild()
            prev_op.addChild(curr_op)
            curr_op.addChild(c)
          # If the next node is lighter than the current one, add the current node as a child of the next one and make the next one the root of the tree
          else:
            curr_op.addChild(subtree_root)
            subtree_root = curr_op
          prev_op = curr_op
        else:
          prev_op = token
          prev_op.addChild(curr_value)
          subtree_root = prev_op
          curr_value = None
    # An undefined operation with only one child can be simplified. Let's.
    if isinstance(subtree_root, Operation) and subtree_root.symbol == '?' and subtree_root.right == None:
      self.root = subtree_root.left
    else:
      self.root = subtree_root

  # Set the value of a variable in the tree
  def setVariable(self, name, value):
    if isinstance(self.root, Operation):
      self.root.setVariable(name, value)
    elif isinstance(self.root, Variable) and self.root.name == name:
      self.root.set(value)

  # Try to simplify the tree
  def simplify(self):
    try:
      self.root.simplify()
    except EvalException:
      return False
    # Try to evaluate the simplified root node
    try:
      self.root = self.root.evaluate()
      return True
    except EvalException:
      return False

  # Evaluate the entire tree
  def evaluate(self):
    return self.root.evaluate()

  # Print the tree using Infix Notation
  def toInfixNotation(self):
    return self.root.toInfixNotation()

  # Print the tree using Polish Notation
  def toPolishNotation(self):
    return self.root.toPolishNotation()

  # Print the tree using Reverse Polish Notation
  def toReversePolishNotation(self):
    return self.root.toReversePolishNotation()

  # Make a string representation of the tree
  def __str__(self):
    return self.root.__str__()

  # Get the length of the tree
  def __len__(self):
    return len(self.root)

  # Check if two trees are equal
  def __eq__(self, other):
    if isinstance(other, Tree):
      return self.root == other.root
    return False
