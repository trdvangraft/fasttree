from src.TreeNode import TreeNode
from operator import itemgetter


class TreeCrawler:
    epsilon = 0.0

    root = None

    def __init__(self, root):
        # print("made TreeNode")

        if (not isinstance(root, TreeNode)):
            print("WARNING: root is not of type TreeNode")
            return

        self.root = root

    def startMerging(self):
        index = 0
        # Make a list with the shortest distance of each child-node of root
        shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node": n} for n in self.root.children],
                                  key=itemgetter('distance'))

        # While the queue is not empty we can merge 2 nodes
        while len(shortesDistances) > 1:
            print("at index " + str(index) + " num of children in root: " + str(len(shortesDistances)))

            # If a node has no more distances stored we recalculate all distances
            if not self.root.allChildrenHaveDistances():
                self.root.calcDistances()

            index += 1

            # The node with the shortest distance to another node will be merged first
            newNode = TreeNode.mergeNodes(shortesDistances[0]["Node"], self.root)

            # Remake the list of shortest distances
            shortesDistances = sorted([{"distance": n.getFirstDistance(), "Node": n} for n in self.root.children],
                                      key=itemgetter('distance'))
