import unittest
import random
import string

from enigma_machine import PlugLead
from enigma_machine.components import Plugboard
from enigma_machine.exceptions import TooManyPlugs, PlugAlreadyInUse


class PlugboardTestCase(unittest.TestCase):

    @staticmethod
    def __random_pair():
        return ''.join(random.sample(string.ascii_uppercase, 2))

    def test_add_successfully(self):
        plugboard = Plugboard()
        plugboard.add(PlugLead("AG"))

        self.assertEqual(plugboard.encode("A"), "G")
        self.assertEqual(plugboard.encode("G"), "A")
        self.assertEqual(plugboard.encode("D"), "D")

    def test_encode_successfully(self):
        plugboard = Plugboard()
        plugboard.add(PlugLead("AG"))

        self.assertEqual(plugboard.encode("A"), "G")
        self.assertEqual(plugboard.encode("G"), "A")
        self.assertEqual(plugboard.encode("D"), "D")

    def test_decode_successfully(self):
        plugboard = Plugboard()
        plugboard.add(PlugLead("AI"))

        self.assertEqual(plugboard.decode("A"), "I")
        self.assertEqual(plugboard.decode("I"), "A")
        self.assertEqual(plugboard.decode("E"), "E")

    def test_raise_exception_too_many_plugs(self):
        leads = []
        board = Plugboard()

        while len(leads) < 10:
            try:
                lead = PlugLead(PlugboardTestCase.__random_pair())
                board.add(lead)
                leads.append(lead)
            except PlugAlreadyInUse:
                pass

        lead = PlugLead(PlugboardTestCase.__random_pair())
        leads.append(lead)

        self.assertRaises(TooManyPlugs, board.add, lead)
        self.assertRaises(TooManyPlugs, Plugboard, leads)

    def test_raise_exception_plug_already_in_use(self):
        plugboard = Plugboard()
        plug = PlugLead("AI")
        plugboard.add(plug)

        self.assertRaises(PlugAlreadyInUse, plugboard.add, plug)


if __name__ == '__main__':
    unittest.main()
