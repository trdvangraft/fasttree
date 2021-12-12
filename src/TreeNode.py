from __future__ import annotations

from operator import itemgetter
from typing import List

from src.profile import Profile
from operator import itemgetter
from src.utils import *

class TreeNode:

    m = 5#TODO: should be some global constant(how many distances to keep from each node)

    variance_correction = 0  # variance correction = 0 for leaves
    upDistance = 0  # updistance = 0 for leaves
    nOutDistanceActive = -1
    outDistance = -1
    selfWeight = None  # sum of proportion of non-gaps in the profile of node i, save for fast use
    selfDistance = 0  # the average distance between children of node i, save for fast use

    def __init__(self, prof):
        # print("made TreeNode")

        if(not isinstance(prof,Profile)):
            print("WARNING: prof is not of type Profile")
            return

        self.profile = prof
        self.parent = None
        self.children: List[TreeNode] = []
        self.distances = [] #tuple of type (distance,connectingNode)

    def addNode(self, n):
        if (isinstance(n, TreeNode) and not n in self.children):
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    def deleteNode(self, n):  # TODO do we ever want this?
        if (isinstance(n, TreeNode) and n in self.children):
            self.children.remove(n)

    def mergeNodes(self, n2):
        if (not isinstance(n2, TreeNode)):
            print("WARNING: tried merging with a non-TreeNode object type")
            return

        # New
        newNode = TreeNode(self.profile.combine(n2.profile))
        newNode.distances = sorted(self.distances + n2.distances, key=itemgetter('distance'))[:5]

        # add the merged nodes as children to the new node
        newNode.addNode(self)
        newNode.addNode(n2)

        return newNode

    def get_profile(self):
        return self.profile#TODO should this be a copy or the actual one?

    def setUpDistance(self, node_i, node_j, weight=0.5):
        """
        update the upDistance of node_ij based on node_i and node_j
        if not weighted, u(ij) = (ProfileDistance(i, j)) / 2
        Weighted Join, u(ij) = Lamda(u(i)+d(i,ij)) + (1-Lamda)(u(j)+d(j,ij))
        :param node_i:
        :param node_j:
        :param node_ij:
        :param weight: if not weighted, default weight is 1/2
        :return:
        """
        (weight_i, dist_i_ij), incorr_weight_i = node_i.profile.distance(self.profile)
        (weight_j, dist_j_ij), incorr_weight_j = node_j.profile.distance(self.profile)

        self.upDistance = weight * (node_i.upDistance + dist_i_ij) + (1 - weight) * (node_j.upDistance + dist_j_ij)

    def setVarianceCorrection(self, node_i, node_j, weight):
        """
        v(ij) = Lamda*v(i)+(1-Lamda)*v(j)+Lamda*(1-Lamda)*V(i,j)
        :param node_i:
        :param node_j:
        :param weight:
        :return:
        """
        self.variance_correction = weight * node_i.variance_correction + (
                    1 - weight) * node_j.variance_correction + weight * (1 - weight) * updateVariance(node_i, node_j)
