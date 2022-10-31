from enigma_machine import EnigmaMachine, EnigmaSetup


class EnigmaProfilingTarget:

    @staticmethod
    def symmetrical_encode():
        input_text = "ARTIFICIALINTELLIGENCE"
        encoded_message = "XABMTXRSXTLZEHCZEJBGUW"
        machine = EnigmaMachine(EnigmaSetup.from_string("I-II-III B 1-1-1 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK"))

        assert machine.encode(input_text, True) == encoded_message
        assert machine.decode(encoded_message) == input_text


if __name__ == '__main__':
    EnigmaProfilingTarget.symmetrical_encode()
