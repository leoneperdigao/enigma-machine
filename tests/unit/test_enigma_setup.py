import unittest

from enigma_machine import EnigmaSetup, RotorLabel
from enigma_machine.exceptions import InvalidEnigmaSetup


class EnigmaSetupTestCase(unittest.TestCase):

    def test_from_string_without_plugboard(self):
        enigma_setup = EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z")
        self._common_assertions(enigma_setup)
        self.assertEqual([], enigma_setup.plugs)

    def test_from_string_with_plugboard(self):
        enigma_setup = EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK")
        self._common_assertions(enigma_setup)
        self.assertEqual(
            ["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"], [str(plug) for plug in enigma_setup.plugs]
        )

    def _common_assertions(self, enigma_setup):
        self.assertIsInstance(enigma_setup, EnigmaSetup)
        self.assertEqual(RotorLabel.B, enigma_setup.reflector_label)
        self.assertEqual([RotorLabel.III, RotorLabel.II, RotorLabel.I], enigma_setup.rotor_labels)
        self.assertEqual([1, 1, 1], enigma_setup.ring_settings)
        self.assertEqual(["Z", "A", "A"], enigma_setup.initial_positions)

    def test_invalid_rotor(self):
        self.assertRaises(
            InvalidEnigmaSetup, EnigmaSetup.from_string, "I-II-3213 B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"
        )

    def test_invalid_reflector(self):
        self.assertRaises(
            InvalidEnigmaSetup, EnigmaSetup.from_string, "I-II-III X 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"
        )

    def test_invalid_ring_settings(self):
        self.assertRaises(
            InvalidEnigmaSetup, EnigmaSetup.from_string, "I-II-III X -1--1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"
        )

    def test_invalid_starting_positions(self):
        self.assertRaises(
            InvalidEnigmaSetup, EnigmaSetup.from_string, "I-II-III X 1-1-1 %-%-& HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"
        )

    def test_invalid_plugboard(self):
        self.assertRaises(
            InvalidEnigmaSetup, EnigmaSetup.from_string, "I-II-III X 1-1-1 %-%-& HL-MO-MO-CX-BZ-SR-NI-YW-DG-PK"
        )

    def test_too_many_parts(self):
        self.assertRaises(
            InvalidEnigmaSetup, EnigmaSetup.from_string, "I-II-III X 1-1-1 %-%-& HL-MO-MO-CX-BZ-SR-NI-YW-DG-PK TOO MUCH"
        )


if __name__ == '__main__':
    unittest.main()
