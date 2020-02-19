# This is the close blueprint for our Memory Object.


class MMU():
    # Attributes
    def __init__(self):
        self.memory = [0] * 4096    # Multiplies a list with a single entry of 0, 4,096 timesself.
                                    # This will create a larger list with 4,096 zeros in the list.
                                    # This list simulates Chip8's 4K of RAM.

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

        for k, v in enumerate(self.memory):
            print(format(k,'03x'), '\t', format(v, '02x'))
