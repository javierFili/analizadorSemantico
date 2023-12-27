from structure.value.Value import Value
from structure.exceptions.TokenizeException import TokenizeException
from structure.operation.Factorial import Factorial, getOperation
import re


class Tokenizer(object):
  # Some static constants
  OPENPAREN = '('
  CLOSEPAREN = ')'

  # Initialize the tokenizer and tokenize the string
  def __init__(self, string):
    self.tokens = []
    # First, strip out whitespace from the string
    string = string.replace(' ', '')
    # Next replace adjacent parentheses with explicit multiplications so we can parse more easily
    string = string.replace(')(', ')*(')
    # Check for unmatches parentheses
    level = 0
    for char in string:
      if char == '(':
        level += 1
      elif char == ')':
        level -= 1
    if level != 0:
      raise TokenizeException('Unmatched parenthesis.')
    # Make variable multiplications written as adjacent characters (e.g. 3x, xy) explicit
    p = re.compile('(\d+)(\w)')
    string = p.sub(r'\1*\2', string)
    p = re.compile('(\w)(\d+)')
    string = p.sub(r'\1*\2', string)
    p = re.compile('(\w)(?=\w)')
    string = p.sub(r'\1*', string)
    # Multiplication of parenthetical expression can also be written implicitly as 'x(...)' or '(...)x'
    # Make these explicit here
    p = re.compile('([\w\d]+)\(')
    string = p.sub(r'\1*(', string)
    p = re.compile('\)([\w\d]+)')
    string = p.sub(r')*\1', string)
    # The characters that we recognize
    numbers = '01234567890.'
    operators = '+-*/^!'
    # Iterate over the string and create tokens of the appropriate type
    curr_value = Value()
    for i in range(0, len(string)):
      char = string[i]
      if char == Tokenizer.OPENPAREN:
        self.pushToken(char)
      elif char == Tokenizer.CLOSEPAREN:
        if len(curr_value) > 0:
          self.pushToken(curr_value)
          curr_value = Value()
        self.pushToken(char)
      elif char in numbers or (
        char == '-' and string[i + 1] in numbers and len(curr_value) == 0 and string[i - 1] != Tokenizer.CLOSEPAREN):
        curr_value.append(char)
        # Last value in the string
        if i == len(string) - 1:
          self.pushToken(curr_value)
      elif char in operators:
        if len(curr_value) > 0:
          self.pushToken(curr_value)
          curr_value = Value()
        self.pushToken(getOperation(char))
      else:
        if len(curr_value) > 0:
          self.pushToken(curr_value)
          curr_value = Value()
        from structure.value.Variable import Variable
        self.pushToken(Variable(char))

  # Return the next token in the list (at the beginning)
  def getToken(self):
    if len(self.tokens) > 0:
      return self.tokens.pop(0)
    else:
      return None

  # Return the next token in the list without removing it
  def peekToken(self):
    if len(self.tokens) > 0:
      return self.tokens[0]
    else:
      return None

  # Add a token to the end of the list
  def pushToken(self, token):
    self.tokens.append(token)

# A class representing an expression tree. Contains logic for parsing strings.
# TODO: This class is probably not that different from the Node class, so they
# 	    should probably be merged or this class should at least be simplified.