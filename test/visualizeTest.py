import unittest

from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode
from src.visualize import Visualize


class VisualizeTest(unittest.TestCase):
    def test_newick_str(self):
        na = TreeNode(Profile("ACGTAA", "seqA"))
        nb = TreeNode(Profile("ACGTAG", "seqB"))
        nc = TreeNode(Profile("ACGTCC", "seqC"))
        nd = TreeNode(Profile("ACGTGG", "seqD"))
        ne = TreeNode(Profile("ACGTTT", "seqE"))

        sub1 = TreeNode.mergeNodes([na, nc, ne])
        sub2 = TreeNode.mergeNodes([nb, sub1, nc])

        vis = Visualize(sub2)
        self.assertEqual(vis.newick_str, "(seqB:0.23,(seqA:0.22,seqC:0.22,seqE:0.22):0.23,seqC:0.20);")

    def test_tree_vis(self):
        na = TreeNode(Profile("ACGTAA", "seqA"))
        nb = TreeNode(Profile("ACGTAG", "seqB"))
        nc = TreeNode(Profile("ACGTCC", "seqC"))
        nd = TreeNode(Profile("ACGTGG", "seqD"))
        ne = TreeNode(Profile("ACGTTT", "seqE"))

        sub1 = TreeNode.mergeNodes([na, nc, ne])
        sub2 = TreeNode.mergeNodes([nb, sub1, nc])

        vis = Visualize(sub2)
        vis.load_newick_tree()
        vis.visualize("../data/outputtree.png", False)

    def test_tree_save(self):
        na = TreeNode(Profile("ACGTAA", "seqA"))
        nb = TreeNode(Profile("ACGTAG", "seqB"))
        nc = TreeNode(Profile("ACGTCC", "seqC"))
        nd = TreeNode(Profile("ACGTGG", "seqD"))
        ne = TreeNode(Profile("ACGTTT", "seqE"))

        sub1 = TreeNode.mergeNodes([na, nc, ne])
        sub2 = TreeNode.mergeNodes([nb, sub1, nc])

        vis = Visualize(sub2)
        vis.save_tree("../data/testoutput.nwk")
