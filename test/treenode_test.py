import unittest

import numpy.testing as npt
from src.profile import Profile
from src.TreeNode import TreeNode


class TreeTest(unittest.TestCase):
    def test_calculate_simple_motif(self):
        profile = Profile("A", "seqA")
        treeNode = TreeNode(profile)
        self.assertDictEqual({
            "A": [1],
            "C": [0],
            "G": [0],
            "T": [0]
        }, treeNode.profile.get_frequency_profile())

    def test_simpleMerge(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGTAA", "seqB")


        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

        nMerge = TreeNode.mergeNodes([na,nb], root)

        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 1, 0, 0]
        }, nMerge.profile.get_frequency_profile())

    def test_simpleMerge2(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGCAA", "seqB")


        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

        nMerge = TreeNode.mergeNodes([na,nb], root)

        print(nMerge.profile.get_frequency_profile())
        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0.5, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 0.5, 0, 0]
        }, nMerge.profile.get_frequency_profile())

    def test_mergeDistances1(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGCAA", "seqB")

        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

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

        nMerge = TreeNode.mergeNodes([na,nb], root)

        npt.assert_array_equal(nMerge.distances,dCorrect)

    def test_mergeDistances2(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGCAA", "seqB")

        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

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

        nMerge = TreeNode.mergeNodes([na,nb], root)

        npt.assert_array_equal(nMerge.distances,dCorrect)

    def test_mergeDistances3(self):
        root : TreeNode = TreeNode(Profile("A", "root"))

        profile_a = Profile("ACGTAA", "seqA")
        profile_b = Profile("ACGCAA", "seqB")

        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)

        na.parent = root
        nb.parent = root
        root.children.append(na)
        root.children.append(nb)

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

        nMerge = TreeNode.mergeNodes([na,nb], root)

        npt.assert_array_equal(nMerge.distances, dCorrect)

