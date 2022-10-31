import itertools
import string
import unittest

from enigma_machine import RotorLabel
from tests.code_breaker.enigma_code_breaker_base import EnigmaCodeBreakerBase


class EnigmaCodeBreakerTestCase4(EnigmaCodeBreakerBase):

    def setUp(self):
        super().setUp()
        self.code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
        self.crib = "TUTOR"

        # These values were set after a some debugging and verification of decoded message.
        self.expected_setup = "V-III-IV A 24-12-10 S-W-U WP-RJ-AT-VF-IK-HN-CG-BS"
        self.expected_decoded_message = "NOTUTORSWEREHARMEDNORIMPLICATEDOFCRIMESDURINGTHEMAKINGOFTHESEEXAMPLES"
        self.expected_qtd_potential_configurations = 9

    def test_break_code(self):
        """On my way home from working late as I walked past the computer science lab I saw one of the tutors
        playing with the Enigma machine. Mere tutors are not allowed to touch such important equipment!
        Suspicious, I open the door, but the tutor hears me, and jumps out of the nearest window.
        They left behind a coded message, but some leads have been pulled out of the machine.
        It might contain a clue, but I’ll have to find the missing lead positions (marked with question marks
        in the settings below).

        * Code: SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW
        * Crib: TUTOR
        * Rotors: V III IV
        * Reflector: A
        * Ring settings: 24 12 10
        * Starting positions: SWU
        * Plugboard pairs: WP RJ A? VF I? HN CG BS

        Solution strategy:
        Most of the configuration is known, except for the plugboard.
        Plugboard are generated considering the missing leads.
        New leads are generated skipping already used leads, as it is known a lead cannot connect to itself

        :return: None
        """
        self.logger.info("CODE BREAKER CASE 4")
        self.possible_rotors = ["V-III-IV"]
        self.possible_reflectors = [RotorLabel.A.name]
        self.possible_ring_settings = ["24-12-10"]
        self.possible_starting_positions = ["S-W-U"]

        incomplete_plugboard = "WP-RJ-A?-VF-I?-HN-CG-BS"

        self.possible_plugboards = self.__generate_plugboards(incomplete_plugboard)

        # due to the small number of variants for this scenario
        # initializing multiprocessing is more expensive (takes more time) than running it serially
        self.assert_variant_results(
            self.check_variants(variants=self.generate_variants(), parallel=True)
        )

    @staticmethod
    def __generate_plugboards(incomplete_plugboard: str):
        """Generate plugboards based upon permuting ASCII uppercase letters
        and filtering them to generate valid plugboards

        :param incomplete_plugboard: plugboard missing leads
        :return: list of possible plugboards
        """
        plugboards = []
        for perm in itertools.permutations(string.ascii_uppercase, 2):
            replacements = 0
            complemented_plugboard = incomplete_plugboard
            if perm[0] not in complemented_plugboard:
                complemented_plugboard = complemented_plugboard.replace("?", perm[0], 1)
                replacements += 1

            if perm[1] not in complemented_plugboard:
                complemented_plugboard = complemented_plugboard.replace("?", perm[1], 1)
                replacements += 1

            if replacements == 2:
                plugboards.append(complemented_plugboard)

        return plugboards


if __name__ == '__main__':
    unittest.main()

