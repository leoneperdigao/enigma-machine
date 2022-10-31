import unittest

from enigma_machine import Rotor, RotorLabel


class RotorTestCase(unittest.TestCase):

    def test_rotor_I_encode(self):
        rotor = Rotor.from_label(RotorLabel.I)
        self.assertEqual("E", rotor.encode_right_to_left("A"))
        self.assertEqual("U", rotor.encode_left_to_right("A"))
        self.assertEqual("K", rotor.encode_right_to_left("B"))
        self.assertEqual("W", rotor.encode_left_to_right("B"))
        self.assertEqual("M", rotor.encode_right_to_left("C"))
        self.assertEqual("Y", rotor.encode_left_to_right("C"))

    def test_rotor_II_encode(self):
        rotor = Rotor.from_label(RotorLabel.II)
        self.assertEqual("A", rotor.encode_right_to_left("A"))
        self.assertEqual("A", rotor.encode_left_to_right("A"))
        self.assertEqual("J", rotor.encode_right_to_left("B"))
        self.assertEqual("J", rotor.encode_left_to_right("B"))
        self.assertEqual("D", rotor.encode_right_to_left("C"))
        self.assertEqual("P", rotor.encode_left_to_right("C"))

    def test_rotor_III_encode(self):
        rotor = Rotor.from_label(RotorLabel.III)
        self.assertEqual("B", rotor.encode_right_to_left("A"))
        self.assertEqual("T", rotor.encode_left_to_right("A"))
        self.assertEqual("D", rotor.encode_right_to_left("B"))
        self.assertEqual("A", rotor.encode_left_to_right("B"))
        self.assertEqual("F", rotor.encode_right_to_left("C"))
        self.assertEqual("G", rotor.encode_left_to_right("C"))

    def test_rotor_reflector(self):
        for label in RotorLabel:
            rotor = Rotor(label=label)
            if label in RotorLabel.get_reflector_labels():
                self.assertTrue(rotor.is_rotor_reflector())


if __name__ == '__main__':
    unittest.main()
