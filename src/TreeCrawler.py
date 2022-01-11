from src.TreeNode import TreeNode
from operator import itemgetter

class TreeCrawler:
    #TODO: Test
    epsilon = 0.5


    root = None
    def __init__(self, root):
        # print("made TreeNode")

        if(not isinstance(root,TreeNode)):
            print("WARNING: root is not of type TreeNode")
            return

        self.root = root


    def startMerging(self):
        index = 0
        shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node":n} for n in self.root.children], key=itemgetter('distance'), reverse=True)

        # well our queue is not empty we can update the tree! 
        while len(self.root.children) > 1:
            print("index=="+str(index))
            index += 1

            print("len(shortestDistances)=="+str(len(shortesDistances)))

            cutoff = shortesDistances[0]["distance"] + self.epsilon
            merger = [shortesDistances[0]["Node"]]

            i = 1
            while i < len(shortesDistances) and cutoff > shortesDistances[i]["distance"]:
                if shortesDistances[i]["Node"].hasLowDistanceTo(merger[0],cutoff):
                    merger.append(shortesDistances[i]["Node"])
                    shortesDistances.remove(shortesDistances[i])
                # cutoff = merger[-1].getFirstDistance() + self.epsilon
                i += 1

            

            print("len(merger)=="+str(len(merger)))
            nParent = TreeNode.mergeNodes(merger, self.root)
            shortesDistances.append({"distance": nParent.getFirstDistance(),"Node":nParent})
            shortesDistances = sorted(shortesDistances, key=itemgetter('distance'), reverse=True)