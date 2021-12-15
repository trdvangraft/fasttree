from operator import itemgetter
from itertools import product
from src.profile import Profile
from operator import itemgetter
from src.utils import *

class TreeNode:

    m = 5#TODO: should be some global constant(how many distances to keep from each node)

    parent = None
    children = []
    distances = []#tuple of type (distance,connectingNode)



    profile = None

    def __init__(self, prof):
        # print("made TreeNode")

        if(not isinstance(prof,Profile)):
            print("WARNING: prof is not of type Profile")
            return

        self.profile = prof

        self.variance_correction = 0  # variance correction = 0 for leaves
        self.upDistance = 0  # updistance = 0 for leaves
        self.nOutDistanceActive = -1
        self.outDistance = -1

        self.selfWeight = self.__setSelfWeight()  # sum of proportion of non-gaps in the profile of node i, save for fast use
        self.selfDistance = self.__setSelfDistance()  # the average distance between children of node i, save for fast use

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

        distances = self.distances
        for n in n2.distances:
            distances.append(n)

        distances = sorted(distances, key=itemgetter('distance'))
        distances = distances[0:5]

        newNode = TreeNode(self.profile.combine(n2.profile))
        newNode.distances = distances
        return newNode

    def getProfile(self):
        return self.profile#TODO should this be a copy or the actual one?

    def setUpDistance(self, node_i, node_j, weight=0.5):
        """
        update the upDistance of node_ij based on node_i and node_j
        if not weighted, u(ij) = (ProfileDistance(i, j)) / 2
        Weighted Join, u(ij) = weight(u(i)+d(i,ij)) + (1-weight)(u(j)+d(j,ij))
        :param node_i:
        :param node_j:
        :param weight: if not weighted, default weight is 1/2
        :return:
        """
        node_dist_ij = internalNodesDistance(node_i, node_j)
        dist_i_ij = (node_dist_ij + node_i.upDistance - node_j.upDistance) / 2
        dist_j_ij = (node_dist_ij + node_j.upDistance - node_i.upDistance) / 2

        self.upDistance = weight * (node_i.upDistance + dist_i_ij) + (1 - weight) * (node_j.upDistance + dist_j_ij)

    def setVarianceCorrection(self, node_i, node_j, weight=0.5):
        """
        update the variance correction of node_ij based on node_i and node_j
        v(ij) = weight*v(i)+(1-weight)*v(j)+weight*(1-weight)*V(i,j)
        :param node_i:
        :param node_j:
        :param weight: if not weighted, default weight is 1/2
        :return:
        """
        self.variance_correction = weight * node_i.variance_correction + (
                    1 - weight) * node_j.variance_correction + weight * (1 - weight) * updateVariance(node_i, node_j)

    def __setSelfWeight(self):
        if self.profile:
            return sum(self.profile.get_weights()) / len(self.profile.get_weights())
        else:
            return None

    def __setSelfDistance(self):
        sum = 0
        n_children = len(self.children)
        for i, j in product(range(n_children), range(n_children)):
            sum += self.children[i].profile.distance(self.children[j].profile)
        return sum

