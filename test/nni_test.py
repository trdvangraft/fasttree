import unittest

from typing import List, Optional, Tuple
from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode
from src.nni import nni_interchange


class NniTest(unittest.TestCase):
    def test_original_tree_is_optimal(self):
        # Arrange
        [node_a, node_b, node_c, node_d], profiles, root = self.__node_factory(["CCC", "CCC", "AAA", "AAA"])
        root = self.__tree_factory([node_a, node_b], [node_c, node_d], root).parent

        # Act
        optimal_tree = nni_interchange(root.children[0])
        
        # Assert
        self.assertEqual(len(optimal_tree.children), 2)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), profiles[0].combine(profiles[1]).motifs)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), profiles[2].combine(profiles[3]).motifs)
    
    def test_non_optimal_tree_gets_corrected(self):
        # Arrange
        [node_a, node_b, node_c, node_d], profiles, root = self.__node_factory(["CCC", "AAA", "CCC", "AAA"])
        root = self.__tree_factory([node_a, node_b], [node_c, node_d], root).parent

        # Act
        optimal_tree = nni_interchange(root.children[0])

        # Assert
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), profiles[0].combine(profiles[2]).motifs)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), profiles[1].combine(profiles[3]).motifs)

    def test_optimal_tree_with_three_nodes(self):
        # Arrange
        [node_a, node_b, node_c], profiles, root = self.__node_factory(["CCC", "CCC", "AAA"])
        root = self.__tree_factory([node_a, node_b], node_c, root)

        # Act
        optimal_tree = nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), profiles[0].combine(profiles[1]).motifs)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), profiles[2].motifs)

    def test_non_optimal_tree_with_three_nodes(self):
        # Arrange
        [node_a, node_b, node_c], profiles, root = self.__node_factory(["CCC", "AAA", "CCC"])
        root = self.__tree_factory([node_a, node_b], node_c, root)

        # Act
        optimal_tree = nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), profiles[0].combine(profiles[2]).motifs)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), profiles[1].motifs)

    def test_complex_non_optimal_tree_with_three_nodes(self):
        # Arrange
        [node_a, node_b, node_c], profiles, root = self.__node_factory(["CCGC", "CCAT", "CCCC"])
        root = self.__tree_factory([node_a, node_b], node_c, root)

        # Act
        optimal_tree = nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), profiles[0].combine(profiles[2]).motifs)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), profiles[1].motifs)

    
    def test_complex_tree(self):
        # Arrange
        [node_a, node_b, node_c, node_d, node_e], profiles,  root = self.__node_factory(["CCC", "CCC", "AAA", "AAA", "TTT"])
        # We need to consider the following valid tree layout:
        # ((A, (B, C)), D, E)
        root = self.__tree_factory_list([[node_a, [node_b, node_c]], node_d, node_e], root)

        # Acct
        optimal_tree = nni_interchange(root)

        # Assert


        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), profiles[0].combine(profiles[1]).motifs)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), profiles[4].combine(profiles[2]).combine(profiles[3]).motifs)
        
        left_branch: TreeNode = optimal_tree.children[0]
        self.assertListEqual(self.__get_motifs(left_branch.children[0]), profiles[4].motifs)
        self.assertListEqual(self.__get_motifs(left_branch.children[1]), profiles[2].combine(profiles[3]))
    
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

    

        