class TreeNode:
    children = []
    distances = []
    profile = 0;#TODO: put profile class here

    def __init__(self):
        print("made TreeNode")

    def __int__(self,n1,n2):
        if (not isinstance(n1, TreeNode) or not isinstance(n2, TreeNode)):
            print("WARNING: tried merging 2 entities while not both are of type TreeNode")
            return

        #TODO: merge profiles

    def addNode(self, n):
        if(isinstance(n,TreeNode) and not n in self.children):
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    def deleteNode(self,n):#TODO do we ever want this?
        if(isinstance(n,TreeNode) and n in self.children):
            self.children.remove(n)

    def mergeNodes(self, n1, n2):
        if(not isinstance(n1,TreeNode) or not isinstance(n2,TreeNode)):
            print("WARNING: tried merging 2 entities while not both are of type TreeNode")
            return

        newNode = TreeNode(n1,n2)
        self.children.remove(n1)
        self.children.remove(n2)
        self.children.append(newNode)