from src.TreeNode import TreeNode
from src.bootstrap import BootStrap
import logging
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
        index = 0
        shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node":n} for n in self.root.children], key=itemgetter('distance'))

        # well our queue is not empty we can update the tree! 
        while len(shortesDistances) > 1:
            print("at index "+ str(index) +" num of children in root: " + str(len(shortesDistances)))
            #index % calcdistannceFreq  == 0:
            if not self.root.allChildrenHaveDistances():
                self.root.calcDistances()

            index += 1

            #merge shortest distance
            newNode = TreeNode.mergeNodes(shortesDistances[0]["Node"], self.root)
            # bootStrap = BootStrap(newNode)
            # logging.info(f"Node {newNode.nodeName} reliability(bootstrap score):    {str(bootStrap.support_score)}")
            # print(f"Node {newNode.nodeName} reliability(bootstrap score):    {str(bootStrap.support_score)}")

            shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node": n} for n in self.root.children], key=itemgetter('distance'))
