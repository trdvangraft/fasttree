from __future__ import annotations
from typing import List
from itertools import product


class Profile:
    def __init__(self, dna, name) -> None:
        self.name = name
        self.motifs = dna if type(dna) == list else [dna]
        self.__count_profile, self.__weight_profile = self.__calculate_count_profile()


    def get_frequency_profile(self) -> dict:
        return {symbol: [count / len(self.motifs) for count in self.__count_profile[symbol]] for symbol in self.__count_profile}

    def get_motifs(self) -> List[str]:
        return self.motifs

    def combine(self, profile: Profile) -> Profile:
        new_motifs = self.motifs + profile.motifs
        new_name = "_".join([self.name, profile.name])
        return Profile(new_motifs, new_name)

    def distance(self, profile: Profile):

        number_of_positions = len(self.motifs[0])

        denom = sum([self.__weight_profile[i] * profile.__weight_profile[i]
                    for i in range(number_of_positions)])
        top = sum([(1 - sum([a * b for a, b in zip(self.get_freq(i), profile.get_freq(i))])) *
                  (self.__weight_profile[i] * profile.__weight_profile[i]) for i in range(number_of_positions)])
        return (denom if denom > 0 else 0.01, top/denom if denom > 0 else 1), denom

    def get_freq(self, i):
        count = [self.__count_profile[key][i] for key in self.__count_profile.keys()]
        freq = [x / sum(count) for x in count]
        return freq

    def __calculate_count_profile(self) -> dict:
        k = len(self.motifs[0])
        n_motifs = len(self.motifs)
        profile = {nucleotide: [0]*k for nucleotide in "ACTG"}
        weights = [0] * k
        for i, j in product(range(len(self.motifs)), range(k)):
            if self.motifs[i][j] == '-':
                # initialize weights for leave nodes
                # the proportion of non-gaps in the profile at each position
                weights[j] += 1
            else:
                profile[self.motifs[i][j]][j] += 1

        return profile, [1 - x/n_motifs for x in weights]

    def get_weights(self):
        return self.__weight_profile

    def __str__(self) -> str:
        pass
