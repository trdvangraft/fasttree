from __future__ import annotations
import math
from typing import List
from itertools import product

from src.utils import *

def hammingDistance(str1, str2):
    return sum([0 if a == b else 1 for a, b in zip(str1, str2)])

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
        new_name = "_".join(["("+self.name+")", "("+profile.name+")"])
        return Profile(new_motifs, new_name)

    def distance(self, profile: Profile):
        number_of_positions = len(self.motifs[0])

        distance = sum(
            [hammingDistance(left_motif, righ_motif) for left_motif, righ_motif in product(self.motifs, profile.motifs)]
        ) / (len(self.motifs) * len(profile.motifs) * number_of_positions)
        denom = sum([self.__weight_profile[i] * profile.__weight_profile[i]
                    for i in range(number_of_positions)])
        top = sum(
            [
                (1 - sum([a * b for a, b in zip(self.get_freq(i), profile.get_freq(i))])) *
                (self.__weight_profile[i] * profile.__weight_profile[i]) 
                for i in range(number_of_positions)
            ]
        )
        return (denom if denom > 0 else 0.01, distance), denom
    
    def log_distance(self, profile: Profile):
        (weight, prof_dist), incorr_weight = self.distance(profile)
        return -.75 * math.log(raw if (raw := 1 - (4/3) * prof_dist) > 0 else 0.00001) 

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