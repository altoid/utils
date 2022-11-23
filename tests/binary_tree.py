#!/usr/bin/env python

import unittest
from utils import binary_tree


def traverse(n):
    if not n:
        return

    traverse(n.left)
    print(n.val)
    traverse(n.right)

class MyTest(unittest.TestCase):
    def test_1(self):
        arr = [5, 3, 6, 2, 4, None, None, 1]
        root = binary_tree.make_tree(arr)
        traverse(root)
