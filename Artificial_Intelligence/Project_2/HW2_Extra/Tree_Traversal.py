#Our Tree structure
class Node:
 	def __init__(self,value):
 		self.left=None
 		self.data=value
 		self.right=None
class Tree:
 	def __init__(self,root):
 		self.root=Node(root)

tree=Tree("START NODE")
tree.root.left=Node("ΚΑΤΑΣΤΑΣΗ Ε")
tree.root.right=Node("ΡΙΞΗ ΖΑΡΙΟΥ")
tree.root.right.right=Node(6)
tree.root.right.right=Node(5)
tree.root.right.right=Node(4)
tree.root.right.right=Node(3)
tree.root.right.right=Node(2)
tree.root.right.right=Node(1)

def inorder(root,visited):
    if root:
        visited = inorder(root.left,visited)
        visited.append(root.data)
        visited = inorder(root.right,visited)
    return visited
     
print(f'Inorder \n',inorder(tree.root,[]))