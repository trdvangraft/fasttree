from __future__ import annotations

from typing import List
from src.profile import Profile
from operator import itemgetter
from itertools import product
from functools import reduce
from src.utils import *


class TreeNode:

    m = 5#TODO: should be some global constant(how many distances to keep from each node)

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
    def mergeNodes(nodes: List[TreeNode], cutoff : float, root: TreeNode):
        #check if all nodes have the same parent
        for i in range(len(nodes)):
            if (x := nodes[i]) and not x.parent.parent == None:
                print("WARNING: Node that isn't directly under root is found 1")
                while not x.parent.parent == None:
                    x = x.parent
                nodes[i] = x

        for i in range(len(nodes)):
            if nodes[i].parent.parent == None:
                print("WARNING: Node that isn't directly under root is found 2")
                while not x.parent.parent == None:
                    x = x.parent
                nodes[i] = x


        base = [nodes[0], nodes[0].distances[0]["Node"]]

        q=  [node.distances for node in nodes]
        print(q)
        t = [item["Node"] for sublist in q for item in sublist]#todo no clue why or how this works
        print(t)
        added = [n for n in t if (n.hasLowDistanceTo(base[0],cutoff) or n.hasLowDistanceTo(base[1],cutoff))]
        print(str(type(nodes)))


        print("len(base)=="+str(len(base)))
        print("len(added)=="+str(len(added)))
        print("len(nodes)=="+str(len(nodes)))
        nodes = base + added
        nodes = list(set(nodes))
        print("type=="+str(type(base)))
        print("2e len(nodes)=="+str(len(nodes)))



        #make new parent node with the original parent
        nParent = TreeNode(reduce(lambda acc, p: acc.combine(p.profile), nodes[1:], nodes[0].profile))
        nParent.parent = root
        root.children.append(nParent)

        #set all node parents to the new parent
        #add all nodes to the new parent
        for n in nodes:
            n.parent = nParent
            nParent.children.append(n)

        #merge distances
        nParent.distances = nodes[0].distances
        for n in nodes[1:]:
            nParent.distances = sorted(nParent.distances + n.distances, key=itemgetter('distance'))[:n.m]

        #TODO: make an test to see if this works
        #DONT DO IT LIKE THIS
        for n in nodes:
            if n in root.children:
                root.children.remove(n)


        # update the self distance
        nParent.__setSelfDistance()
        # TODO: update the covariance correction with weight
        # weight = updateWeight()
        # nParent.setVarianceCorrection(nodes[0]. nodes[1])

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
                # print("typeof(distance)=="+str(type(distance)))
                na.addDistance(nb,distance)
                nb.addDistance(na,distance)

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

    def getAncestor(self):
        x = self
        if self.parent.parent == None:
            x = x.parent.parent
        return x