import TreeNode
import heapq

class TreeCrawler:
    #TODO: Test
    epsilon = 0.0001


    root = None
    def __init__(self, root):
        # print("made TreeNode")

        if(not isinstance(root,TreeNode)):
            print("WARNING: prof is not of type Profile")
            return

        self.root = root


    def startMerging(self):
        shortesDistances = []

        for n in self.root.children:
            heapq.heappush(shortesDistances,(n.getFirstDistance(),n))

        while len(shortesDistances) > 1:
            merger = []
            (d,n) = heapq.heappop(shortesDistances)
            merger.append(n)

            next = heapq.heappop(shortesDistances)

            while d + self.epsilon > next[0]:
                merger.append(next[1])
                next = heapq.heappop(shortesDistances)

            nParent = TreeNode.mergeNodes(merger)
            heapq.heappush(shortesDistances,(nParent.getFirstDistance(),nParent))