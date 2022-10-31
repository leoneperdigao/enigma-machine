import logging
import os
from typing import Tuple, Union, List

from enigma_machine.components import Plugboard, PlugLead
from enigma_machine.components.rotors import Rotor, RotorLabel
from enigma_machine.exceptions import InvalidEnigmaSetup, PlugAlreadyInUse, TooManyPlugs

logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
logger = logging.getLogger(__name__)


class EnigmaSetup:
    """The rotor, reflector and plugboard setup of the Enigma machine"""

    def __init__(
            self,
            rotor_labels: Union[
                Tuple[RotorLabel, RotorLabel, RotorLabel], Tuple[RotorLabel, RotorLabel, RotorLabel, RotorLabel]
            ],
            reflector_label: RotorLabel,
            ring_settings: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
            initial_positions: Union[Tuple[str, str, str], Tuple[str, str, str, str]],
            plugs: List[PlugLead],
    ):
        self.__rotor_labels = rotor_labels
        self.__reflector_label = reflector_label
        self.__ring_settings = ring_settings
        self.__initial_positions = initial_positions
        self.__plugs = plugs
        self.__validate_setup()

    @property
    def rotor_labels(self):
        return self.__rotor_labels

    @rotor_labels.setter
    def rotor_labels(self, value):
        self.__rotor_labels = value

    @property
    def reflector_label(self):
        return self.__reflector_label

    @reflector_label.setter
    def reflector_label(self, value: Rotor):
        assert value.__label in [RotorLabel.A, RotorLabel.B, RotorLabel.C]
        self.__reflector_label = value

    @property
    def ring_settings(self):
        return self.__ring_settings

    @ring_settings.setter
    def ring_settings(self, value):
        self.__ring_settings = value

    @property
    def initial_positions(self):
        return self.__initial_positions

    @initial_positions.setter
    def initial_positions(self, value):
        self.__initial_positions = value

    @property
    def plugs(self):
        return self.__plugs

    @plugs.setter
    def plugs(self, value):
        self.__plugs = value

    def __validate_setup(self):
        """Validates Enigma setup
        """
        try:
            Plugboard(self.plugs)
            assert len(self.rotor_labels) == len(self.ring_settings) == len(self.initial_positions)
        except (TooManyPlugs, PlugAlreadyInUse) as ex:
            raise InvalidEnigmaSetup(f"Invalid plugboard configuration. {str(ex)}")
        except AssertionError:
            raise InvalidEnigmaSetup(
                "The number os rotors, rings settings and initial positions, must be the same"
            )

    @classmethod
    def from_string(cls, config_string: str):
        """Set the Enigma from an input string
         A rotors string such as "I-II-III-IV C 01-01-01-01 X-X-X-X AB-CD-EF-GH"
         will be resolved as:
            * Rotors from right to left: IV, III, II, I
            * Reflector: C
            * Rotor positions right to left: X, X, X, X
            * Ring setting right to left: 01, 01, 01, 01
            * Plugboard settings: AB, CD, EF, GH

        :param config_string: (str) an input configuration string
        :return: (EnigmaSetup) instance of the setup class
        """
        try:
            config_parts = config_string.split()
            rotor_labels = []
            parsed_initial_positions = []
            parsed_ring_settings = []
            plugs = []

            logger.debug("extracting config parts")
            # extract rotor labels, positions and ring rotors from the right to the left
            config = zip(
                config_parts[0].split('-')[::-1],
                config_parts[2].split('-')[::-1],
                config_parts[3].split('-')[::-1]
            )
            logger.debug("setting enigma_machine machine properties")
            # iterate over the config and set the enigma_machine machine properties
            for rotor_label, ring_setting, initial_rotor_position in config:
                rotor_labels.append(RotorLabel[rotor_label.upper()])
                parsed_ring_settings.append(int(ring_setting))
                parsed_initial_positions.append(initial_rotor_position)

            logger.debug("verifying if there is a plugboard to consider")
            if len(config_parts) > 4:
                config_plugboard = config_parts[4].replace('-', ' ').split()
            else:
                config_plugboard = []

            if config_plugboard:
                logger.debug("setting up plugboard")
                for pair in config_plugboard:
                    plugs.append(PlugLead(pair))

            logger.debug("validating reflector")
            reflector = RotorLabel[config_parts[1]]
            if reflector not in RotorLabel.get_reflector_labels():
                raise InvalidEnigmaSetup("Invalid reflector. It must be A, B or C")

            return cls(
                rotor_labels=rotor_labels,
                reflector_label=reflector,
                ring_settings=parsed_ring_settings,
                initial_positions=parsed_initial_positions,
                plugs=plugs
            )
        except Exception as ex:
            # in case a more specific exception was generated, re-raise it
            if isinstance(ex, InvalidEnigmaSetup):
                raise ex

            raise InvalidEnigmaSetup(
                "Unable to setup machine with given string configuration. Please check your entry."
            )

    def __str__(self):
        """EnigmaSetup to string
        :return: (str) setup like "I-II-III B 01-01-01 A-A-A"
        """
        return "{0} {1} {2} {3} {4}".format(
            "-".join(r.name for r in self.rotor_labels[::-1]),
            self.reflector_label.name,
            "-".join("{:02d}".format(r) for (r) in self.ring_settings[::-1]),
            "-".join(str(r) for r in self.initial_positions[::-1]),
            "-".join(str(r) for r in self.plugs)
        )
