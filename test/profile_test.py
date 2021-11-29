import profile
import unittest

from src.profile import Profile

class ProfileTest(unittest.TestCase):
    def test_calculate_simple_motif(self):
        profile = Profile("A")
        self.assertDictEqual({
            "A": [1],
            "C": [0],
            "G": [0],
            "T": [0]
        }, profile.get_frequency_profile())

    def test_calculate_complex_motif(self):
        profile = Profile("ACGTAA")
        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 1, 0, 0]
        }, profile.get_frequency_profile())

    def test_combine_profiles(self):
        profile_a = Profile("ACGTAA")
        profile_b = Profile("ACGTAA")
        profile_c = profile_a.combine(profile_b)
        self.assertDictEqual({
            "A": [1, 0, 0, 0, 1, 1],
            "C": [0, 1, 0, 0, 0, 0],
            "G": [0, 0, 1, 0, 0, 0],
            "T": [0, 0, 0, 1, 0, 0]
        }, profile_c.get_frequency_profile())
    
    def test_combine_different_profiles(self):
        profile_a = Profile("ACGT")
        profile_b = Profile("TGCA")
        profile_c = profile_a.combine(profile_b)
        self.assertDictEqual({
            "A": [0.5, 0, 0, 0.5],
            "C": [0, 0.5, 0.5, 0],
            "G": [0, 0.5, 0.5, 0],
            "T": [0.5, 0, 0, 0.5]
        }, profile_c.get_frequency_profile())
    
    def test_profile_with_multiple_motifs(self):
        profile = Profile(["ACGT", "TGCA"])
        self.assertDictEqual({
            "A": [0.5, 0, 0, 0.5],
            "C": [0, 0.5, 0.5, 0],
            "G": [0, 0.5, 0.5, 0],
            "T": [0.5, 0, 0, 0.5]
        }, profile.get_frequency_profile())
