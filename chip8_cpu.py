# This is the class blueprint for our CPU Object.


class CPU():
    # A class is the blueprint for an object.
    # Two main components:
    #   What is has. - attributes
    #   What it can do. - functions

    # Attributes
    def __init__(self):
        # CPU Registers
        self.PC = 0x0200                # Program Counter - Point to the current instruction
                                        # to execute in memory.
    # Functions
