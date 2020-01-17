# This is the close blueprint for our Memory Object.


class MMU():
    # Attributes
    def __init__(self):
        self.memory = [0] * 4096    # Multiplies a list with a single entry of 0, 4,096 timesself.
                                    # This will create a larger list with 4,096 zeros in the list.
                                    # This list simulates Chip8's 4K of RAM.

    # The functions below define what the Object can DO once created.
    def read(self, address):
        return self.memroy[address]

    def write(self, address, value):
        self.memory[address] = value
