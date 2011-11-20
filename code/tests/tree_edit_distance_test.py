#coing=utf8
import unittest
from utils.tree_edit_distance import *

class TreeEditDistanceTest(unittest.TestCase):
    def setUp(self):
        self.A = Node("6", "f",
                 Node("4","d",
                      Node("1", "a"),
                      Node("3", "c",
                           Node("2", "b"))),
                 Node("5", "e"))
        

        
        self.B = Node("6", "f",
                  Node("4", "c",
                       Node("3","d",
                            Node("1", "a"),
                            Node("2", "b"))),
                  Node("5", "e"))

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
        self.failUnlessEqual(distance(self.A, self.B), 2)
