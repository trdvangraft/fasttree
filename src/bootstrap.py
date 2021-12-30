import copy
import random
from src.TreeNode import TreeNode
from src.profile import Profile


class BootStrap:
    """
    Traverse the tree, for each node, use bootstrap to test the reliability
    """
    def __init__(self, node, nums=100):
        # init the bootstrap with default value 100
        self.nBootStraps = nums
        self.node = node
        self.support_score = self.splitSupport()

    def splitSupport(self):
        """
        Computes support for (A,B),(C,D) compared to that for (A,C),(B,D) and (A,D),(B,C)
        Support1 = Support(AB|CD over AC|BD) = d(A,C)+d(B,D)-d(A,B)-d(C,D)
        Support2 = Support(AB|CD over AD|BC) = d(A,D)+d(B,C)-d(A,B)-d(C,D)
        count numbers of  support1 > 0 and support2 > 0 in nBootStraps
        :return:
        """
        if len(self.node.children) < 2:
            return

        profile_a, profile_b, profile_c, profile_d = self.createProfiles()

        nSupport = 0
        for i in range(self.nBootStraps):
            resample_motifs_c = self.resampleColumns(profile_c.motifs)
            profile_c.motifs = resample_motifs_c
            support_1 = profile_a.distance(profile_c)[0][1] + profile_b.distance(profile_d)[0][1] - \
                        profile_a.distance(profile_b)[0][1] - profile_c.distance(profile_d)[0][1]

            support_2 = profile_a.distance(profile_d)[0][1] + profile_b.distance(profile_c)[0][1] - \
                        profile_a.distance(profile_b)[0][1] - profile_c.distance(profile_d)[0][1]

            if support_1 > 0 and support_2 > 0:
                nSupport += 1
        return nSupport / self.nBootStraps

    def resampleColumns(self, sequences):
        """
        Resample each sequence of node N
        :param sequences:
        :return:
        """
        resample_sequences = []
        for sequence in sequences:
            re_sequence = list(copy.deepcopy(sequence))
            for idx in range(len(sequence)):
                resample_pos = random.randint(0, len(sequence) - 1)
                re_sequence[idx] = sequence[resample_pos]
            resample_sequences.append("".join(re_sequence))
        return resample_sequences

    def createProfiles(self):
        """
        Node n with children A, B, parent D and sibling C, grandparent G.
        Find the profiles of children A, B, C, D, where D is another sibling if D is root node
        :param node:
        :return:
        """
        # create the profile of node A, B, C, D
        profile_a = self.node.children[0].profile
        profile_b = self.node.children[1].profile

        parent = self.node.parent
        children = [child.nodeName for child in parent.children]
        node_idx = children.index(self.node.nodeName)
        if parent.nodeName == "root":
            profile_c = parent.children[(node_idx - 1) % len(children)].profile
            profile_d = parent.children[(node_idx + 1) % len(children)].profile
        else:
            profile_c = parent.children[(node_idx - 1) % len(children)].profile
            profile_d = parent.profile
        return profile_a, profile_b, profile_c, profile_d
