from __future__ import annotations

from typing import List
from src.profile import Profile
from operator import itemgetter
from itertools import product
from functools import reduce
from src.utils import *


class TreeNode:

    m = 35#TODO: should be some global constant(how many distances to keep from each node)

    def __init__(self, prof):
        # print("made TreeNode")

        if(not isinstance(prof,Profile)):
            print("WARNING: prof is not of type Profile")
            return

        self.profile = prof
        self.nodeName = prof.name

        self.children = []
        self.parent = None
        self.distances = []

        self.variance_correction = 0  # variance correction = 0 for leaves
        self.upDistance = 0  # updistance = 0 for leaves
        self.nOutDistanceActive = -1
        self.outDistance = -1

        self.selfWeight = self.__setSelfWeight()  # sum of proportion of non-gaps in the profile of node i, save for fast use
        self.selfDistance = self.__setSelfDistance()  # the average distance between children of node i, save for fast use

    def addNode(self, n):
        if (isinstance(n, TreeNode) and not n in self.children):
            n.parent = self
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    def deleteNode(self, n):  # TODO do we ever want this?
        if (isinstance(n, TreeNode) and n in self.children):
            self.children.remove(n)

    @staticmethod
    def mergeNodes(node: TreeNode, root: TreeNode):

        if not node.parent.parent == None:
            node.distances = []
            return node.getAncestor()

        nName = node.profile.name
        #get top ancestor of both
        node : TreeNode = node.getAncestor()
        if len(node.distances) == 0:
            return node

        otherNode : TreeNode = node.distances[0]["Node"].getAncestor()

        node.distances.remove(node.distances[0])
        if len(otherNode.distances)>0:
            otherNode.distances.remove(otherNode.distances[0])

        if not node.parent.parent == None:
            print("node not under root")

        if not otherNode.parent.parent == None:
            print("otherNode not under root")

            #if those are the same -> return it
        if node == otherNode or node.profile.name == otherNode.profile.name:
            return node

        #create profile and set root
        nParent = TreeNode(node.profile.combine(otherNode.profile))
        nParent.parent = root

        root.children.append(nParent)
        root.children.remove(node)
        root.children.remove(otherNode)

        #add both children to new parent
        nParent.children.append(node)
        nParent.children.append(otherNode)

        node.parent=nParent
        otherNode.parent = nParent

        nParent.distances = node.distances + otherNode.distances#todo: limit number
        nParent.sortDistances()
        nParent.__setSelfDistance()
        nParent.__setSelfWeight()

        node.distances = []
        otherNode.distances = []

        return nParent

    def getProfile(self):
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


    def __setSelfWeight(self):
        if self.profile:
            return sum(self.profile.get_weights()) / len(self.profile.get_weights())
        else:
            return None

    def __setSelfDistance(self):
        sum = 0
        n_children = len(self.children)
        for i, j in product(range(n_children), range(n_children)):
            (weight, dist), incorr_weight = self.children[i].profile.distance(self.children[j].profile)
            sum += dist
        return sum


    def addDistance(self, node, distance):
        self.distances.append({'distance': distance, 'Node': node})
        #TODO: keep it space efficient by deleting when it goes over root(N)

    def calcDistances(self):
        for i in range(len(self.children)):
            for j in range(i+1,len(self.children)):
                na : TreeNode = self.children[i]
                nb : TreeNode = self.children[j]

                distance = setJoinsCriterion(self,na,nb,len(self.children))
                na.addDistance(nb,distance)
                nb.addDistance(na,distance)

        for n in self.children:
            n.sortDistances()

    def getFirstDistance(self):#TODO Test
        if len(self.distances) > 0:
            return self.distances[0]["distance"]

        return 9999999999999999999999999

    def generateProfileFromChildren(self):
        p = None
        for c in self.children:
            if p == None:
                p = c.getProfile()
            else:
                p = p.combine(c.getProfile())
        self.profile = p

    def hasLowDistanceTo(self, target : TreeNode, limit:float):
        for d in self.distances:
            if d["distance"] <= limit and d["Node"].getAncestor() == target:
                return True

        return False

    def isLeafNode(self) -> bool:
        return len(self.children) == 0
        
    def getAncestor(self):
        x = self

        while x.parent.parent is not None:
            x = x.parent

        return x

    def sortDistances(self):
        self.distances = sorted(self.distances, key=itemgetter('distance'), reverse=False)[:self.m]
