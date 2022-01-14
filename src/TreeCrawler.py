from src.TreeNode import TreeNode
from operator import itemgetter

class TreeCrawler:
    #TODO: Test
    epsilon = 0.0


    root = None
    def __init__(self, root):
        # print("made TreeNode")

        if(not isinstance(root,TreeNode)):
            print("WARNING: root is not of type TreeNode")
            return

        self.root = root


    def startMerging(self):
        sortDirection = False#true for reversed order

        index = 0
        shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node":n} for n in self.root.children], key=itemgetter('distance'), reverse=sortDirection)

        # well our queue is not empty we can update the tree! 
        while len(shortesDistances) > 1:
            print("index=="+str(index))
            index += 1

            #merge shortest distance
            TreeNode.mergeNodes(shortesDistances[0]["Node"], self.root)

            shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node": n} for n in self.root.children],
                                      key=itemgetter('distance'), reverse=sortDirection)
