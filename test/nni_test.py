from typing import List
import unittest

from src.utils import *
from src.profile import Profile
from src.TreeNode import TreeNode
from src.nni import nni_interchange


class NniTest(unittest.TestCase):
    def test_original_tree_is_optimal(self):
        # Arrange
        node_a, node_b, node_c, node_d = self.__node_factory(["CCC", "CCC", "AAA", "AAA"])
        root = self.__tree_factory([node_a, node_b], [node_c, node_d])

        # Act
        optimal_tree = nni_interchange(root)
        
        # Assert
        self.assertEqual(len(optimal_tree.children), 2)
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), self.__get_motifs(node_a.mergeNodes(node_b)))
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), self.__get_motifs(node_c.mergeNodes(node_d)))
    
    def test_non_optimal_tree_gets_corrected(self):
        # Arrange
        node_a, node_b, node_c, node_d = self.__node_factory(["CCC", "CCC", "AAA", "AAA"])
        root = self.__tree_factory([node_a, node_b], [node_c, node_d])

        # Act
        optimal_tree = nni_interchange(root)

        # Assert
        self.assertListEqual(self.__get_motifs(optimal_tree.children[0]), self.__get_motifs(node_a.mergeNodes(node_b)))
        self.assertListEqual(self.__get_motifs(optimal_tree.children[1]), self.__get_motifs(node_c.mergeNodes(node_d)))
    
    def test_complex_tree(self):
        # Arrange
        node_a, node_b, node_c, node_d, node_e = self.__node_factory(["CCC", "CCC", "AAA", "AAA", "TTT"])
        # We need to consider the following valid tree layout:
        # ((A, (B, C)), D, E)
        root = self.__tree_factory([[node_a, [node_b, node_c]], node_d, node_e])
    
    def __node_factory(self, dna_strings: List[str]) -> List[TreeNode]:
        return [TreeNode(Profile(string)) for string in dna_strings]
    
    def __tree_factory(self, branches: List[TreeNode]) -> TreeNode:
        pass
    
    def __tree_factory(self, left_branch: List[TreeNode], right_branch: List[TreeNode]) -> TreeNode:
        left_root = self.__tree_factory(left_branch[0], left_branch[1]) if isinstance(left_branch, list) else left_branch
        right_root = self.__tree_factory(right_branch[0], right_branch[1]) if isinstance(right_branch, list) else right_branch

        return left_root.mergeNodes(right_root)
         
    def __get_motifs(self, node: TreeNode) -> List[str]:
        return node.get_profile().motifs

    

        