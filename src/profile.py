from __future__ import annotations
from typing import List
from itertools import product


class Profile:
    def __init__(self, dna, name) -> None:
        self.name = name
        self.motifs = dna if type(dna) == list else [dna]
        self.__count_profile = self.__calculate_count_profile()

        self.__weight_profile = [1] * len(self.motifs[0])


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
        return [self.__count_profile[key][i] for key in self.__count_profile.keys()]

    def __calculate_count_profile(self) -> dict:
        k = len(self.motifs[0])
        profile = {nucleotide: [0]*k for nucleotide in "ACTG"}
        for i, j in product(range(len(self.motifs)), range(k)):
            profile[self.motifs[i][j]][j] += 1

        return profile

    def __str__(self) -> str:
        pass
