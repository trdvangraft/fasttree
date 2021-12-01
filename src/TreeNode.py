from src.profile import Profile

class TreeNode:
    children = []
    distances = []
    profile = None

    def __init__(self, prof):
        print("made TreeNode")
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

        newNode = TreeNode(self.profile.combine(n2.profile))
        return newNode

    def getProfile(self):
        return self.profile#TODO should this be a copy or the actual one?