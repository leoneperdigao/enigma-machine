import unittest

from enigma_machine import EnigmaSetup, EnigmaMachine


class EnigmaMachineTestCase(unittest.TestCase):
    def test_multiple_rotor(self):
        self.assertEqual(
            EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z")).encode_character('A'), 'U'
        )
        self.assertEqual(
            EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-A")).encode_character('A'), 'B'
        )
        self.assertEqual(
            EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 Q-E-V")).encode_character('A'), 'L'
        )
        self.assertEqual(
            EnigmaMachine(EnigmaSetup.from_string("IV-V-Beta B 14-9-24 A-A-A")).encode_character('H'), 'Y'
        )
        self.assertEqual(
            EnigmaMachine(EnigmaSetup.from_string("I-II-III-IV C 7-11-15-19 Q-E-V-Z")).encode_character('Z'), 'V'
        )

    def test_default_asymmetric_character_encoding(self):
        machine_a_to_u = EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z"))
        self.assertEqual(machine_a_to_u.encode_character("T"), "F")
        self.assertEqual(machine_a_to_u.encode_character("T"), "O")

        machine_a_to_u.reset_rotors()

        self.assertEqual(machine_a_to_u.encode_character("A"), "U")
        self.assertEqual(machine_a_to_u.encode_character("A"), "B")

    def test_default_asymmetric_encoding(self):
        input_text = "ARTIFICIALINTELLIGENCE"
        encoded_message = "XABMTXRSXTLZEHCZEJBGUW"
        machine = EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"))

        self.assertEqual(machine.encode(input_text), encoded_message)
        self.assertEqual(machine.encode(encoded_message), "FUESPUQLUJIPCSUHQLVNER")

    def test_symmetric_encoding(self):
        hello_world = "HELLOWORLD"
        encoded_message = "RFKTMBXVVW"
        machine = EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"))

        self.assertEqual(machine.encode(hello_world, True), encoded_message)
        self.assertEqual(machine.decode(encoded_message, True), hello_world)

    def test_reset_rotors(self):
        input_text = "THISISARESETTEST"
        machine = EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"))
        positions_before_reset = []
        positions_after_reset = []

        for r in machine.rotors:
            positions_before_reset.append(r.position)

        self.assertEqual(machine.encode(input_text), "FKQCRELVWGXOEHOU")

        machine.reset_rotors()

        for r in machine.rotors:
            positions_after_reset.append(r.position)

        self.assertEqual(positions_before_reset, positions_after_reset)


if __name__ == '__main__':
    unittest.main()
