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
