import copy
import random
import logging
from src.TreeNode import TreeNode
from src.profile import Profile


class BootStrap:
    """
    Traverse the tree, use bootstrap to test the reliability of the specific node
    """
    def __init__(self, node, nums=10):
        # init the bootstrap with default value 100
        self.nBootStraps = nums
        self.node = node
        self.support_score = self.splitSupport()

    def splitSupport(self):
        """
        Computes support for (A,B),(C,D) compared to that for (A,C),(B,D) and (A,D),(B,C)
        Support1 = Support(AB|CD over AC|BD) = d(A,C)+d(B,D)-d(A,B)-d(C,D)
        Support2 = Support(AB|CD over AD|BC) = d(A,D)+d(B,C)-d(A,B)-d(C,D)
        count numbers of (support1 > 0 and support2 > 0) in nBootStraps
        :return:
        """
        if len(self.node.children) < 2:
            return

        profile_a, profile_b, profile_c, profile_d = self.createProfiles()

        nSupport = 0
        a_resample = copy.deepcopy(profile_a)
        b_resample = copy.deepcopy(profile_b)
        c_resample = copy.deepcopy(profile_c)
        d_resample = copy.deepcopy(profile_d)
        for i in range(self.nBootStraps):
            # resample_motifs_c = self.resampleColumns(profile_c.motifs)
            
            a_resample.motifs = self.resampleColumns(profile_a.motifs)

            b_resample.motifs = self.resampleColumns(profile_b.motifs)

            c_resample.motifs = self.resampleColumns(profile_c.motifs)

            d_resample.motifs = self.resampleColumns(profile_d.motifs)

            support_1 = a_resample.log_distance(c_resample) + b_resample.log_distance(d_resample) - \
                        a_resample.log_distance(b_resample) - c_resample.log_distance(d_resample)

            support_2 = a_resample.log_distance(d_resample) + b_resample.log_distance(profile_c) - \
                        a_resample.log_distance(b_resample) - c_resample.log_distance(d_resample)

            # support_1 = a_resample.distance(c_resample)[0][1] + b_resample.distance(d_resample)[0][1] - \
            #             a_resample.distance(b_resample)[0][1] - profile_c.distance(d_resample)[0][1]

            # support_2 = profile_a.distance(d_resample)[0][1] + b_resample.distance(c_resample)[0][1] - \
            #             profile_a.distance(b_resample)[0][1] - c_resample.distance(d_resample)[0][1]
            
            if support_1 > 0  and support_2 > 0:
                nSupport += 1
            logging.info(f"bootstrap iteration {i}, {support_1} - {support_2} - nsupport {nSupport}")
        return nSupport / self.nBootStraps

    def resampleColumns(self, sequences):
        """
        Resample each sequence of node N
        :param sequences: input sequences
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
        Node N with children A, B, parent D and sibling C, grandparent G.
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
        # parent is root node
        if parent.parent == None:
            profile_c = parent.children[(node_idx - 1) % len(children)].profile
            profile_d = parent.children[(node_idx + 1) % len(children)].profile
        else:
            profile_c = parent.children[(node_idx - 1) % len(children)].profile
            profile_d = parent.profile
        return profile_a, profile_b, profile_c, profile_d
