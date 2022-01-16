import unittest
from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode


class UtilTest(unittest.TestCase):
    def test_update_variance1(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        self.assertEqual(1 / 6, updateVariance(na, nb), "Update Variance wrong.")

    def test_profile_distance(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

        nab = TreeNode.mergeNodes([na, nb],root)
        (weight_i, dist_i), incorr_weight_i = na.profile.distance(nab.profile)
        self.assertEqual(-10/12, dist_i)

    def test_update_weight(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

        nab = TreeNode.mergeNodes([na,nb],root)
        self.assertEqual(1 / 2, updateWeight(nab, na, nb, 1), "Update weight wrong.")

    def test_internal_nodes_distance(self):
        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        self.assertEqual(1 / 6, internalNodesDistance(na, nb),
                         "Update internal nodes distance wrong.")

    def test_set_joins_criterion(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

        nab = TreeNode.mergeNodes([na,nb],root)
        self.assertEqual(1/6, setJoinsCriterion(nab, na, nb, 1),
                         "Set joins criterion wrong.")

    def test_set_out_distance(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAG", "seqB")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

        nab = TreeNode.mergeNodes([na,nb],root)
        self.assertEqual(-5/3, setOutDistance(nab, na, 3), "Set out distance wrong.")
        self.assertEqual(-5/3, setOutDistance(nab, nb, 3), "Set out distance wrong.")
