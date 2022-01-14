from typing import List
import unittest

from src.profile import Profile

class ProfileTest(unittest.TestCase):
    def test_calculate_simple_motif(self):
        profile = Profile("A", "name")
        self.assertDictEqual({
            "A": [1],
            "C": [0],
            "G": [0],
            "T": [0]
        }, profile.get_frequency_profile())

    def test_calculate_complex_motif(self):
        profile = Profile("ACGTAA", "name")
        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 1, 0, 0]
        }, profile.get_frequency_profile())

    def test_combine_profiles(self):
        profile_a = Profile("ACGTAA", "name")
        profile_b = Profile("ACGTAA", "name")
        profile_c = profile_a.combine(profile_b)
        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 1, 0, 0]
        }, profile_c.get_frequency_profile())
    
    def test_combine_different_profiles(self):
        profile_a = Profile("ACGT", "name")
        profile_b = Profile("TGCA", "name")
        profile_c = profile_a.combine(profile_b)
        self.assertDictEqual({
            "A": [0.5, 0, 0, 0.5],
            "C": [0, 0.5, 0.5, 0],
            "G": [0, 0.5, 0.5, 0],
            "T": [0.5, 0, 0, 0.5]
        }, profile_c.get_frequency_profile())
    
    def test_profile_with_multiple_motifs(self):
        profile = Profile(["ACGT", "TGCA"], "name")
        self.assertDictEqual({
            "A": [0.5, 0, 0, 0.5],
            "C": [0, 0.5, 0.5, 0],
            "G": [0, 0.5, 0.5, 0],
            "T": [0.5, 0, 0, 0.5]
        }, profile.get_frequency_profile())

    
    def test_distance_between_profiles_works(self):
        profile_a, profile_b, profile_c = self.__node_factory(["AAA", "AAA", "TTT"])

        self.assertTrue(profile_a.log_distance(profile_b) < profile_a.log_distance(profile_c))
        self.assertEqual(profile_a.log_distance(profile_b), 1)
        self.assertEqual(profile_a.log_distance(profile_c), 1)

    

    def __node_factory(self, dna_strings: List[str]) -> List[Profile]:
        profiles = [Profile(string, name=string) for string in dna_strings]
        return profiles
