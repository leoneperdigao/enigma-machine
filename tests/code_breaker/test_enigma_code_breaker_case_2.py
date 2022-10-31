import itertools
import string
import unittest

from enigma_machine import RotorLabel
from tests.code_breaker.enigma_code_breaker_base import EnigmaCodeBreakerBase


class EnigmaCodeBreakerTestCase2(EnigmaCodeBreakerBase):

    def setUp(self):
        super().setUp()
        self.code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
        self.crib = "UNIVERSITY"

        # These values were set after a some debugging and verification of decoded message.
        self.expected_setup = "BETA-I-III B 23-02-10 I-M-G VH-PT-ZG-BJ-EY-FS"
        self.expected_decoded_message = "IHOPEYOUAREENJOYINGTHEUNIVERSITYOFBATHEXPERIENCESOFAR"

    def test_break_code(self):
        """You leave the machine in the hands of the university.
        The team have cracked the day’s settings thanks to some earlier codebreaking, but unfortunately,
        the initial rotor positions are changed for each message.
        For the message below, the team has no idea what the initial settings should be,
        but know the message was addressed to them. Help them out.

        * Code: CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH
        * Crib: UNIVERSITY
        * Rotors: Beta I III
        * Reflector: B
        * Ring settings: 23 02 10
        * Starting positions: Unknown
        * Plugboard pairs: VH PT ZG BJ EY FS

        Solution strategy:
        Most of the config is known, except for the starting positions.
        Need to test all starting positions until we see if the message contain the crib
        If so, the code stops, and we need to check the message.
        If that makes sense (i.e., readable by humans) a test assertion is added.
        """
        self.logger.info("CODE BREAKER CASE 2")

        self.possible_rotors = ["Beta-I-III"]
        self.possible_reflectors = [RotorLabel.B.name]
        self.possible_ring_settings = ["23-02-10"]

        # first generate all possible combinations of starting positions
        potential_starting_positions = itertools.permutations(string.ascii_uppercase, 3)
        self.possible_starting_positions = ["-".join(sp) for sp in potential_starting_positions]

        self.possible_plugboards = ["VH-PT-ZG-BJ-EY-FS"]

        self.assert_variant_results(
            self.check_variants(variants=self.generate_variants(), parallel=True)
        )


if __name__ == '__main__':
    unittest.main()
