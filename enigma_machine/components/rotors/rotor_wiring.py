import typing

from .rotor_label import RotorLabel
from enigma_machine.constants import ENGLISH_ALPHABET


class RotorWiring(dict):
    _CONFIG: typing.Optional[dict] = None

    def __setitem__(self, k, v):
        if RotorLabel.is_rotor(k):
            super().__setitem__(RotorLabel(k), v)
        else:
            raise KeyError(f"Rotor '{k}' is not valid")

    def __getitem__(self, k):
        if isinstance(k, str):
            k = RotorLabel(k.upper())
        return super().__getitem__(k)

    @staticmethod
    def _configure():
        wiring = RotorWiring()
        wiring[RotorLabel.I] = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        wiring[RotorLabel.II] = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
        wiring[RotorLabel.III] = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
        wiring[RotorLabel.ETW] = ENGLISH_ALPHABET

        # Model: M3 Army
        wiring[RotorLabel.IV] = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
        wiring[RotorLabel.V] = "VZBRGITYUPSDNHLXAWMJQOFECK"

        # M3 & M4 Naval (FEB 1942)
        wiring[RotorLabel.VI] = "JPGVOUMFYQBENHZRDKASXLICTW"
        wiring[RotorLabel.VII] = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
        wiring[RotorLabel.VIII] = "FKQHTLXOCBJSPDZRAMEWNIUYGV"

        # Model: M4 R2
        wiring[RotorLabel.BETA] = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
        wiring[RotorLabel.GAMMA] = "FSOKANUERHMBTIYCWLQPZXVGJD"

        # Reflectors
        wiring[RotorLabel.A] = "EJMZALYXVBWFCRQUONTSPIKHGD"
        wiring[RotorLabel.B] = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        wiring[RotorLabel.C] = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

        # Swiss K model
        wiring[RotorLabel.I_K] = "PEZUOHXSCVFMTBGLRINQJWAYDK"
        wiring[RotorLabel.II_K] = "ZOUESYDKFWPCIQXHMVBLGNJRAT"
        wiring[RotorLabel.III_K] = "EHRVXGAOBQUSIMZFLYNWKTPDJC"
        wiring[RotorLabel.UKW_K] = "IMETCGFRAYSQBZXWLHKDVUPOJN"
        wiring[RotorLabel.ETW_K] = "QWERTZUIOASDFGHJKPYXCVBNML"

        RotorWiring._CONFIG = wiring

    @staticmethod
    def from_label(label: RotorLabel) -> str:
        if RotorWiring._CONFIG is None:
            RotorWiring._configure()

        return RotorWiring._CONFIG[label]


class Turnover(dict):
    _CONFIG: typing.Optional[dict] = None

    def __setitem__(self, k, v):
        if RotorLabel.has_notch(k):
            super().__setitem__(RotorLabel(k), v)
        else:
            raise KeyError(f"Turnover '{k}' is not valid")

    def __getitem__(self, k):
        if isinstance(k, str):
            k = RotorLabel(k.upper())
        return super().__getitem__(k)

    @staticmethod
    def _configure():
        wiring = Turnover()
        wiring[RotorLabel.I] = "Q"
        wiring[RotorLabel.II] = "E"
        wiring[RotorLabel.III] = "V"
        wiring[RotorLabel.IV] = "J"
        wiring[RotorLabel.V] = "Z"

        Turnover._CONFIG = wiring

    @staticmethod
    def from_label(label: RotorLabel) -> str:
        if Turnover._CONFIG is None:
            Turnover._configure()

        return Turnover._CONFIG[label]
