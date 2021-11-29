import profile
import unittest

from src.profile import Profile
from src.TreeNode import TreeNode


class ProfileTest(unittest.TestCase):
    def test_calculate_simple_motif(self):
        profile = Profile("A")
        treeNode = TreeNode(profile)
        self.assertDictEqual({
            "A": [1],
            "C": [0],
            "G": [0],
            "T": [0]
        }, treeNode.profile.get_frequency_profile())

    def test_simpleMerge(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAA")


        na = TreeNode(profile_a)
        nc = TreeNode(profile_b)

        nMerge = na.mergeNodes(nc)

        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 1, 0, 0]
        }, nMerge.profile.get_frequency_profile())

    def test_simpleMerge2(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGCAA")


        na = TreeNode(profile_a)
        nc = TreeNode(profile_b)

        nMerge = na.mergeNodes(nc)

        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0.5, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 0.5, 0, 0]
        }, nMerge.profile.get_frequency_profile())