import unittest

from enigma_machine.components import PlugLead
from enigma_machine.exceptions import InvalidLead


class PlugLeadTestCase(unittest.TestCase):

    def test_encode_successfully(self):
        lead = PlugLead("AG")

        self.assertEqual(lead.encode("A"), "G")
        self.assertEqual(lead.encode("G"), "A")
        self.assertEqual(lead.encode("D"), "D")

    def test_decode_successfully(self):
        lead = PlugLead("AI")

        self.assertEqual(lead.decode("A"), "I")
        self.assertEqual(lead.decode("I"), "A")
        self.assertEqual(lead.decode("E"), "E")

    def test_raise_exception_invalid_lead_input_too_long(self):
        self.assertRaises(InvalidLead, PlugLead, "TOA")

    def test_raise_exception_invalid_lead_same_plug(self):
        self.assertRaises(InvalidLead, PlugLead, "AA")


if __name__ == '__main__':
    unittest.main()
