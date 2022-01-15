import unittest

from typing import List, Optional, Tuple
from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode
from src.nni import nni_interchange, nni_runner


class NniTest(unittest.TestCase):
    def test_original_tree_is_optimal(self):
        # Arrange
        [node_a, node_b, node_c, node_d], profiles, root = self.__node_factory(["CCC", "CCG", "AAT", "AAA"])

        node_a.addDistance(node_b, 0.0)
        node_b.addDistance(node_a, 0.0)

        node_c.addDistance(node_d, 0.0)
        node_d.addDistance(node_c, 0.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(node_b, root)
        TreeNode.mergeNodes(node_c, root)
        TreeNode.mergeNodes(node_d, root)

        # Act
        nni_interchange(root)
        
        # Assert
        self.assertEqual(len(root.children), 2)
        self.assertListEqual(self.__get_motifs(root.children[0]), profiles[0].combine(profiles[1]).motifs)
        self.assertListEqual(self.__get_motifs(root.children[1]), profiles[2].combine(profiles[3]).motifs)
    
    def test_non_optimal_tree_gets_corrected(self):
        # Arrange
        [node_a, node_b, node_c, node_d], profiles, root = self.__node_factory(["CCC", "AAT", "CCG", "AAA"])
        
        node_a.addDistance(node_b, 0.0)
        node_b.addDistance(node_a, 0.0)

        node_c.addDistance(node_d, 0.0)
        node_d.addDistance(node_c, 0.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(node_b, root)
        TreeNode.mergeNodes(node_c, root)
        TreeNode.mergeNodes(node_d, root)

        # Act
        nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(root.children[0]), profiles[0].combine(profiles[2]).motifs)
        self.assertListEqual(self.__get_motifs(root.children[1]), profiles[3].combine(profiles[1]).motifs)

    def test_optimal_tree_with_three_nodes(self):
        # Arrange
        [node_a, node_b, node_c], profiles, root = self.__node_factory(["CCC", "CCG", "AAA"])

        node_a.addDistance(node_b, 0.0)
        node_b.addDistance(node_a, 0.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(node_b, root)

        # Act
        nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(root.children[1]), profiles[0].combine(profiles[1]).motifs)
        self.assertListEqual(self.__get_motifs(root.children[0]), profiles[2].motifs)

    def test_non_optimal_tree_with_three_nodes(self):
        # Arrange
        [node_a, node_b, node_c], profiles, root = self.__node_factory(["CCC", "AAA", "CCG"])

        node_a.addDistance(node_b, 0.0)

        TreeNode.mergeNodes(node_a, root)

        # Act
        nni_interchange(root)

        # Assert
        self.assertCountEqual(self.__get_motifs(root.children[0]), profiles[0].combine(profiles[2]).motifs)
        self.assertCountEqual(self.__get_motifs(root.children[1]), profiles[1].motifs)

    def test_complex_non_optimal_tree_with_three_nodes(self):
        # Arrange
        [node_a, node_b, node_c], profiles, root = self.__node_factory(["CCGC", "CCAT", "CCCC"])

        node_a.addDistance(node_b, 0.0)
        node_b.addDistance(node_a, 0.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(node_b, root)

        # Act
        nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(root.children[0]), profiles[0].combine(profiles[2]).motifs)
        self.assertListEqual(self.__get_motifs(root.children[1]), profiles[1].motifs)

    def test_complex_optimal_multi_layer_tree(self):
        # Arrange
        dna = ["CCGC", "CCAT", "CCCC", "AAAA", "AAAT", "AATT"]
        [node_a, node_b, node_c, node_d, node_e, node_f], profiles, root = self.__node_factory(dna)

        node_e.addDistance(node_f, 0.0)
        node_e.addDistance(node_d, 2.0)
        node_e.addDistance(node_a, 10.0)

        node_a.addDistance(node_c, 0.0)
        node_a.addDistance(node_b, 2.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(root.children[-1], root)

        TreeNode.mergeNodes(node_e, root)
        TreeNode.mergeNodes(root.children[-1], root)

        # root.children[0].addDistance(root.children[1], 0.0)
        TreeNode.mergeNodes(root.children[1], root)

        # Act
        nni_runner(root)

        # Assert
        self.assertCountEqual(self.__get_motifs(root.getChild().children[0]), profiles[3].combine(profiles[5].combine(profiles[4])).motifs)
        self.assertCountEqual(self.__get_motifs(root.getChild().children[1]), profiles[1].combine(profiles[0].combine(profiles[2])).motifs)

    def test_complex_non_optimal_multi_layer_tree_local_switches(self):
        # Arrange
        dna = ["CCGC", "CCAT", "CCCC", "AAAA", "AAAT", "AATT"]
        [node_a, node_b, node_c, node_d, node_e, node_f], profiles, root = self.__node_factory(dna)

        node_e.addDistance(node_f, 0.0)
        node_e.addDistance(node_d, 2.0)
        node_e.addDistance(node_a, 10.0)

        node_a.addDistance(node_c, 0.0)
        node_a.addDistance(node_b, 2.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(root.children[-1], root)

        TreeNode.mergeNodes(node_e, root)
        TreeNode.mergeNodes(root.children[-1], root)

        # root.children[0].addDistance(root.children[1], 0.0)
        TreeNode.mergeNodes(root.children[1], root)

        # Act
        nni_runner(root)

        # Assert
        self.assertCountEqual(self.__get_motifs(root.getChild().children[0]), profiles[3].combine(profiles[5].combine(profiles[4])).motifs)
        self.assertCountEqual(self.__get_motifs(root.getChild().children[1]), profiles[1].combine(profiles[0].combine(profiles[2])).motifs)

    def test_complex_non_optimal_multi_layer_tree_global_switches(self):
        # Arrange
        dna = ["CCGC", "CCAT", "CCCC", "AAAA", "AAAT", "AATT"]
        [node_a, node_b, node_c, node_d, node_e, node_f], profiles, root = self.__node_factory(dna)

        node_e.addDistance(node_d, 0.0)
        node_e.addDistance(node_c, 2.0)
        node_e.addDistance(node_a, 10.0)

        node_a.addDistance(node_b, 0.0)
        node_a.addDistance(node_f, 2.0)

        TreeNode.mergeNodes(node_a, root)
        TreeNode.mergeNodes(root.children[-1], root)

        TreeNode.mergeNodes(node_e, root)
        TreeNode.mergeNodes(root.children[-1], root)

        # root.children[0].addDistance(root.children[1], 0.0)
        TreeNode.mergeNodes(root.children[1], root)

        # Act
        nni_runner(root)

        # Assert
        self.assertCountEqual(self.__get_motifs(root.getChild().children[1]), profiles[3].combine(profiles[5].combine(profiles[4])).motifs)
        self.assertCountEqual(self.__get_motifs(root.getChild().children[0]), profiles[1].combine(profiles[0].combine(profiles[2])).motifs)
    
    def __node_factory(self, dna_strings: List[str]) -> Tuple[List[TreeNode], List[Profile], TreeNode]:
        profiles = [Profile(string, name=string) for string in dna_strings]
        nodes = [TreeNode(profile) for profile in profiles]
        root: TreeNode = TreeNode(Profile("A", "root"))

        for node in nodes:
            root.addNode(node)

        return nodes, profiles, root
    
    def __tree_factory_list(self, branches: List[TreeNode], root) -> TreeNode:
        nodes = [self.__tree_factory_list(node, root) if isinstance(node, list) else node for node in branches] 
        return TreeNode.mergeNodes(nodes, root)
    
    def __tree_factory(self, left_branch: List[TreeNode], right_branch: List[TreeNode], root) -> TreeNode:
        left_root = self.__tree_factory(left_branch[0], left_branch[1], root) if isinstance(left_branch, list) else left_branch
        right_root = self.__tree_factory(right_branch[0], right_branch[1], root) if isinstance(right_branch, list) else right_branch

        return TreeNode.mergeNodes([left_root, right_root], root)
         
    def __get_motifs(self, node: TreeNode) -> List[str]:
        return node.getProfile().motifs

    

        