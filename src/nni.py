from typing import List
from src.TreeNode import TreeNode
from src.profile import Profile

import numpy as np

NODE_CONFIGS = [
    [0, 1, 2, 3],
    [1, 2, 0, 3],
    [2, 0, 1, 3],
]

def nni_interchange(root: TreeNode) -> TreeNode:
    profiles = __get_profiles(root)
    score = [__get_log_distance(profiles[NODE_CONFIG]) for NODE_CONFIG in NODE_CONFIGS]

    return __rebuild_tree(profiles, NODE_CONFIGS[score.index(min(score))])

def __rebuild_tree(profiles: List[Profile], node_config: List[int]) -> TreeNode:
    optimal_profile = profiles[node_config]

    node_ab = TreeNode(optimal_profile[0]).mergeNodes(TreeNode(optimal_profile[1]))
    node_cd = TreeNode(optimal_profile[2]).mergeNodes(TreeNode(optimal_profile[3]))

    return node_ab.mergeNodes(node_cd)

def __get_profiles(root: TreeNode) -> List[Profile]:
    return np.array([grand_child.get_profile() for child in root.children for grand_child in child.children])

def __get_log_distance(profiles: List[Profile]) -> float:
    return profiles[0].log_distance(profiles[1]) + profiles[2].log_distance(profiles[3])


