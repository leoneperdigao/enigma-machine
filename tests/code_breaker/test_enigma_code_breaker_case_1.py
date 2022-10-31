import unittest

from enigma_machine import RotorLabel
from tests.code_breaker.enigma_code_breaker_base import EnigmaCodeBreakerBase


class EnigmaCodeBreakerTestCase1(EnigmaCodeBreakerBase):

    def setUp(self):
        super().setUp()
        self.code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
        self.crib = "SECRETS"

        # These values were set after a some debugging and verification of decoded message.
        self.expected_setup = "BETA-GAMMA-V C 04-02-14 M-J-M KI-XN-FL"
        self.expected_decoded_message = "NICEWORKYOUVEMANAGEDTODECODETHEFIRSTSECRETSTRING"

    def test_break_code(self):
        """You recovered an Enigma machine! Amazingly, it is set up in that day’s position, ready for you to replicate
        in your software. But unfortunately the label has worn off the reflector. All the other settings are still in
        place, however. You also found a book with the title “SECRETS” which contained the following code,
        could it be so simple that the code contains that text?

        * Code: DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ
        * Crib: SECRETS
        * Rotors: Beta Gamma V
        * Reflector: Unknown
        * Ring settings: 04 02 14
        * Starting positions: MJM
        * Plugboard pairs: KI XN FL

        Solution strategy:
        Most of the config is known, except for the reflector
        Need to test all starting positions until we see if the message contain the crib
        If so, the code stops, and we need to check the message.
        If that makes sense (i.e., readable by humans) a test assertion is added
        """
        self.logger.info("CODE BREAKER CASE 1")

        self.possible_rotors = ["BETA-GAMMA-V"]
        self.possible_reflectors = [ref.name for ref in RotorLabel.get_reflector_labels()]
        self.possible_ring_settings = ["04-02-14"]
        self.possible_starting_positions = ["M-J-M"]
        self.possible_plugboards = ["KI-XN-FL"]

        # due to the small number of variants for this scenario
        # initializing multiprocessing is more expensive (takes more time) than running it serially
        self.assert_variant_results(
            self.check_variants(variants=self.generate_variants(), parallel=False)
        )


if __name__ == '__main__':
    unittest.main()
