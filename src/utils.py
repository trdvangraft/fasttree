# encoding: utf-8
"""
@author: Xinqi
@contact: lixinqi98@gmail.com
@file: utils.py
@time: 12/7/21
@desc:
"""
import logging
import src.TreeNode as TreeNode

logging.basicConfig(format='%(asctime)s-10s | %(levelname)-8s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='FastTree.log', level=logging.DEBUG)


def updateVariance(node_i: TreeNode, node_j: TreeNode):
    """
    V(i,j) = profileDistance(i,j) - v(i) - v(j)
    :param node_i:
    :param node_j:
    :return: V(i,j)
    """
    (weight, prof_dist), incorr_weight = node_i.profile.distance(node_j.profile)
    return prof_dist - node_i.variance_correction - node_j.variance_correction


def updateWeight(root: TreeNode, node_i: TreeNode, node_j: TreeNode, active_num):
    """
    Weights the join of i,j with minimizing the variance of the distance estimates for the new node ij
    top = \sum_{k!i,j}(V(j,k)-V(i,k)) = (n-2)(v(i)-v(j)) + \sum_{k!i,j} profileDistance(j,k) - \sum_{k!i,j} profileDistance(i,k)
    = (n-2)(v(i)-v(j)) + n(profileDistance(j, T) - profileDistance(i, T))
    weight = 0.5 + top / 2(n-2)V(i,j)
    :param root:
    :param node_i:
    :param node_j:
    :param active_num:
    :return: Lamda, the weight of i in ij
    """
    # TODO: check whether outProfile will be implemented as the profile of root node
    (weight_i, dist_i), incorr_weight_i = node_i.profile.distance(root.profile)
    (weight_j, dist_j), incorr_weight_j = node_j.profile.distance(root.profile)
    top = (active_num - 2) * (node_i.variance_correction - node_j.variance_correction) + active_num * (dist_i - dist_j)
    bottom = 2 * (active_num - 2) * updateVariance(node_i, node_j)
    return 0.5 + top / bottom


def internalNodesDistance(node_i: TreeNode, node_j: TreeNode):
    """
    distance between nodes:d(i,j) = profiledistance(i,j) - upDistance(i) - upDistance(j)
    :param node_i:
    :param node_j:
    :return:
    """
    (weight, prof_dist), incorr_weight = node_i.profile.distance(node_j.profile)
    return prof_dist - node_i.upDistance - node_j.upDistance


def setJoinsCriterion(root: TreeNode, node_i: TreeNode, node_j: TreeNode, active_num):
    """
    Neighbor Joining Criterion: d_u(i,j) - r(i) - r(j)
    :param root:
    :param node_i:
    :param node_j:
    :param active_num:
    :return: criterion
    """
    if node_i.parent is not None or node_i.parent is not None:#TODO: all nodes have a parent except the root, so this check seems strange
        return
    # assert node_i.nOutDistanceActive >= active_num
    # assert node_j.nOutDistanceActive >= active_num
    node_dist = internalNodesDistance(node_i, node_j)
    outdist_i = setOutDistance(root, node_i, active_num)
    outdist_j = setOutDistance(root, node_i, active_num)
    return node_dist - outdist_i - outdist_j


def setOutDistance(root: TreeNode, node: TreeNode, active_num):
    """
    In the absence of gaps, compute the out-distance of node i to other active nodes:
    r(i) = \sum_{k!=i} d_u(i,k) / (n-2)
    Compute each out-distance as needed in O(La) time by using a "total profile" T which is the average of all
    active nodes' profile, u(i) indicating the "up-distance" or the average of the node from its children
    \sum_{k!=i} d_u(i,k) = n*\delta(i, T) - \delta(i,i) - (n-2) * u(i) - \sum_j u(j)
    With gaps, take the weights of the comparisons into account
    \sum_{k!=i} d_u(i,k) = (n-1)*\delta(i, T-i) - \delta(i,i) - (n-2) * u(i) - \sum_j u(j)
    \delta(i, T-i) = \sum_{j!=i}\sum_{l=1}^L \delta_l(i,j)w_l(i)w_l(j) / \sum_{j!=i}\sum_{l=1}^L w_l(i)w_l(j)
    :param root:
    :param node:
    :param active_num:
    :return: out-distance
    """
    (weight, dist), incorr_weight = node.profile.distance(root.profile)
    # TODO: check if root.upDistance represent the total up distance
    if node.selfWeight is not None:
        # with gaps
        delta = (dist * weight * active_num - node.selfWeight * node.selfDistance) / (
                weight * active_num - node.selfDistance)
        out_dist = (active_num - 1) * delta - (active_num - 2) * node.upDistance - root.upDistance
    else:
        # without gaps
        out_dist = active_num * dist - node.selfDistance - (active_num - 2) * node.upDistance - root.upDistance

    node.outDistance = out_dist / (active_num - 2)
    node.nOutDistanceActive = active_num
    return node.outDistance
