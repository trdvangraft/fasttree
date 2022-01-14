# from itertools import product
from src.nni import nni_interchange
from src.TreeNode import TreeNode
from src.profile import Profile
from src.TreeCrawler import TreeCrawler
from src.visualize import Visualize

def read_atl(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return {lines[i].strip(">").strip("\n"): lines[i+1].strip("\n") for i in range(0, len(lines), 2)}


if __name__ == "__main__":
    sequences = read_atl("data/test-small.aln")

    root : TreeNode = TreeNode(Profile("A", "root"))

    print(sequences)
    for n in sequences:
        # print(n)
        # print(sequences[n])
        node = TreeNode(Profile(sequences[n], n))
        root.addNode(node)

    root.generateProfileFromChildren()
    # print(root.profile.get_frequency_profile())
    root.calcDistances()

    crawler = TreeCrawler(root)
    crawler.startMerging()

    ## ADD NNI STEP
    # optimal_tree = nni_interchange(root)

    print(root)
    vis = Visualize(root)
    vis.visualize(path="./results/first_tree.png")
