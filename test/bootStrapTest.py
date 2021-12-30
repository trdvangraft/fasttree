import unittest
from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode
from src.bootstrap import BootStrap


class bootStrapTest(unittest.TestCase):
    def test_resample_column(self):
        na = TreeNode(Profile("ACGTAA", "seqA"))
        nb = TreeNode(Profile("ACGTAG", "seqB"))
        nc = TreeNode(Profile("ACGTCC", "seqC"))
        nd = TreeNode(Profile("ACGTGG", "seqD"))
        ne = TreeNode(Profile("ACGTTT", "seqE"))

        sub1 = TreeNode.mergeNodes([na, nb])
        sub2 = TreeNode.mergeNodes([nc, sub1])
        root = TreeNode.mergeNodes([nd, sub2, ne])

        bootStrap = BootStrap(sub1)
        print(bootStrap.support_score)

