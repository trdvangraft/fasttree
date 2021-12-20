# from itertools import product
from src.TreeNode import TreeNode
from src.profile import Profile

def read_atl(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return {lines[i].strip(">").strip("\n"): lines[i+1].strip("\n") for i in range(0, len(lines), 2)}


if __name__ == "__main__":
    sequences = read_atl("data/fasttree-input.aln")

    root : TreeNode = TreeNode(Profile("A"))

    print(sequences)
    for n in sequences:
        # print(n)
        # print(sequences[n])
        node = TreeNode(Profile(sequences[n]))
        root.addNode(node)

    root.generateProfileFromChildren()
    print(root.profile.get_frequency_profile())