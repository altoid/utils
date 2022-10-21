from collections import deque
import pickle

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class DecoratedTreeNode:
    def __init__(self, x):
        self.val = x
        self.order = None
        self.left = None
        self.right = None


class Codec:

    def insert(self, root, node):
        if not root:
            return

        if node.order < root.order:
            if root.left:
                self.insert(root.left, node)
            else:
                root.left = node
            return

        if node.order > root.order:
            if root.right:
                self.insert(root.right, node)
            else:
                root.right = node
            return

    def clone_original(self, root):
        """
        root is a tree of TreeNodes.  create a clone of it with DecoratedTreeNodes.
        """
        if root is None:
            return None

        newnode = DecoratedTreeNode(root.val)
        newnode.left = self.clone_original(root.left)
        newnode.right = self.clone_original(root.right)

        return newnode

    def clone_decorated(self, root):
        """
        root is a tree of DecoratedTreeNodes.  create a clone of it with TreeNodes.
        """
        if root is None:
            return None

        newnode = TreeNode(root.val)
        newnode.left = self.clone_decorated(root.left)
        newnode.right = self.clone_decorated(root.right)

        return newnode

    def decorate(self, root, initial):
        """
        do an inorder walk of the tree and set the value of <order> in each of the nodes.
        this will make the tree a BST if you use order as the key.
        """
        if not root:
            return initial

        counter = self.decorate(root.left, initial)
        root.order = counter
        counter = self.decorate(root.right, counter + 1)

        return counter

    def serialize(self, root):
        """
        1. clone the tree at <root> but with DecoratedTreeNodes.
        2. do an inorder walk of the tree and set the value of <order> in each of the nodes.
           this will make the tree a BST if you use order as the key.
        3. do a breadth-first traversal of the tree and create an array of (value, order) tuples,
           one for each node.
        4. serialize this array using pickle and return the byte string.
        """

        dtree = self.clone_original(root)
        self.decorate(dtree, 1)

        d = deque()
        serialization = []
        if dtree:
            d.append(dtree)
        while len(d) > 0:
            n = d.popleft()
            serialization.append((n.val, n.order))
            if n.left:
                d.append(n.left)
            if n.right:
                d.append(n.right)

        pkl = pickle.dumps(serialization)

        return pkl

    def deserialize(self, pkl):
        """Decodes your encoded data to tree.
        """

        serialization = pickle.loads(pkl)
        if not serialization:
            return None

        toop = serialization[0]
        root = DecoratedTreeNode(toop[0])
        root.order = toop[1]
        for d in serialization[1:]:
            node = DecoratedTreeNode(d[0])
            node.order = d[1]
            self.insert(root, node)

        new_root = self.clone_decorated(root)

        return new_root
