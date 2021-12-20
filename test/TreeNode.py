import profile
import unittest
import numpy.testing as npt
from src.profile import Profile
from src.TreeNode import TreeNode


class TreeTest(unittest.TestCase):
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

        nMerge = TreeNode.mergeNodes([na,nc])

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

        nMerge = TreeNode.mergeNodes([na,nc])

        print(nMerge.profile.get_frequency_profile())
        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0.5, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 0.5, 0, 0]
        }, nMerge.profile.get_frequency_profile())

    def test_mergeDistances1(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGCAA")

        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        da = [
            {'distance': 1, 'Node': None},
            {'distance': 2, 'Node': None},
            {'distance': 3, 'Node': None},
            {'distance': 4, 'Node': None},
            {'distance': 5, 'Node': None}
        ]

        db = [
            {'distance': 6, 'Node': None},
            {'distance': 7, 'Node': None},
            {'distance': 8, 'Node': None},
            {'distance': 9, 'Node': None},
            {'distance': 10, 'Node': None}
        ]

        na.distances = da
        nb.distances = db

        dCorrect = [
            {'distance': 1, 'Node': None},
            {'distance': 2, 'Node': None},
            {'distance': 3, 'Node': None},
            {'distance': 4, 'Node': None},
            {'distance': 5, 'Node': None}
        ]

        nMerge = TreeNode.mergeNodes([na,nb])

        npt.assert_array_equal(nMerge.distances,dCorrect)

    def test_mergeDistances2(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGCAA")

        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        da = [
            {'distance': 1, 'Node': None},
            {'distance': 6, 'Node': None},
            {'distance': 3, 'Node': None},
            {'distance': 8, 'Node': None},
            {'distance': 5, 'Node': None}
        ]

        db = [
            {'distance': 2, 'Node': None},
            {'distance': 9, 'Node': None},
            {'distance': 4, 'Node': None},
            {'distance': 10, 'Node': None},
            {'distance': 6, 'Node': None}
        ]

        na.distances = da
        nb.distances = db

        dCorrect = [
            {'distance': 1, 'Node': None},
            {'distance': 2, 'Node': None},
            {'distance': 3, 'Node': None},
            {'distance': 4, 'Node': None},
            {'distance': 5, 'Node': None}
        ]

        nMerge = TreeNode.mergeNodes([na,nb])

        npt.assert_array_equal(nMerge.distances,dCorrect)

    def test_mergeDistances3(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGCAA")

        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        da = [
            {'distance': 3, 'Node': None},
            {'distance': 68, 'Node': None},
            {'distance': 24, 'Node': None},
            {'distance': 98, 'Node': None},
            {'distance': 68, 'Node': None}
        ]

        db = [
            {'distance': 37, 'Node': None},
            {'distance': 53, 'Node': None},
            {'distance': 42, 'Node': None},
            {'distance': 10, 'Node': None},
            {'distance': 6, 'Node': None}
        ]

        na.distances = da
        nb.distances = db

        dCorrect = [
            {'distance': 3, 'Node': None},
            {'distance': 6, 'Node': None},
            {'distance': 10, 'Node': None},
            {'distance': 24, 'Node': None},
            {'distance': 37, 'Node': None}
        ]

        nMerge = TreeNode.mergeNodes([na,nb])

        npt.assert_array_equal(nMerge.distances, dCorrect)

#TODO add test for mergers between more than 2 nodes