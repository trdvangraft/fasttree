from src.profile import Profile
from operator import itemgetter
from src.utils import *


class TreeNode:
    m = 5  # TODO: should be some global constant(how many distances to keep from each node)

    parent = None
    children = []
    distances = []  # tuple of type (distance,connectingNode)

    profile = None
    variance_correction = 0  # variance correction = 0 for leaves
    upDistance = 0  # updistance = 0 for leaves
    nOutDistanceActive = -1
    outDistance = -1
    selfWeight = None  # sum of proportion of non-gaps in the profile of node i, save for fast use
    selfDistance = 0  # the average distance between children of node i, save for fast use

    def __init__(self, prof):
        # print("made TreeNode")

        if (not isinstance(prof, Profile)):
            print("WARNING: prof is not of type Profile")
            return

        self.profile = prof

    def addNode(self, n):
        if (isinstance(n, TreeNode) and not n in self.children):
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    def deleteNode(self, n):  # TODO do we ever want this?
        if (isinstance(n, TreeNode) and n in self.children):
            self.children.remove(n)

    @staticmethod
    def mergeNodes(nodes):
        # check if all are of type TreeNode
        for n in nodes:
            if (not isinstance(n, TreeNode)):
                print("WARNING: tried TreeNode merging with a non-TreeNode object type")
                return

        # check if all nodes have the same parent
        for x in nodes:
            if not x.parent == nodes[0].parent:
                print("WARNING: tried merging with a non-TreeNode object type")

        # mergeProfiles
        pParent = nodes[0].profile
        for p in nodes[1:]:
            pParent = pParent.combine(p.profile)

        # make new parent node with the original parent
        nParent = TreeNode(pParent)
        nParent.parent = nodes[0].parent

        # set all node parents to the new parent
        # add all nodes to the new parent
        for n in nodes:
            n.parent = nParent
            nParent.children.append(n)

        # merge distances
        nParent.distances = nodes[0].distances
        for n in nodes[1:]:
            nParent.distances = sorted(nParent.distances + n.distances, key=itemgetter('distance'))[:n.m]

        # TODO: make an test to see if this works
        # remove nodes from old parent
        for n in nodes:
            if isinstance(nParent.parent, TreeNode):
                nParent.parent.children.remove(n)

        return nParent

    def getProfile(self):
        return self.profile  # TODO should this be a copy or the actual one?

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

    def addDistance(self, node, distance):
        self.distances.append({'distance': distance, 'Node': node})
        # TODO: keep it space efficient by deleting when it goes over root(N)

    def calcDistances(self):
        for i in range(len(self.children)):
            for j in range(i + 1, len(self.children)):
                na: TreeNode = self.children[i]
                nb: TreeNode = self.children[j]

                distance = setJoinsCriterion(self, na, nb)
                na.addDistance(nb, distance)
                nb.addDistance(na, distance)

    def getFirstDistance(self):  # TODO Test
        if len(self.distances) > 0:
            return self.distances[0]

        return 9999999999999999999999999

    def generateProfileFromChildren(self):
        p = None

        print("Profile before update == ")
        print(self.profile.get_frequency_profile())
        for c in self.children:
            if p == None:
                p = c.getProfile()
            else:
                p = p.combine(c.getProfile())
        self.profile = p
        print("Profile before update == ")
        print(self.profile.get_frequency_profile())
