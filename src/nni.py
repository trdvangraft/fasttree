from typing import Deque, List
from collections import deque
from itertools import combinations
from src.TreeNode import TreeNode
from src.profile import Profile

import numpy as np

NODE_CONFIGS = {
    3: [
        [0, 1, 2],
        [0, 2, 1],
        [1, 2, 0]
    ],
    4: [
        [0, 1, 2, 3],
        [1, 2, 0, 3],
        [2, 0, 1, 3],
    ],
    5: [
        [0, 4, 3, 1, 2],
        [0, 4, 2, 1, 3],
        [0, 2, 4, 1, 3],
        [1, 3, 0, 2, 4],
        [0, 3, 1, 2, 4],
        [0, 1, 3, 2, 4],
        [0, 1, 2, 3, 4],
        [0, 1, 4, 2, 3],
        [1, 4, 0, 2, 3],
        [0, 4, 1, 2, 3],
        [0, 2, 3, 1, 4],
        [0, 3, 4, 1, 2],
        [0, 2, 1, 3, 4],
        [0, 3, 2, 1, 4],
        [1, 2, 0, 3, 4],
    ]
}


def nni_interchange(root: TreeNode) -> TreeNode:
    # we ignore the fake root node and immediatly move down to the actual root node
    profiles = __get_profiles(root)

    shape_node_configs = NODE_CONFIGS[len(profiles)]

    score = [__get_log_distance(profiles[shape_node_config]) for shape_node_config in shape_node_configs]

    new_tree = __rebuild_tree(profiles, shape_node_configs[score.index(min(score))])

    return new_tree

def __rebuild_tree(profiles: List[Profile], node_config: List[int]) -> TreeNode:
    optimal_profile = profiles[node_config]

    root: TreeNode = TreeNode(Profile("A", "root"))

    nodes = [TreeNode(profile_idx) for profile_idx in optimal_profile]

    for node in nodes:
        root.addNode(node)

    if len(optimal_profile) == 5:
        node_ab = TreeNode.mergeNodes([nodes[1], nodes[2]], root)
        node_cab = TreeNode.mergeNodes([nodes[0], node_ab], root)
        node_de = TreeNode.mergeNodes([nodes[3], nodes[4]], root)
        return TreeNode.mergeNodes([node_cab, node_de], root)
    elif len(optimal_profile) == 4 or len(optimal_profile) == 3:
        node_ab = TreeNode.mergeNodes(nodes[:2], root)
        node_cd = TreeNode.mergeNodes(nodes[2:], root)

        return TreeNode.mergeNodes([node_ab, node_cd], root)
    else:
        return TreeNode.mergeNodes(nodes, root)



def __get_profiles(root: TreeNode) -> List[Profile]:
    # we implemenent a queue to BFS search the tree for Profiles
    queue: Deque[TreeNode] = deque(root.children)
    profiles: List[Profile] = []

    while len(queue) > 0 and len(profiles) <= 5:
        current_node = queue.popleft()

        if current_node.isLeafNode():
            profiles.append(current_node.getProfile())
        else:
            for child in current_node.children:
                queue.append(child)

    return np.array(profiles)

def __get_log_distance(profiles: List[Profile]) -> float:
    if len(profiles) == 3:
        return profiles[0].log_distance(profiles[1]) + profiles[2].log_distance(profiles[2])
    elif len(profiles) == 4:
        return profiles[0].log_distance(profiles[1]) + profiles[2].log_distance(profiles[3])
    elif len(profiles) == 5:
        return profiles[0].log_distance(profiles[1].combine(profiles[2])) + profiles[1].log_distance(profiles[2]) + profiles[3].log_distance(profiles[4])



