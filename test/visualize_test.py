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

        root : TreeNode = TreeNode(Profile("A", "root"))
        na.parent = root
        nc.parent = root
        nb.parent = root

        root.children.append(na)
        root.children.append(nc)
        root.children.append(nb)

        root.generateProfileFromChildren()
        root.upDistance = root.setSelfUpDistanceFromChild()
        root.selfDistance = root.setSelfDistance()

        sub1 = TreeNode.mergeNodes([na, nc], root)
        sub2 = TreeNode.mergeNodes([nb, sub1], root)

        vis = Visualize(root)
        print(vis.newick_str)
        # self.assertEqual(vis.newick_str, "(seqB:0.23,(seqA:0.22,seqC:0.22,seqE:0.22):0.23,seqC:0.20);")

    def test_tree_vis(self):
        na = TreeNode(Profile("ACGTAA", "seqA"))
        nb = TreeNode(Profile("ACGTAG", "seqB"))
        nc = TreeNode(Profile("ACGTCC", "seqC"))
        nd = TreeNode(Profile("ACGTGG", "seqD"))
        ne = TreeNode(Profile("ACGTTT", "seqE"))
        root : TreeNode = TreeNode(Profile("A", "root"))
        na.parent = root
        nc.parent = root
        nb.parent = root

        root.children.append(na)
        root.children.append(nc)
        root.children.append(nb)

        
        root.generateProfileFromChildren()
        root.upDistance = root.setSelfUpDistanceFromChild()
        root.selfDistance = root.setSelfDistance()

        sub1 = TreeNode.mergeNodes([na, nc], root)
        sub2 = TreeNode.mergeNodes([nb, sub1], root)

        vis = Visualize(root)
        vis.load_newick_tree()
        vis.visualize("data/outputtree.png", False)

    def test_tree_save(self):
        na = TreeNode(Profile("ACGTAA", "seqA"))
        nb = TreeNode(Profile("ACGTAG", "seqB"))
        nc = TreeNode(Profile("ACGTCC", "seqC"))
        nd = TreeNode(Profile("ACGTGG", "seqD"))
        ne = TreeNode(Profile("ACGTTT", "seqE"))

        root : TreeNode = TreeNode(Profile("A", "root"))
        na.parent = root
        nc.parent = root
        nb.parent = root

        root.children.append(na)
        root.children.append(nc)
        root.children.append(nb)

        root.generateProfileFromChildren()
        root.upDistance = root.setSelfUpDistanceFromChild()
        root.selfDistance = root.setSelfDistance()

        sub1 = TreeNode.mergeNodes([na, nc], root)
        sub2 = TreeNode.mergeNodes([nb, sub1], root)

        vis = Visualize(root)
        vis.save_tree("data/testoutput.nwk")
