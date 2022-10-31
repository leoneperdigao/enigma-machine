class InvalidEnigmaSetup(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidLead(InvalidEnigmaSetup):
    def __init__(self, message):
        super().__init__(message)


class TooManyPlugs(InvalidEnigmaSetup):
    def __init__(self, message):
        super().__init__(message)


class PlugAlreadyInUse(InvalidEnigmaSetup):
    def __init__(self, message):
        super().__init__(message)


class IncompatibleConfiguration(InvalidEnigmaSetup):
    def __init__(self, message):
        super().__init__(message)
