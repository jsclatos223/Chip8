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
        self.gpu_memory = 0

        # Draw Flag
        self.draw_flag = False          # Draw to screen if instructed.


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
            self.DRW()
        elif (self.instruction & 0xF000) == 0xE000:
            self.notDefined()
        elif (self.instruction & 0xF000) == 0xF000:
            self.notDefined()


    # OpCode Functions

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


    # dxyn
    def DRW(self):
        '''
        Dxyn - DRW Vx, Vy, nibble
        Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

        The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen at coordinates (Vx, Vy). Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen. See instruction 8xy3 for more information on XOR, and section 2.4, Display, for more information on the Chip-8 screen and sprites.
        '''

        vx = (self.instruction & 0x0F00) >> 8               # The CPU Register that is currently holding the x coordinates.
        vy = (self.instruction & 0x00F0) >> 4               # The CPU Register that is currently holding the y coordinates.
        xcord = self.V[vx]                                  # Extract the x value from the CPU instruction.
        ycord = self.V[vy]                                  # Extract the y value from the CPU instruction.
        height = self.instruction & 0x000F                  # The number of bytes that make up the sprite.
        pixel = 0
        self.V[0xF] = 0

        for scanline in range(height):
            pixel = self.system_memory.memory[self.I + scanline]        # Register I holds the memory locatiohn of where the sprites exists in memory.
            for column in range(8):                                     # Check all 8 pixels that make up a single scanline of a sprite.
                gpuMemX = xcord + column                                # Get the number of bytes horizontally in the GPU memory.
                gpuMemY = (scanline + ycord) * 64                       # Get the number of bytes vertically in the GPU memory.
                gpuByte = gpuMemX + gpu_memory                          # GPU Byte to draw to.
                if pixel & (128 >> column) != 0 and not (scanline + ycord >= 32 or column + xcord >= 64):   # Make sure drawing is completely within boundaries.
                    if self.gpu_memory.graphics_memory[gpuByte] == 1:
                        self.V[0xf] = 1
                    self.gpu_memory.graphics_memory[gpuByte] ^= 1       # XOR the byte to update the pixel.
        self.draw_flag = True
        # self.pc += 2                                                    # Enable the draw flag to instruct the sysytem to draw the above data to screen.
