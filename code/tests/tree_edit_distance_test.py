#coing=utf8
import unittest
from utils.tree_edit_distance import *

class TreeEditDistanceTest(unittest.TestCase):
    def setUp(self):
        # the serial should not matter
        self.A = Node("6", "f", "2",
                 Node("4","d", "2",
                      Node("1", "a", "2"),
                      Node("3", "c", "2",
                           Node("2", "b", "2"))),
                 Node("5", "e", "2"))
        print "A", self.A
        
        self.B = Node("6", "f", "1",
                  Node("4", "c", "1",
                       Node("3","d", "1",
                            Node("1", "a", "1"),
                            Node("2", "b", "1"))),
                  Node("5", "e", "1"))
        print "B", self.B

    def test_postorder(self):
        posta = postorder(self.A)
        postb = postorder(self.B)
        labelsa = [n.label for n in posta]
        labelsb = [n.label for n in postb]
        self.failUnlessEqual(["a", "b", "c", "d", "e", "f"], labelsa)
        self.failUnlessEqual(["a", "b", "d", "c", "e", "f"], labelsb)

    def test_leftmost_leaf_descendant_indices(self):
        post = postorder(self.A)
        lld_indices = leftmost_leaf_descendant_indices(post)
        self.failUnlessEqual(lld_indices, [0, 1, 1, 0, 4, 0])

        post = postorder(self.B)
        lld_indices = leftmost_leaf_descendant_indices(post)
        self.failUnlessEqual(lld_indices, [0, 1, 0, 0, 4, 0])

    def test_key_root_indices(self):
        post = postorder(self.A)
        lld_indices = leftmost_leaf_descendant_indices(post)
        kri = key_root_indices(lld_indices)
        self.failUnlessEqual(kri, [2, 4, 5])

        post = postorder(self.B)
        lld_indices = leftmost_leaf_descendant_indices(post)
        kri = key_root_indices(lld_indices)
        self.failUnlessEqual(kri, [1, 4, 5])

    def test_distance(self):
        def cost(n1,n2):
            if n1 is None or n2 is None:
                return 1
            if n1.label == n2.label:
                return 0
            return 1

        self.failUnlessEqual(distance(self.A, self.B, costs=cost), 2)
