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
        if(isinstance(n,TreeNode)):
            #TODO: check if n is already in node
            self.children.append(n)
        else:
            print("WARNING: tried adding a non-TreeNode to tree")

    def mergeNodes(self, n1, n2):
        if(not isinstance(n1,TreeNode) or not isinstance(n2,TreeNode)):
            print("WARNING: tried merging 2 entities while not both are of type TreeNode")
            return

        newNode = TreeNode(n1,n2)
        self.children.remove(n1)
        self.children.remove(n2)
        self.children.append(newNode)