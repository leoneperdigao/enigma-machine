import logging
import os
import re

from enigma_machine.components import Plugboard
from enigma_machine.components.rotors import RotorLabel, Rotor, RotorWiring
from enigma_machine.constants import ENGLISH_ALPHABET_SIZE
from enigma_machine.enigma_setup import EnigmaSetup


class EnigmaMachine:
    """Represents a 3 or 4 rotor Enigma machine.

    The Enigma machine is a cipher device developed and used in the early- to mid-20th century to protect commercial,
    diplomatic, and military communication. It was employed extensively by Nazi Germany during World War II,
    in all branches of the German military. The Enigma machine was considered so secure that it was used to encipher
    the most top-secret messages.

    Read more: https://en.wikipedia.org/wiki/Enigma_machine
    """

    def __init__(self, setup: EnigmaSetup):
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
        self.__logger = logging.getLogger(EnigmaMachine.__name__)

        self.setup = setup
        self.plugboard = Plugboard(self.setup.plugs)
        self.input_ring = RotorWiring.from_label(RotorLabel.ETW)  # connects to the right-most rotor
        self.__set_rotors(zip(setup.rotor_labels, setup.initial_positions, setup.ring_settings))

        self.__logger.debug(f"configuration is {setup}")

    def __set_rotors(self, rotor_config):
        """Set rotor configuration based on EnigmaSetup
        :param rotor_config: (zip(tuple)) a compressed rotor rotors
        """
        self.rotors = []
        for rotor_label, initial_rotor_position, ring_setting in rotor_config:
            rotor = Rotor(
                label=rotor_label,
                position=self.input_ring.index(initial_rotor_position),
                ring=int(ring_setting) - 1  # ring settings should be in 0-25
            )
            self.rotors.append(rotor)

        self.rotors.append(Rotor.from_label(self.setup.reflector_label))  # reflector goes at the end

        # for each of the rotors set its neighbours to the left and to the right
        for rotor_inx in range(len(self.rotors)):
            first = (rotor_inx == 0)
            last = (rotor_inx == len(self.rotors) - 1)
            if not last:
                self.rotors[rotor_inx].left_rotor = self.rotors[rotor_inx + 1]
            if not first:
                self.rotors[rotor_inx].right_rotor = self.rotors[rotor_inx - 1]

    def encode_character(self, character: str, reset_rotors: bool = False):
        """Encode or decode a character through Enigma settings.
        Rotors will not reset by default, to ensure symmetry

        :param character:
        :param reset_rotors: (bool) reset rotors
        :return: decoded or encoded character
        """
        character = character.upper()
        EnigmaMachine.__validate_character(character)
        # swap character if connected in plugboard
        character = self.plugboard.encode(character)
        # rotate all the rotors
        self.__rotate_n_steps(1)
        # pass characters
        for rotor in self.rotors:
            character = rotor.encode_right_to_left(character)

        for rotor in reversed(self.rotors[0:-1]):
            character = rotor.encode_left_to_right(character)

        # calculate offset between last rotor on right and static ring
        inx = self.input_ring.index(character)
        first_rotor_offset = self.rotors[0].get_relative_position() % ENGLISH_ALPHABET_SIZE
        character = self.input_ring[(inx - first_rotor_offset) % ENGLISH_ALPHABET_SIZE]

        if reset_rotors:
            self.reset_rotors()

        # swap the character again if connected in the plugboard by lead.
        return self.plugboard.encode(character)

    def decode_character(self, character: str, reset_rotors: bool = False):
        """Alias to encode_character
        :param character: (str) a character to be encoded
        :param reset_rotors: (bool) reset rotors
        :return: (str) encoded message
        """
        return self.encode_character(character, reset_rotors)

    def encode(self, message: str, reset_rotors: bool = False):
        """ Encode or decode a string. Rotors will not reset by default

        :param message:
        :param reset_rotors: (bool) reset rotors
        :return: decoded or encoded string
        """
        encoded_message = ""
        for c in message:
            encoded_message += str(self.encode_character(c.upper()))

        if reset_rotors:
            self.reset_rotors()

        return encoded_message

    def decode(self, message, reset_rotors: bool = False):
        """Alias to encode
        :param message: (str) a string to be encoded
        :param reset_rotors: (bool) reset rotors
        :return: (str) encoded message
        """
        return self.encode(message, reset_rotors)

    def reset_rotors(self):
        """Set rotor positions back to initial position
        :return:
        """
        for rotor, initial_position in zip(self.rotors[:-1], self.setup.initial_positions):
            rotor.position = self.input_ring.index(initial_position)

    def get_reflector(self):
        return self.rotors[-1]  # get the last rotor

    def set_reflector(self, reflector: Rotor):
        if reflector.label not in RotorLabel.get_reflector_labels():
            raise ValueError("Please provide a valid reflector")
        self.rotors[-1] = reflector

    def __rotate_n_steps(self, n):
        """Position rotors forward n-steps
        In case that encoding/decoding happens at an offset then this can be used
        to adjust the rotor positions.

        :param n: the number of steps to position rotors forward
        :return:
        """
        # rotate the rotors from right to left
        for i in range(n):
            rotate_left_rotor = self.rotors[0].rotate()
            if rotate_left_rotor or self.rotors[1].is_in_notch_position():
                rotate_left_rotor = self.rotors[1].rotate()
                if rotate_left_rotor:
                    self.rotors[2].rotate()

    @staticmethod
    def __validate_character(character) -> None:
        """Make sure the letter is in a-zA-Z.
        :param character:
        """
        if bool(re.compile(r"[^a-zA-Z ]").search(character)) or len(character) != 1:
            raise ValueError("Please provide a letter in a-zA-Z.")

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(
            self.rotors[-1],
            "-".join(str(r) for r in self.rotors[-2::-1]),
            "-".join(str(r.__ring_setting + 1) for (r) in self.rotors[-2::-1]),
            "-".join(str(self.input_ring[r.__position + r.__ring_setting]) for r in self.rotors[-2::-1]),
            self.plugboard)
