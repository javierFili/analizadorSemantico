from structure.tree.Tree import Tree

if __name__ == '__main__':
  tree = Tree()
  tree.parse('8*2+8/7+3-2')
  tree.viewTreeUI()
