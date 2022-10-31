import logging
import os

from .rotor_label import RotorLabel
from .rotor_wiring import RotorWiring, Turnover
from enigma_machine.constants import ENGLISH_ALPHABET_SIZE


class Rotor:
    """Represents the internal wiring connects the right side of the rotor (with the spring-loaded contacts) to the
    left side.

    Each rotor is a simple substitution cipher. The letters are listed as connected to alphabet order. If the
    first letter of a rotor is E, this means that the A is wired to the E. This does not mean that E is wired to A;
    such looped wiring is only the case with the reflectors.
    """
    def __init__(self, label: RotorLabel, left_rotor=None, right_rotor=None, position=0, ring=0):
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
        self.__logger = logging.getLogger(Rotor.__name__)

        self.__label = label
        self.__position = position - ring
        self.__ring_setting = ring
        self.__left_rotor = left_rotor
        self.__right_rotor = right_rotor
        self.__right_pins = RotorWiring.from_label(RotorLabel.ETW)
        self.__left_pins = RotorWiring.from_label(label)
        self.__notch = None

        if label.turnover:
            self.__logger.debug(f"rotor {label} has a notch, setting up")
            self.__notch = Turnover.from_label(label)
            if self.__ring_setting:
                self.__logger.debug("right pins in place, overwriting notch")
                self.__notch = self.__right_pins[self.__right_pins.index(self.__notch) - ring]

    @staticmethod
    def from_label(label: RotorLabel):
        return Rotor(label)

    @property
    def label(self):
        return self.__label

    @property
    def right_rotor(self):
        return self.__right_rotor

    @right_rotor.setter
    def right_rotor(self, right_rotor):
        self.__right_rotor = right_rotor

    @property
    def left_rotor(self):
        return self.__left_rotor

    @left_rotor.setter
    def left_rotor(self, left_rotor):
        self.__left_rotor = left_rotor

    @property
    def position(self) -> int:
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def wiring(self):
        return self.__left_pins

    @wiring.setter
    def wiring(self, value):
        self.__left_pins = value

    def get_relative_position(self):
        return self.__position % ENGLISH_ALPHABET_SIZE

    def encode_left_to_right(self, character) -> str:
        """Character to go through right of the rotor
        :param character:   Input character to be encoded.
        :return:            Encoded character
        """
        self.__logger.debug(f"encoding character={character}, left to right")
        self.__logger.debug(f"current position={self.__position}")

        offset = self.__position
        if self.__left_rotor:
            self.__logger.debug("left rotor in place, overwriting offset")
            offset -= self.__left_rotor.get_relative_position()

        input_pin = (self.__right_pins.index(character) + offset) % ENGLISH_ALPHABET_SIZE
        pin_index = self.__left_pins.index(self.__right_pins[input_pin])

        self.__logger.debug(f"input pin is {input_pin}")
        self.__logger.debug(f"pin index is {pin_index}")
        self.__logger.debug(f"return encoded result {self.__right_pins[pin_index]}")

        return self.__right_pins[pin_index]

    def encode_right_to_left(self, character) -> str:
        """Character to go through right of the rotor
        :param character:   Input character to be encoded.
        :return:            Encoded character
        """
        self.__logger.debug(f"encoding character={character}, right to left")
        self.__logger.debug(f"current position={self.__position}")

        offset = self.__position
        if self.__right_rotor:
            self.__logger.debug("right rotor in place, overwriting offset")
            offset -= self.__right_rotor.get_relative_position()

        input_pin = (self.__right_pins.index(character) + offset) % ENGLISH_ALPHABET_SIZE

        self.__logger.debug(f"input pin is {input_pin}")
        self.__logger.debug(f"return encoded result {self.__left_pins[input_pin]}")

        return self.__left_pins[input_pin]

    def rotate(self):
        """Rotate the rotor one notch
        :return: Boolean so rotor to left will also rotate
        """
        self.__logger.debug(f"current position is position={self.__position}")
        self.__logger.debug("rotate, position will be incremented +1")

        rotate_left = self.is_in_notch_position()

        self.__position += 1
        self.__position %= ENGLISH_ALPHABET_SIZE

        self.__logger.debug(f"current position is position={self.__position}")

        return rotate_left

    def is_rotor_reflector(self) -> bool:
        self.__logger.debug("check if rotor is reflector")
        return self.__left_rotor is None

    def is_in_notch_position(self) -> int:
        self.__logger.debug("check if rotor is in notch position")
        return self.__right_pins[self.__position] == self.__notch

    def __str__(self):
        return self.__label.name
