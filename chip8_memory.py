# This is the close blueprint for our Memory Object.


class MMU():
    # Attributes
    def __init__(self):
        self.memory = [0] * 4096    # Multiplies a list with a single entry of 0, 4,096 timesself.
                                    # This will create a larger list with 4,096 zeros in the list.
                                    # This list simulates Chip8's 4K of RAM.

        # Initialize and define fontset = [
                                                0xF0, 0x90, 0x90, 0x90, 0xF0,           # 0 key
                                                0x20, 0x60, 0x20, 0x20, 0x70,           # 1 key
                                                0xF0, 0x10, 0xF0, 0x80, 0xF0,           # 2 key
                                                0xF0, 0x10, 0xF0, 0x10, 0xF0,           # 3 key
                                                0x90, 0x90, 0xF0, 0x10, 0x10,           # 4 key
                                                0xF0, 0x80, 0xF0, 0x10, 0xF0,           # 5 key
                                                0xF0, 0x80, 0xF0, 0x90, 0xF0,           # 6 key
                                                0xF0, 0x10, 0x20, 0x40, 0x40,           # 7 key
                                                0xF0, 0x90, 0xF0, 0x90, 0xF0,           # 8 key
                                                0xF0, 0x90, 0xF0, 0x10, 0xF0,           # 9 key
                                                0xF0, 0x90, 0xF0, 0x90, 0x90,           # A key
                                                0xE0, 0x90, 0xE0, 0x90, 0xE0,           # B key
                                                0xF0, 0x80, 0x80, 0x80, 0xF0,           # C key
                                                0xE0, 0x90, 0x90, 0x90, 0xE0,           # D key
                                                0xF0, 0x80, 0xF0, 0x80, 0xF0,           # E key
                                                0xF0, 0x80, 0xF0, 0x80, 0x80,           # F key
                                            ]

        # Assign fontset to system Memory
        for byte in range(80):
            self.memory[byte] = self.fontset[byte]


    # The functions below define what the Object can DO once created.
    def read(self, address):
        return self.memory[address]


    def write(self, address, value):
        self.memory[address] = value


    def loadROM(self, rom):
        # Loading ROM into Memory
        with open(rom, 'rb') as romDataFile:
            rom_data = romDataFile.read()

            count = 0x0200

            # 2 main types of loops - for loop and while loop.
            for byte in rom_data:                       # For each byte in the rom_data list, do something.
                self.memory[count] = byte
                count += 1                              # Increment the PC register by 1.
