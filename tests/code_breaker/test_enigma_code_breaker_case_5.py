import itertools
import unittest

from enigma_machine import RotorLabel, EnigmaSetup, EnigmaMachine, RotorWiring
from enigma_machine.constants import ENGLISH_ALPHABET
from tests.code_breaker.enigma_code_breaker_base import EnigmaCodeBreakerBase


class EnigmaCodeBreakerTestCase5(EnigmaCodeBreakerBase):

    def setUp(self):
        super().setUp()
        self.code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
        self.crib = "INSTAGRAM, FLICKR, PINTEREST, TUMBLR"  # multiple cribs are tested

        # These values were set after a some debugging and verification of decoded message.
        self.expected_setup = "V-II-IV B 06-18-07 A-J-L UG-IE-PO-NX-WT"
        self.expected_decoded_message = "YOUCANFOLLOWMYDOGONINSTAGRAMATTALESOFHOFFMANN"
        self.expected_reflector_hiring = "PQUHRSLDYXNGOKMABEFZCWVJIT"
        self.modified_reflector = RotorLabel.B

    def test_break_code(self):
        """I later remembered that I had given the tutor permission to use the Enigma machine to solve some codes
        I’d received via email. As for the window, they are just a big fan of parkour, this is always how they
        leave the building. It seems they are stuck on one last code. It came in via email so we suspect it’s just spam,
        probably related to a social media website, but you never know when you’ll find a gem in that kind of stuff.
        The tutor has narrowed the search and found most of the settings, but it seems this code was made with a
        non-standard reflector. Indeed, there was a photo attached to the email along with the code. It appears that
        the sender has taken a standard reflector, cracked it open, and swapped some of the wires – two pairs of wires
        have been modified, by the looks of the dodgy soldering job.
        To be clear, a single wire connects two letters, e.g. mapping A to Y and Y to A.
        The sender has taken two wires (fours pairs of letters), e.g. A-Y and H-J, and swapped one of the ends,
        so one option would be H-Y and A-J.
        They did this twice, so they modified eight letters total (they did not swap the same wire more than once).
        In your answer, include what the original reflector was and the modifications.

        * Code: HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX
        * Crib: the name of a social media website/platform
        * Rotors: V II IV
        * Reflector: Unknown and non-standard (see above)
        * Ring settings: 06 18 07
        * Starting positions: AJL
        * Plugboard pairs: UG IE PO NX WT

        Solution strategy:
        Most of the configuration is known, except for the reflector.
        Reflector is not standard, so we need to tweak it.
        Cribs are not known, but we can start by using some known social media that are more popular.
        It was mentioned that a photo was attached in the email, so we can think narrow
        this down to image-based social media. Instagram, perhaps, is a good crib.
        Assertions are added to cover the code break and machine setup.

        :return: None
        """
        self.logger.info("CODE BREAKER CASE 5")

        rotor_config = "V-II-IV"
        ring_settings = "06-18-07"
        starting_positions = "A-J-L"
        plugboard = "UG-IE-PO-NX-WT"
        results = []
        modified_reflector_wiring = None
        modified_reflector = None

        for reflector in RotorLabel.get_reflector_labels():
            muddled_wiring_permutations = EnigmaCodeBreakerTestCase5.__permutate_reflector_wiring(
                RotorWiring.from_label(reflector)
            )
            for muddled_wiring in muddled_wiring_permutations:
                setup = EnigmaSetup.from_string(
                    f"{rotor_config} {reflector.name} {ring_settings} {starting_positions} {plugboard}".upper()
                )
                enigma_machine = EnigmaMachine(setup)
                # override reflector wiring with a hacked one
                enigma_machine.get_reflector().wiring = muddled_wiring
                potential_decoded_message = enigma_machine.encode(self.code)

                # search for crib in message
                result = self.lookup_crib(self.crib, potential_decoded_message, setup)
                if result:
                    modified_reflector = reflector
                    modified_reflector_wiring = muddled_wiring
                    results.append(result)
                    break
            else:
                continue
            break

        # assert the expected reflector modification
        self.assertEqual(self.expected_reflector_hiring, modified_reflector_wiring)
        # assert the reflector modified
        self.assertEqual(self.modified_reflector, modified_reflector)
        # assert rest of the config
        self.assert_variant_results(results)

    @staticmethod
    def __swap_pairs(pair, another_pair):
        """Swaps two wiring pairs and return new combinations
        Given (A,C), (B,E), returns [(A,B), (C,E), (A,E), (C,B)]
        :param pair: wiring pair
        :param another_pair: another wiring pair
        :return: possible swaps
        :return:
        """
        return [
            [(pair[0], another_pair[0]), (pair[1], another_pair[1])],
            [(pair[0], another_pair[1]), (pair[1], another_pair[0])]
        ]

    @staticmethod
    def __wiring_to_pairs(reflector_wiring: str):
        """Covert reflector wiring into pairs, e.g., BADC => (A,B), (C,D)
        :param reflector_wiring: 
        :return: list of wiring pairs
        """
        unique_pairs = set()
        # Leads are symmetric, so AI = IA in the reflector, which means 13 pairs
        # Therefore, need to ensure there are no duplicates
        exclude = set()
        for c in reflector_wiring:
            if not reflector_wiring.index(c) in exclude:
                unique_pairs.add((c, ENGLISH_ALPHABET[reflector_wiring.index(c)]))
                exclude.add(ENGLISH_ALPHABET.index(c))
        return unique_pairs

    @staticmethod
    def __stringify_wiring_pairs(reflector_pairs):
        """Opposite to wiring_to_pairs. Convert wiring pairs wiring string
        :param reflector_pairs:
        :return:
        """
        # considering 13 pairs, thus reflector_pairs * 2 = ENGLISH_ALPHABET_SIZE = 26
        letters = list(ENGLISH_ALPHABET[:len(reflector_pairs) * 2])
        for pair in reflector_pairs:
            i, j = letters.index(pair[0]), letters.index(pair[1])
            letters[i], letters[j] = letters[j], letters[i]

        return "".join(letters)

    @staticmethod
    def __permutate_reflector_wiring(original_wiring: str, r: int = 2):
        """Takes the original wiring and a swap factor and returns its permutations.
        Unlike a regular rotor a reflector has only 13 pairs (so if A is mapped to E, then E is also mapped to A).
        Each swap affects two pairs, e.g. (A,D), (B,C), thus if A is swapped with B then (A,B), (C,D).

        If multiple swaps are required, a single wire can only be swapped once. Two swaps, for example,
        means swapping two wires, which affects four pairs, because a single wire swap affects two pairs.

        Each of these four-pair combinations provides three ways to swap the wires between them (two new ways).
        Only new methods will be returned., e.g. [(A,B),(C,E)] and [(A,E),(C,B)].

        :param original_wiring: original wiring of reflector
        :param r: swap factor, defaults to 2, as stated in the problem
        :return: wiring pairs permutations
        """
        unique_pairs = EnigmaCodeBreakerTestCase5.__wiring_to_pairs(original_wiring)
        result = []
        for pair_combination in list(itertools.combinations(unique_pairs, r * 2)):
            swap_combinations = list(itertools.combinations(pair_combination, 2))
            for selected_pairs in swap_combinations[:int(len(swap_combinations) / 2)]:
                # selected pairs are the two pairs chosen from a set of four, and
                # remaining_two_pairs are the remaining ones.
                remaining_two_pairs = list(set(pair_combination) - set(selected_pairs))
                # swap two pairs in two new ways:
                all_swaps_selected_pairs = EnigmaCodeBreakerTestCase5.__swap_pairs(
                    selected_pairs[0], selected_pairs[1]
                )
                # swap again, but now the remaining pairs:
                all_swaps_remaining_pairs = EnigmaCodeBreakerTestCase5.__swap_pairs(
                    remaining_two_pairs[0], remaining_two_pairs[1]
                )

                # combine swapped wiring pairs
                for i in range(len(all_swaps_selected_pairs)):
                    for j in range(len(all_swaps_remaining_pairs)):
                        chain = itertools.chain(
                            all_swaps_selected_pairs[i] + all_swaps_remaining_pairs[j],
                            (unique_pairs - set(pair_combination))
                        )
                        result.append(list(chain))

        # return permutation, without duplications
        return set([EnigmaCodeBreakerTestCase5.__stringify_wiring_pairs(pair_combo) for pair_combo in result])


if __name__ == '__main__':
    unittest.main()
