from __future__ import annotations

from typing import List
from src.profile import Profile
from operator import itemgetter
from itertools import product
from functools import reduce
from src.utils import *


class TreeNode:

    m = 35  # 35 by default, but will be overwritten with root(N) where N is the number of sequences

    def __init__(self, prof):

        if(not isinstance(prof,Profile)):
            print("WARNING: prof is not of type Profile")
            return

        self.profile: Profile = prof
        self.nodeName = prof.name

        self.children: List[TreeNode] = []
        self.parent: TreeNode = None
        self.distances = []

        self.variance_correction = 0  # Variance correction = 0 for leaves
        self.outDistance = 0  # OutDistance = 0 for leaves
        self.nOutDistanceActive = -1
        
        # Update the updistance from child nodes, the average distance of the nodes from its children
        # Leave node's upDistance = 0
        self.upDistance = self.setSelfUpDistanceFromChild() 

        self.selfWeight = self.setSelfWeight()  # Sum of proportion of non-gaps in the profile of node i, save for fast use
        self.selfDistance = self.setSelfDistance()  # The average distance between children of node i, save for fast use

    # Add the node as a child of self
    def addNode(self, n):
        if (isinstance(n, TreeNode) and not n in self.children):
            n.parent = self
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    # Remove the node from the children of self
    def deleteNode(self, n):
        if (isinstance(n, TreeNode) and n in self.children):
            self.children.remove(n)
            n.parent = None
            # we update the profile to reflect the current number of children
            self.profile = self.children[-1].getProfile()

    # Return the i-th child
    def getChild(self, i: int = 0):
        return self.children[i]

    # This method will merge a node with it's closest sibling node
    @staticmethod
    def mergeNodes(node: TreeNode, root: TreeNode):
        # Only nodes directly under the root may merge
        # Since the rest already had been merged
        if not node.parent.parent == None:
            node.distances = []
            return node.getAncestor()

        # Get top ancestor of both nodes
        node : TreeNode = node.getAncestor()
        if len(node.distances) == 0:
            return node

        # Get the ancestor of the node that we have the shortest distance to
        otherNode : TreeNode = node.distances[0]["Node"].getAncestor()

        node.distances.remove(node.distances[0])
        if len(otherNode.distances)>0:
            otherNode.distances.remove(otherNode.distances[0])

        # Because we don't recalculate distances after each merge
        # It might be that distances refers to an node in the same subtree
        # In that case we do nothing and (might) continue merging other nodes
        if node == otherNode or node.profile.name == otherNode.profile.name:
            return node

        # Create the new parent for node and otherNode
        # Make it's profile, set the root and correct children of root
        nParent = TreeNode(node.profile.combine(otherNode.profile))
        nParent.parent = root
        nParent.m = node.m

        root.children.append(nParent)
        root.children.remove(node)
        root.children.remove(otherNode)

        # Add node and otherNode as children of their new parent
        nParent.children.append(node)
        nParent.children.append(otherNode)

        node.parent=nParent
        otherNode.parent = nParent

        # Use top-hit heuristics to make a list of distances
        # Distances is the list of shortest distances of the children
        # The underlying idea is that if a node is close to A it is also close to (A,B)
        nParent.distances = node.distances + otherNode.distances
        nParent.sortDistances()

        # Set distances to speed-up future computations
        nParent.selfDistance = nParent.setSelfDistance()
        nParent.selfWeight = nParent.setSelfWeight()
        nParent.upDistance = nParent.setSelfUpDistanceFromChild()

        # Empty the child distances as they are no longer needed and save space
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


    def setSelfWeight(self):
        if self.profile:
            return sum(self.profile.get_weights()) / len(self.profile.get_weights())
        else:
            return None

    def setSelfDistance(self):
        sum = 0
        n_children = len(self.children)
        for i, j in product(range(n_children), range(n_children)):
            (weight, dist), incorr_weight = self.children[i].profile.distance(self.children[j].profile)
            sum += dist
        return sum

    def setSelfUpDistanceFromChild(self):
        sum = 0
        for child in self.children:
            (weight, dist), incorr_weight = child.profile.distance(self.profile)
            sum += dist
        return sum

    def addDistance(self, node: TreeNode, distance: float):
        self.distances.append({'distance': distance, 'Node': node})

    # Calculate distances to all other nodes
    # Should only be called on the root
    def calcDistances(self):
        # Empty distances for each child in case it isn't the first time distances are calculated
        for node in self.children:
            node.distances = []

        # Calculate all distances
        # Since distances are symmetrical each distance is added to both nodes
        for i in range(len(self.children)):
            for j in range(i+1,len(self.children)):
                na : TreeNode = self.children[i]
                nb : TreeNode = self.children[j]

                distance = setJoinsCriterion(self,na,nb,len(self.children))
                na.addDistance(nb,distance)
                nb.addDistance(na,distance)

        # Sort distances and keep the top m
        for n in self.children:
            n.sortDistances()

        print("calculated all distances")

    # Get the lowest distance for this node
    def getFirstDistance(self):
        if len(self.distances) > 0:
            return self.distances[0]["distance"]

        return 9999999999999999999999999

    # Generate the profile corresponding to the children
    # Useful for the root node
    def generateProfileFromChildren(self):
        p = None
        for c in self.children:
            if p == None:
                p = c.getProfile()
            else:
                p = p.combine(c.getProfile())
        self.profile = p
        self.nodeName = p.name

    # Return whether this node contains leaf nodes
    def isTerminalSplitNode(self) -> bool:
        return all([len(child.children) == 0 for child in self.children])

    def isLeafNode(self) -> bool:
        return len(self.children) == 0

    # Get the highest ancestor that is below the root
    def getAncestor(self):
        x = self

        while x.parent.parent is not None:
            x = x.parent

        return x

    # Sort and limit the distances
    def sortDistances(self):
        self.distances = sorted(self.distances, key=itemgetter('distance'), reverse=False)[:self.m]

    # Only called on the root
    # Check whether all children have distances
    def allChildrenHaveDistances(self):
        for child in self.children:
            if not child.hasDistances():
                return False

        return True

    #returns whether the node has children
    def hasDistances(self):
        return len(self.children) > 0
