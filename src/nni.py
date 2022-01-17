from typing import Deque, List, Tuple
from collections import deque
from itertools import combinations
from src.TreeNode import TreeNode
from src.profile import Profile

import numpy as np

NODE_CONFIGS = {
    3: [
        [0, 1, 2],
        [1, 2, 0],
        [2, 1, 0]
    ],
    4: [
        [0, 1, 2, 3],
        [1, 2, 0, 3],
        [0, 2,  1, 3],
    ]
}

def nni_runner(root: TreeNode) -> TreeNode:
    # perform the root interchange
    nni_interchange(root.getChild())
    queue = deque(root.getChild().children)

    while len(queue) > 0:
        current_node: TreeNode = queue.popleft()

        # we cant do an interchange on a leaf node
        if current_node.isLeafNode():
            continue

        # perform nni of the current node
        nni_interchange(current_node)
        for child in current_node.children:
            queue.append(child)
        
def nni_interchange(root: TreeNode) -> TreeNode:
    if root.isLeafNode() or root.isTerminalSplitNode():
        return

    # we ignore the fake root node and immediatly move down to the actual root node
    profiles, nodes, number_of_children = __get_nodes_and_profiles(root)

    # we apply a reverse operation such that the two trees appear the same for the algorithm
    if len(nodes) == 3 and number_of_children[0] == 2:
        profiles, nodes, number_of_children = profiles[::-1], nodes[::-1], number_of_children[::-1]

    shape_node_configs = NODE_CONFIGS[len(profiles)]

    score = [__get_log_distance(profiles[shape_node_config]) for shape_node_config in shape_node_configs]

    # if the index of min score is zero then we keep the original tree
    if score.index(min(score)) == 0:
        return

    __rebuild_tree(nodes, shape_node_configs[score.index(min(score))])


def __rebuild_tree(nodes: List[TreeNode], node_config: List[int]):
    optimal_profile: List[TreeNode] = nodes[node_config]

    if len(optimal_profile) == 4:
        node_a, node_b, node_c, node_d = optimal_profile
        left_parent, right_parent = node_a.parent, node_d.parent

        # remove the nodes that are to be swapped
        node_b.parent.deleteNode(node_b)
        node_c.parent.deleteNode(node_c)

        # add the nodes back to their parents
        left_parent.addNode(node_b)
        right_parent.addNode(node_c)

        # recalculate the profile for the parents
        right_parent.generateProfileFromChildren()
        left_parent.generateProfileFromChildren()

    elif len(optimal_profile) == 3:
        node_a, node_b, node_c = optimal_profile
        left_parent, right_parent = node_c.parent, node_b.parent

        # remove nodes that are to be swapped
        node_a.parent.deleteNode(node_a)
        node_c.parent.deleteNode(node_c)

        # add the nodes back to their parents
        left_parent.addNode(node_a)
        right_parent.addNode(node_c)
    
        # recalculate the profile for the parents
        right_parent.generateProfileFromChildren()
        left_parent.generateProfileFromChildren()



def __get_nodes_and_profiles(root: TreeNode) -> Tuple[List[Profile], List[TreeNode], List[int]]:
    # since we are only expecting binary tree we can just get the children of the root node
    # two scenarios can happen a child is already a leaf node or a child is an internal node
    # if the child is a leaf we add it to the node list else we add the childen of the internal node

    nodes: List[TreeNode] = []
    number_of_children: List[int] = []

    for child in root.children:
        if child.isLeafNode():
            nodes.append(child)
            number_of_children.append(1)
        else:
            number_of_children.append(2)
            for grand_child in child.children:
                nodes.append(grand_child)

    
    profiles: List[Profile] = [node.getProfile() for node in nodes]
    return np.array(profiles), np.array(nodes), number_of_children

def __get_log_distance(profiles: List[Profile]) -> float:
    if len(profiles) == 3:
        return profiles[1].log_distance(profiles[2]) + profiles[0].log_distance(profiles[0])
    elif len(profiles) == 4:
        return profiles[0].log_distance(profiles[1]) + profiles[2].log_distance(profiles[3])



