from src.profile import Profile
from operator import itemgetter

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

    def addNode(self, n):
        if(isinstance(n,TreeNode) and not n in self.children):
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    def deleteNode(self,n):#TODO do we ever want this?
        if(isinstance(n,TreeNode) and n in self.children):
            self.children.remove(n)

    def mergeNodes(self, n2):
        if(not isinstance(n2,TreeNode)):
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
