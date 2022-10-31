import itertools
import logging
import multiprocessing
import os
import time
import typing
import unittest

from enigma_machine import EnigmaMachine, EnigmaSetup


class EnigmaCodeBreakerBase(unittest.TestCase):
    """Represents a base Enigma Code Breaker framework for testing possible setups
    and asserting assumptions.

    This module also configures logging and measure time for all tests.
    """
    def setUp(self):
        logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
        self.logger = logging.getLogger(self.__class__.__name__)

        self.code = None  # the code to be decoded
        self.crib = None  # a clue to be found in the message
        self.expected_setup = None  # the expected setup that is able to decode the message
        self.expected_decoded_message = None  # the expected decoded message
        self.expected_qtd_potential_configurations = 1

        # all possible config variants, for a standard enigma_machine machine
        self.possible_rotors = []
        self.possible_reflectors = []
        self.possible_ring_settings = []
        self.possible_starting_positions = []
        self.possible_plugboards = []

        self.exact_config_found = False
        self.qtd_potential_setups = 0

        self.__start_time = time.time()

    def tearDown(self):
        self.assertTrue(self.exact_config_found)

        self.logger.info(
            "\n------------------------------------------------------------------------\n"
            "#### EXECUTION DETAILS #### \n"
            f"-> Execution time: {(time.time() - self.__start_time):.3f} seconds\n"
            f"-> Potential setups {self.qtd_potential_setups}\n"
            f"-> Expected setup {self.expected_setup}\n"
            f"-> Expected message {self.expected_decoded_message}\n"
            "------------------------------------------------------------------------\n"
        )

    def generate_variants(self) -> list[tuple]:
        """Generates all possible variants.
        It considers the defined instance variables for rotors, reflectors, ring settings,
        starting positions and pluboards.

        :raises: AssertionError if a variant is empty.
        :return: all possible variants
        """
        self.assertFalse(0, len(self.possible_rotors))
        self.assertFalse(0, len(self.possible_reflectors))
        self.assertFalse(0, len(self.possible_ring_settings))
        self.assertFalse(0, len(self.possible_starting_positions))
        self.assertFalse(0, len(self.possible_plugboards))

        variants = list(
            itertools.product(
                self.possible_rotors,
                self.possible_reflectors,
                self.possible_ring_settings,
                self.possible_starting_positions,
                self.possible_plugboards,
            )
        )
        self.logger.info(f"{len(variants)} were generated.")
        return set(variants)

    def check_variants(
            self, variants: list[tuple], parallel: bool = False,
    ) -> list[typing.Optional[tuple[EnigmaSetup, str]]]:
        """Test all provided variants
        :param variants: enigma_machine machine config variants
        :param parallel: a flag to control whether the execution will be serial or parallel
        :return: results (Optional[tuple[EnigmaSetup, str]]) from tests

        Args:
            reflector_wiring_override:
        """
        results = []
        if not parallel:
            self.logger.info("Checking variants sequentially")
            for v, variant in enumerate(variants, start=1):
                self.logger.debug(f"Checking variant {v}:{str(variant)}")
                result = self.check_potential_setup(self.code, self.crib, variant)
                if result:
                    self.logger.debug(f"Potential setup found for variant: {str(result)}")
                    results.append(result)

        else:
            self.logger.info("Checking variants in parallel")
            results = self.__check_variants_in_parallel(variants)

        return results

    def __check_variants_in_parallel(self, variants: typing.List[typing.Tuple]):
        """Run the test of potential setups in parallel
        :param variants:
        :return:
        """
        # Creates a pool of worker processes and offloaded tasks.
        # By default, it takes the available CPU count.
        with multiprocessing.Pool() as pool:
            args = zip(
                itertools.repeat(self.code),  # fixed and known code
                itertools.repeat(self.crib),  # fixed and known crib
                variants,
            )
            # pass collection of iterables to the worker test_potential_setup
            # it blocks until the result is ready.
            # pool.starmap is used so each potential variant is unpacked as arguments.
            results = pool.starmap(self.check_potential_setup, args)

        return list(filter(None, results))

    def assert_variant_results(self, results: typing.List[typing.Optional[tuple[EnigmaSetup, str]]]):
        """Assert all variant results.
        It checks:
            * if an exact EnigmaMachineSetup is present.
            * if the quantity of potential setups is equal to the expected
        :param results: a list of decoding attempts
        :return: None
        :raises AssertionError in case any check does not pass
        """
        assertions = 0
        self.qtd_potential_setups = len(results)
        self.exact_config_found = False
        self.assertEqual(self.expected_qtd_potential_configurations, self.qtd_potential_setups)

        for result in results:
            try:
                assertions += 1
                self.assert_potential_code_break(result)
                self.exact_config_found = True
                break
            except AssertionError:
                continue

        if assertions == self.qtd_potential_setups and not self.exact_config_found:
            raise AssertionError

    def assert_potential_code_break(self, potential_code_break: typing.Optional[tuple[EnigmaSetup, str]]):
        """Given a potential setup, checks the expected message and the expected enigma_machine machine setup
        :param potential_code_break: (typing.Optional[tuple[EnigmaSetup, str]]) a potential setup and message
        :return: None
        """
        setup_as_string = str(potential_code_break[0])
        potential_decoded_message = str(potential_code_break[1])

        self.logger.debug("Asserting potential code break")
        self.logger.debug(f"Setup is {setup_as_string}")
        self.logger.debug(f"Potential decoded message is {potential_decoded_message}")

        self.assertEqual(self.expected_setup, setup_as_string)
        self.assertEqual(self.expected_decoded_message, potential_decoded_message)

    @staticmethod
    def lookup_crib(known_crib: str, potential_decoded_message: str, setup: EnigmaSetup):
        """Verify if one or more cribs are in the potential decoded message
        :param known_crib: one or more cribs separated by comma
        :param potential_decoded_message: a decoded message
        :param setup: an EnigmaMachine setup
        :return:
        """
        if any(crib in potential_decoded_message for crib in known_crib.split(",")):
            return setup, potential_decoded_message
        return None

    @staticmethod
    def check_potential_setup(
            known_code: str, known_crib: str, variant: typing.Tuple,
    ) -> typing.Optional[tuple[EnigmaSetup, str]]:
        """Test a potential setup considering the known code and crib and the variants.
        Those are taken in following order: rotor_config, reflector, ring_config, starting_positions, plugboard

        :param known_code: (str) encoded message
        :param known_crib: (str) a clue to help breaking code
        :param variant: (typing.Tuple) a enigma setup variant
        :return: (EnigmaSetup) setup, (str) potential_decoded_message

        """
        rotor_config = variant[0]
        reflector = variant[1]
        ring_config = variant[2]
        starting_positions = variant[3]
        plugboard = variant[4]

        setup = EnigmaSetup.from_string(
            f"{rotor_config} {reflector} {ring_config} {starting_positions} {plugboard}".upper()
        )
        potential_decoded_message = EnigmaMachine(setup).encode(known_code)

        return EnigmaCodeBreakerBase.lookup_crib(known_crib, potential_decoded_message, setup)
