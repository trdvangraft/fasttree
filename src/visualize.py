from io import StringIO

import matplotlib.pyplot as plt
from Bio import Phylo

from src.utils import *


class Visualize:
    def __init__(self, tree, format="newick"):
        self.newick_str = '(' + self.tree_to_newick(tree) + ');'
        self.tree_format = format

        self.tree = self.load_newick_tree()

    def tree_to_newick(self, root: TreeNode):
        """
        Newick format reference: https://evolution.genetics.washington.edu/phylip/newicktree.html
        :param root:
        :return:
        """
        items = []
        for child in root.children:
            res = ''
            dist = internalNodesDistance(root, child)
            if len(child.children) > 0:
                subres = self.tree_to_newick(child)
                if subres != '':
                    res += '(' + subres + '):' + "{:.4f}".format(dist)
            else:
                res += child.nodeName + ':' + "{:.4f}".format(dist)
            items.append(res)
        return ','.join(items)

    def visualize(self, path=None, show=False):
        """
        Visualize reference: https://biopython-tutorial.readthedocs.io/en/latest/notebooks/13%20-%20Phylogenetics%20with%20Bio.Phylo.html
        :return:
        """
        if self.tree is None:
            self.load_newick_tree()
        print(self.tree)
        fig = plt.figure(figsize=(20, 20), dpi=100)
        # alternatively
        # fig.set_size_inches(10, 20)
        axes = fig.add_subplot(1, 1, 1)
        Phylo.draw(self.tree, axes=axes, branch_labels=lambda c: c.branch_length, do_show=show)
        if not show:
            plt.savefig(path, dpi=100)

    def load_newick_tree(self):
        if self.newick_str is None:
            self.tree = None
        else:
            self.tree = Phylo.read(StringIO(self.newick_str), self.tree_format)

    def save_tree(self, path):
        if self.tree is None:
            self.load_newick_tree()
        Phylo.write(self.tree, path, self.tree_format)
