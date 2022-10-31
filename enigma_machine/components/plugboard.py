import logging
import os

from typing import List

from .plug_lead import PlugLead
from enigma_machine.exceptions import TooManyPlugs, PlugAlreadyInUse


class Plugboard:
    """Represents an extension of the Enigma Machine that could connect different letters,
    swapping their values from the keyboard.
    """
    __MAX_PAIRS = 10

    def __init__(self, plugs: List[PlugLead] = []):
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
        self.__logger = logging.getLogger(Plugboard.__name__)

        self.__wiring_pairs = dict()
        self.__add_all(plugs)

    def add(self, lead: PlugLead):
        self.__logger.debug(f"adding lead={lead}")
        self.__logger.debug(f"current wiring mapping is {self.__wiring_pairs}")

        # wiring is mirrored, thus we check the considering 2 connections
        if len(self.__wiring_pairs) + 1 > Plugboard.__MAX_PAIRS * 2:
            raise TooManyPlugs(f"Please specify {Plugboard.__MAX_PAIRS} or less pairs")

        if lead.plug_one not in self.__wiring_pairs and lead.plug_two not in self.__wiring_pairs:
            self.__logger.debug(f"adding lead to wiring mapping")

            self.__wiring_pairs[lead.plug_one] = lead
            self.__wiring_pairs[lead.plug_two] = lead

            self.__logger.debug(f"wiring mapping after addition is {self.__wiring_pairs}")
        else:
            raise PlugAlreadyInUse(f"Plug {lead.plug_one}-{lead.plug_two} is already in use")

    def remove(self, lead: PlugLead):
        self.__logger.debug(f"removing lead={lead}")
        self.__wiring_pairs.pop(lead.plug_one, None)
        self.__wiring_pairs.pop(lead.plug_two, None)

    def encode(self, character):
        self.__logger.debug(f"encoding character={character}")
        if character in self.__wiring_pairs:
            self.__logger.debug(f"character={character} is in wiring_pairs. Returning encoded value.")
            return self.__wiring_pairs.get(character).encode(character)

        self.__logger.debug(f"character={character} is not in wiring_pairs. Returning itself.")
        return character

    def decode(self, character):
        return self.encode(character)

    def __add_all(self, plugs: List[PlugLead]):
        for lead in plugs:
            self.add(lead)

    def __str__(self):
        return str(set("{0}".format(" ".join(str(self.__wiring_pairs[i]) for i in self.__wiring_pairs)).split()))
