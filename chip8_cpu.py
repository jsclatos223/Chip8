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
        self.pc = 0x0200                # Program Counter - Point to the current instruction
                                        # to execute in memory.
        self.stack = []                 # CPU Stack
        self.sp = 0                     # Stack Point

        # Component Connections
        self.system_memory = 0


    # Functions
    def tick(self):
        # Fetch
        instruction = (self.system_memory.read(self.pc) << 8) | self.system_memory.read(self.pc + 1)
        # print(format(instruction, '04x'))

        # Decode / Execute
        print(format(instruction, '04x'))

        if (instruction & 0xF000) == 0x0000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x1000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x2000:
            self.call(instruction)
        elif (instruction & 0xF000) == 0x3000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x4000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x5000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x6000:
            self.load(instruction)
        elif (instruction & 0xF000) == 0x7000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x8000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0x9000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0xA000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0xB000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0xC000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0xD000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0xE000:
            self.notDefined(instruction)
        elif (instruction & 0xF000) == 0xF000:
            self.notDefined(instruction)
        

    def notDefined(self, instruction):
        print('Error.  Instruction has not been implemented.')
        print('Instruction: ', format(instruction, '04x'))
        sys.exit()


    def call(self, instruction):
        '''
        2nnn - CALL addr
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current PC on the top of the stack.
        The PC is then set to nnn.
        '''

        nnn = instruction & 0x0FFF
        self.sp += 1
        self.stack.append(self.pc)
        self.pc = nnn


    def load(self, instruction):
        '''
        6xkk - LD Vx, byte
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        '''

        kk = instruction & 0x00FF
        x = (instruction & 0x0F00) >> 8
        self.V[x] = kk
        self.pc += 2
