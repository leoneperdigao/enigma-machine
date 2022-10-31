from enum import Enum


class RotorLabel(Enum):
    # Model: Enigma I
    I = "I"
    II = "II"
    III = "III"
    ETW = "ETW"

    # Model: M3 Army
    IV = "IV"
    V = "V"

    # M3 & M4 Naval (FEB 1942)
    VI = "VI"
    VII = "VII"
    VIII = "VIII"

    # Model: M4 R2
    BETA = "BETA"
    GAMMA = "GAMMA"
    A = "A"  # Reflector
    B = "B"  # Reflector
    C = "C"  # Reflector

    # Swiss K model
    I_K = "I_K"
    II_K = "II_K"
    III_K = "III_K"
    UKW_K = "UKW_K"
    ETW_K = "ETW_K"

    @property
    def turnover(self):
        """Return if it should turn over, based on notch rotors
        :return: (bool) if rotor label has a notch
        """
        return RotorLabel.has_notch(self)

    @classmethod
    def get_reflector_labels(cls):
        return [cls.A, cls.B, cls.C]

    @classmethod
    def is_rotor(cls, rotor):
        if isinstance(rotor, cls):
            target = rotor.value
        return target in cls.__members__

    @classmethod
    def has_notch(cls, rotor_label):
        """Checks if rotor label is one of the notch-able ones
        :param rotor_label: the rotor label instance
        :return: (bool) if rotor label has a notch, i.e., I, II, III, IV, V
        """
        return rotor_label in [cls.I, cls.II, cls.III, cls.IV, cls.V]
