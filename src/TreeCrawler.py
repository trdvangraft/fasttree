from src.TreeNode import TreeNode
from operator import itemgetter

class TreeCrawler:
    #TODO: Test
    epsilon = 0


    root = None
    def __init__(self, root):
        # print("made TreeNode")

        if(not isinstance(root,TreeNode)):
            print("WARNING: root is not of type TreeNode")
            return

        self.root = root


    def startMerging(self):
        shortesDistances = []
        index = 0

        for n in self.root.children:
            shortesDistances.append({"distance":n.getFirstDistance(),"Node":n})

        while len(shortesDistances) > 1:
            print(index)
            index += 1

            print("len(shortestDistances)=="+str(len(shortesDistances)))

            merger = []
            cutoff = shortesDistances[0]["distance"] + self.epsilon
            merger.append(shortesDistances[0]["Node"])

            i = 1
            while i<len(shortesDistances) and shortesDistances[0]["distance"] + self.epsilon > shortesDistances[i]["distance"]:
                merger.append(shortesDistances[i]["Node"])
                i+= 1


            print("len(merger)=="+str(len(merger)))
            nParent = TreeNode.mergeNodes(merger,cutoff=cutoff)
            shortesDistances.append({"distance": nParent.getFirstDistance(),"Node":nParent})
            shortesDistances = sorted(shortesDistances, key=itemgetter('distance'))