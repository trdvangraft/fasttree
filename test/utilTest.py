# encoding: utf-8
"""
@author: Xinqi
@contact: lixinqi98@gmail.com
@file: utilTest.py
@time: 12/7/21
@desc:
"""

import unittest
from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode


class ProfileTest(unittest.TestCase):
    def test_update_variance1(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAG")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        self.assertEqual(1 / 6, updateVariance(na, nb), "Update Variance wrong.")

    def test_update_weight(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAG")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        root = TreeNode.mergeNodes([na,nb])
        self.assertEqual(1 / 2, updateWeight(root, na, nb, 1), "Update weight wrong.")

    def test_internal_nodes_distance(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAG")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        self.assertEqual(1 / 6, internalNodesDistance(na, nb),
                         "Update internal nodes distance wrong.")

    def test_set_joins_criterion(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAG")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        root = TreeNode.mergeNodes([na,nb])
        self.assertEqual(-1.5, setJoinsCriterion(root, na, nb, 1),
                         "Set joins criterion wrong.")

    def test_set_out_distance(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAG")
        na = TreeNode(profile_a)
        nb = TreeNode(profile_b)
        root = TreeNode.mergeNodes([na,nb])
        self.assertEqual(5 / 6, setOutDistance(root, na, 1), "Set out distance wrong.")
        self.assertEqual(5 / 6, setOutDistance(root, nb, 1), "Set out distance wrong.")
