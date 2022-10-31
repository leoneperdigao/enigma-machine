import itertools
import unittest

from enigma_machine import RotorLabel, ENGLISH_ALPHABET_SIZE
from tests.code_breaker.enigma_code_breaker_base import EnigmaCodeBreakerBase


class EnigmaCodeBreakerTestCase3(EnigmaCodeBreakerBase):

    def setUp(self):
        super().setUp()
        self.code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
        self.crib = "THOUSANDS"

        # These values were set after a some debugging and verification of decoded message.
        self.expected_setup = "II-GAMMA-IV C 24-08-20 E-M-Y FH-TS-BE-UQ-KD-AL"
        self.expected_decoded_message = "SQUIRRELSPLANTTHOUSANDSOFNEWTREESEACHYEARBYMERELYFORGETTINGWHERETHEYPUTTHEIRACORNS"

    def test_break_code(self):
        """The department has intercepted a message from the admissions team.
        They know it contains the word “THOUSANDS” and they are worried it might relate to how many students are
        arriving next semester. But the admissions team are a bit unusual: they love even numbers, and hate odd numbers.
        You happen to know they will never use an odd-numbered rotor, ruling out I, III, and V.
        They will also never use a ring setting that has even a single odd digit: 02 is allowed but 11 is certainly not,
        and even 12 is banned.

        * Code: ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY
        * Crib: THOUSANDS
        * Rotors: Unknown but restricted (see above)
        * Reflector: Unknown
        * Ring settings: Unknown but restricted (see above)
        * Starting positions: EMY
        * Plugboard pairs: FH TS BE UQ KD AL

        Solution strategy:
        For each possible ring setting, all the supported reflectors are tested.
        Likewise, considering the restricted rotors, all permutations are tested.
        If crib is part of the message, code stops.
        If that makes sense (i.e., readable by humans) a test assertion is added.

        :return: None
        """
        # ring_settings = "??-??-??" let's find out
        # reflector = "?" let's find out

        rotors_possibilities = ["Beta", "Gamma", "II", "IV"]
        # permute all rotors
        rotor_permutations = itertools.permutations(rotors_possibilities, 3)
        # permute all ring settings
        ring_settings_permutations = itertools.permutations(range(1, ENGLISH_ALPHABET_SIZE + 1), 3)

        self.possible_rotors = list("-".join(rotor_config) for rotor_config in rotor_permutations)
        self.possible_reflectors = [ref.name for ref in RotorLabel.get_reflector_labels()]
        self.possible_ring_settings = self.__filter_ring_settings(ring_settings_permutations)
        self.possible_starting_positions = ["E-M-Y"]
        self.possible_plugboards = ["FH-TS-BE-UQ-KD-AL"]

        self.assert_variant_results(
            self.check_variants(variants=self.generate_variants(), parallel=True)
        )

    @staticmethod
    def __filter_ring_settings(ring_settings_permutations):
        """Filter odd ring settings out
        :param ring_settings_permutations: all possible ring settings
        :return: all-even ring settings
        """
        potential_ring_settings = []
        for permutation in ring_settings_permutations:
            even_num_count = 0

            for ring in permutation:
                if ring % 2 == 0:
                    even_num_count += 1

            # check if all are even
            if even_num_count == len(permutation):
                # format and append
                potential_ring_settings.append(
                    '-'.join(["{:02d}".format(num) for num in permutation])
                )

        return potential_ring_settings


if __name__ == '__main__':
    unittest.main()
