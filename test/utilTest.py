import unittest
from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode


class utilTest(unittest.TestCase):
    def test_update_variance1(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        self.assertEqual(1 / 6, updateVariance(na, nb), "Update Variance wrong.")

    def test_profile_distance(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        root = TreeNode.mergeNodes([na,nb])
        (weight_i, dist_i), incorr_weight_i = na.profile.distance(root.profile)
        self.assertEqual(1 / 12, dist_i)

    def test_update_weight(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        root = TreeNode.mergeNodes([na,nb])
        self.assertEqual(1 / 2, updateWeight(root, na, nb, 2), "Update weight wrong.")

    def test_internal_nodes_distance(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        self.assertEqual(1 / 6, internalNodesDistance(na, nb),
                         "Update internal nodes distance wrong.")

    def test_set_joins_criterion(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        root = TreeNode.mergeNodes([na,nb])

        nc = TreeNode(Profile("ACGTTT", "seqC"))
        self.assertEqual(1 / 3, setJoinsCriterion(root, root, nc, 2),
                         "Set joins criterion wrong.")
