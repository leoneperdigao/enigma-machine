import logging
import os

from enigma_machine.exceptions import InvalidLead


class PlugLead:
    """
    Represents an Enigma Machine plug lead.

    Each lead in the enigma_machine machine connects two plugs in the plugboard.
    It takes a string of length two, which represents the two characters this lead should connect.
    Leads are reversible.

    Example:
        * lead = PlugLead("AG") creates a lead which connects A to G.
        * PlugLead("AG") is equivalent to PlugLead("GA")
    """

    def __init__(self, mapping: str) -> None:
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
        self.__logger = logging.getLogger(PlugLead.__name__)

        self.__connection = tuple(mapping)
        self.__validate_mapping()

    @property
    def plug_one(self) -> str:
        return self.__connection[0]

    @property
    def plug_two(self) -> str:
        return self.__connection[1]

    def encode(self, character: str) -> str:
        """
        Encode a character so that a letter will be swapped this replicates the lead.
        :param character:
        :return:
        """
        if self.plug_one == character:
            return self.plug_two

        if self.plug_two == character:
            return self.plug_one

        return character

    def decode(self, character) -> str:
        """
        Decode a character so that a letter will be swapped this replicates the lead.
        Equivalent to encode.
        :param character:
        :return:
        """
        return self.encode(character)

    def __validate_mapping(self) -> None:
        self.__logger.debug(f"validating mapping connection={self.__connection}")

        if len(self.__connection) != 2:
            raise InvalidLead(f"Invalid lead. It is required a string of length two, which represents the two "
                              f"characters this lead should "
                              f"connect. Actual: {len(self.__connection)}")

        if self.plug_one == self.plug_two:
            raise InvalidLead("Invalid lead. Unable to connect plug to itself.")

    def __str__(self) -> str:
        return f"{self.__connection[0]}{self.__connection[1]}"
