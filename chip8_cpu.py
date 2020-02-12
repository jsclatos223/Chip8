# This is the class blueprint for our CPU Object.
import sys      # Functions specific to Python.


class CPU():
    # A class is the blueprint for an object.
    # Two main components:
    #   What is has. - attributes
    #   What it can do. - functions

    # Attributes
    def __init__(self):
        # General Purpose Registers
        self.V = [0] * 16      # Array of General Purpose Registers

        # Special Purpose Registers
        self.pc = 0x0200                # Program Counter - Point to the current self.instruction
                                        # to execute in memory.
        self.stack = []                 # CPU Stack
        self.sp = 0                     # Stack Point
        self.I = 0                      # Index Register - Holds memory addresses

        # Component Connections
        self.system_memory = 0


    # Functions
    def tick(self):
        # Fetch
        self.instruction = (self.system_memory.read(self.pc) << 8) | self.system_memory.read(self.pc + 1)
        # print(format(self.instruction, '04x'))

        # Decode / Execute
        # print(format(self.instruction, '04x'))

        if (self.instruction & 0xF000) == 0x0000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x1000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x2000:
            self.call()
        elif (self.instruction & 0xF000) == 0x3000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x4000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x5000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x6000:
            self.load()
        elif (self.instruction & 0xF000) == 0x7000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x8000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0x9000:
            self.load_I()
        elif (self.instruction & 0xF000) == 0xA000:
            self.load_I()
        elif (self.instruction & 0xF000) == 0xB000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0xC000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0xD000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0xE000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0xF000:
            self.notDefined()


    # 0nnn
    def notDefined(self):
        print('Error.  instruction has not been implemented.')
        print('instruction: ', format(self.instruction, '04x'))
        sys.exit()


    # 2nnn
    def call(self):
        '''
        2nnn - CALL addr
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current PC on the top of the stack.
        The PC is then set to nnn.
        '''

        nnn = self.instruction & 0x0FFF
        self.sp += 1
        self.stack.append(self.pc)
        self.pc = nnn


    # 6xkk
    def load(self):
        '''
        6xkk - LD Vx, byte
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8
        self.V[x] = kk
        self.pc += 2


    # annn
    def load_I(self):
        '''
        Set I = nnn.

        The value of register I is set to nnn.
        '''

        nnn = self.instruction & 0x0FFF
        self.I = nnn
        self.pc += 2
