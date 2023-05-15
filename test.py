# class TreeNode:
# 	def __init__(self, value):
# 		self.value = value
# 		self.left = None
# 		self.right = None
#
#
# tree = TreeNode(1)
# tree.left = TreeNode(2)
# tree.right = TreeNode(3)
# tree.left.left = TreeNode(4)
# tree.left.right = TreeNode(5)
#
# def pre_order(node):
# 	if node:
# 		print(node.value)
# 		pre_order(node.left)
# 		pre_order(node.right)
#
# def post_order(node):
# 	if node:
# 		post_order(node.left)
# 		post_order(node.right)
# 		print(node.value)
#
#
# def in_order(node):
# 	if node:
# 		in_order(node.left)
# 		print(node.value)
# 		in_order(node.right)
#
# in_order(tree)

# class Solution(object):
# 	def jew(self, jewels, stones):
# 		count = 0
# 		for j in jewels:
# 			count += stones.count(j)
# 		return count
#
#
# jewels = "aA"
# stones = "aAAbbbb"


class BinaryTree():
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None

tree = BinaryTree(1)
tree.left = BinaryTree(2)
tree.right = BinaryTree(3)
tree.left.left = BinaryTree(4)
tree.left.right = BinaryTree(5)
tree.left.left.left = BinaryTree(6)
tree.left.right.right = BinaryTree(7)

def pre_order(node):
	if node:
		pre_order(node.left)
		pre_order(node.right)
		print(node.value)

pre_order(tree)