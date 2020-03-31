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
            if (self.instruction & 0x00FF) == 0x00E0:
                self.CLS()
            elif 0x00EE:
                self.RET()

        elif (self.instruction & 0xF000) == 0x1000:
            self.JP()

        elif (self.instruction & 0xF000) == 0x2000:
            self.CALL()

        elif (self.instruction & 0xF000) == 0x3000:
            self.SE()

        elif (self.instruction & 0xF000) == 0x4000:
            self.SNE()

        elif (self.instruction & 0xF000) == 0x5000:
            self.SRR()

        elif (self.instruction & 0xF000) == 0x6000:
            self.LOAD()

        elif (self.instruction & 0xF000) == 0x7000:
            self.ADD()

        elif (self.instruction & 0xF000) == 0x8000:
            if (self.instruction & 0x000F) == 0:
                self.LD()
            elif (self.instruction & 0x000F) == 1:
                self.OR()
            elif (self.instruction & 0x000F) == 2:
                self.AND()
            elif (self.instruction & 0x000F) == 3:
                self.XOR()
            elif (self.instruction & 0x000F) == 4:
                self.ADD_2()
            elif (self.instruction & 0x000F) == 5:
                self.SUB()
            elif (self.instruction & 0x000F) == 6:
                self.SHR()
            elif (self.instruction & 0x000F) == 7:
                self.SUBN()
            elif (self.instruction & 0x000F) == E:
                self.SHL()

        elif (self.instruction & 0xF000) == 0x9000:
            self.SNE_2()

        elif (self.instruction & 0xF000) == 0xA000:
            self.LOAD_I()

        elif (self.instruction & 0xF000) == 0xB000:
            self.JP_2()

        elif (self.instruction & 0xF000) == 0xC000:
            self.RND()

        elif (self.instruction & 0xF000) == 0xD000:
            self.DRW()

        elif (self.instruction & 0xF000) == 0xE000:
            if (self.instruction & 0x00FF) == 9E:
                self.SKP()
            elif (self.instruction & 0x00FF) == A1:
                self.SKNP()

        elif (self.instruction & 0xF000) == 0xF000:
            if (self.instruction & 0x00FF) == 07:
                self.LD_DT()
            elif (self.instruction & 0x00FF) == 0A:
                self.LD_K()
            elif (self.instruction & 0x00FF) == 15:
                self.LD_DT_2()
            elif (self.instruction & 0x00FF) == 18:
                self.LD_ST()
            elif (self.instruction & 0x00FF) == 1E:
                self.ADD_I()
            elif (self.instruction & 0x00FF) == 29:
                self.LD_F()
            elif (self.instruction & 0x00FF) == 33:
                self.LD_B()
            elif (self.instruction & 0x00FF) == 55:
                self.LD_I()
            elif (self.instruction & 0x00FF) == 65:
                self.LD_I_2()


    # OpCode Functions

    # 0nnn
    def notDefined(self):
        '''
        0nnn - SYS addr
        Jump to a machine code routine at nnn.

        This instruction is only used on the old computers on which Chip-8 was originally implemented. It is ignored by modern interpreters.
        '''

        print('Error.  instruction has not been implemented.')
        print('instruction: ', format(self.instruction, '04x'))
        sys.exit()


    # 2nnn
    def CALL(self):
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
    def LOAD(self):
        '''
        6xkk - LD Vx, byte
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8
        self.V[x] = kk
        self.pc += 2


    # Annn
    def LOAD_I(self):
        '''
        Set I = nnn.

        The value of register I is set to nnn.
        '''

        nnn = self.instruction & 0x0FFF
        self.I = nnn
        self.pc += 2


    # Dxyn
    def DRW(self):
        '''
        Dxyn - DRW Vx, Vy, nibble
        Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

        The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen at coordinates (Vx, Vy).
        Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is positioned so
        part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen. See instruction 8xy3 for more information on XOR,
        and section 2.4, Display, for more information on the Chip-8 screen and sprites.
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
                        self.V[0xF] = 1
                    self.gpu_memory.graphics_memory[gpuByte] ^= 1       # XOR the byte to update the pixel.
        self.draw_flag = True                                           # Enable the draw flag to instruct the sysytem to draw the above data to screen.
        self.pc += 2


    # 00E0
    def CLS(self):
        '''
        00E0 - CLS
        Clear the display.
        '''

        for i in range(len(self.gpu_memory.graphics_memory)):
            self.gpu_memory.graphics_memory[i] == 0
        self.draw_flag = True
        self.pc += 2


    # 00EE
    def RET(self):
        '''
        00EE - RET
        Return from a subroutine.

        The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
        '''

        self.pc = self.stack.pop()


    # 1nnn
    def JP(self):
        '''
        1nnn - JP addr
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        '''

        nnn = self.instruction & 0x0FFF
        self.pc = nnn


    # 3xkk
    def SE(self):
        '''
        3xkk - SE Vx, byte
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8

        if self.V[x] == kk:
            self.pc += 2


    # 4xkk
    def SNE(self):
        '''
        4xkk - SNE Vx, byte
        Skip next instruction if Vx != kk.

        The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8

        if self.V[x] != kk:
            self.pc += 2


    # 5xy0
    def SRR(self):
        '''
        5xy0 - SE Vx, Vy
        Skip next instruction if Vx = Vy.

        The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] == self.V[y]:
            self.pc += 2


    # 7xkk
    def ADD(self):
        '''
        7xkk - ADD Vx, byte
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then stores the result in Vx.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8
        self.V[x] += kk
        self.pc += 2


    # 8xy0
    def LD(self):
        '''
        8xy0 - LD Vx, Vy
        Set Vx = Vy.

        Stores the value of register Vy in register Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4
        self.V[x] = self.V[y]
        self.pc += 2


    # 8xy1
    def OR(self):
        '''
        8xy1 - OR Vx, Vy
        Set Vx = Vx OR Vy.

        Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. A bitwise OR compares the corrseponding bits from two values,
        and if either bit is 1, then the same bit in the result is also 1. Otherwise, it is 0.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4
        self.V[x] = self.V[x] | self.V[y]
        self.pc += 2


    # 8xy2
    def AND(self):
        '''
        8xy2 - AND Vx, Vy
        Set Vx = Vx AND Vy.

        Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx. A bitwise AND compares the corrseponding bits from two values,
        and if both bits are 1, then the same bit in the result is also 1. Otherwise, it is 0.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4
        self.V[x] = self.V[x] & self.V[y]
        self.pc += 2


    # 8xy3
    def XOR(self):
        '''
        8xy3 - XOR Vx, Vy
        Set Vx = Vx XOR Vy.

        Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx. An exclusive OR compares the corrseponding bits from two values,
        and if the bits are not both the same, then the corresponding bit in the result is set to 1. Otherwise, it is 0.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4
        self.V[x] = self.V[x] ^ self.V[y]
        self.pc += 2


    # 8xy4
    def ADD_2(self):
        '''
        8xy4 - ADD Vx, Vy
        Set Vx = Vx + Vy, set VF = carry.

        The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] + self.V[y] > 255:
            self.V[F] = 1
        else:
            self.V[F] = 0

        self.V[x] = self.V[x] + self.V[y]
        self.pc += 2


    # 8xy5
    def SUB(self):
        '''
        8xy5 - SUB Vx, Vy
        Set Vx = Vx - Vy, set VF = NOT borrow.

        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] > self.V[y]:
            self.V[F] = 1
        else:
            self.V[F] = 0

        self.V[x] = self.V[x] - self.V[y]
        self.pc += 2


    # 8xy6
    def SHR(self):
        '''
        8xy6 - SHR Vx {, Vy}
        Set Vx = Vx SHR 1.

        If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4
        # How to do this?
        self.V[x] / 2
        self.pc += 2


    # 8xy7
    def SUBN(self):
        '''
        8xy7 - SUBN Vx, Vy
        Set Vx = Vy - Vx, set VF = NOT borrow.

        If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[y] > self.V[x]:
            self.V[F] = 1
        else:
            self.V[F] = 0

        self.V[x] = self.V[y] - self.V[x]
        self.pc += 2


    # 8xyE
    def SHL(self):
        '''
        8xyE - SHL Vx {, Vy}
        Set Vx = Vx SHL 1.

        If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4
        # How to do this?
        self.V[x] * 2
        self.pc += 2


    # 9xy0
    def SNE_2(self):
        '''
        9xy0 - SNE Vx, Vy
        Skip next instruction if Vx != Vy.

        The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] != self.V[y]:
            self.pc += 2


    # Bnnn
    def JP_2(self):
        '''
        Bnnn - JP V0, addr
        Jump to location nnn + V0.

        The program counter is set to nnn plus the value of V0.
        '''

        nnn = self.instruction & 0x0FFF
        self.pc = nnn + self.V[0]


    # Cxkk
    def RND(self):
        '''
        Cxkk - RND Vx, byte
        Set Vx = random byte AND kk.

        The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx. See instruction 8xy2 for more information on AND.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8
        # self.V[x] = kk & ##           How to generate a random byte from 0 - 255?
        self.pc += 2


    # Ex9E
    def SKP(self):
        '''
        Ex9E - SKP Vx
        Skip next instruction if key with the value of Vx is pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position, PC is increased by 2.
        '''

        # How to do this?
        self.pc += 2


    # ExA1
    def SKNP(self):
        '''
        ExA1 - SKNP Vx
        Skip next instruction if key with the value of Vx is not pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
        '''

        # How to do this?
        self.pc += 2


    # Fx07
    def LD_DT(self):
        '''
        Fx07 - LD Vx, DT
        Set Vx = delay timer value.

        The value of DT is placed into Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        # V[x] = Delay Timer Value?
        self.pc += 2


    # Fx0A
    def LD_K(self):
        '''
        Fx0A - LD Vx, K
        Wait for a key press, store the value of the key in Vx.

        All execution stops until a key is pressed, then the value of that key is stored in Vx.
        '''

        # How to do this?
        self.pc += 2


    # Fx15
    def LD_DT_2(self):
        '''
        Fx15 - LD DT, Vx
        Set delay timer = Vx.

        DT is set equal to the value of Vx.
        '''

        # How to do this?
        self.pc += 2


    # Fx18
    def LD_ST(self):
        '''
        Fx18 - LD ST, Vx
        Set sound timer = Vx.

        ST is set equal to the value of Vx.
        '''

        # How to do this?
        self.pc += 2


    # Fx1E
    def ADD_I(self):
        '''
        Fx1E - ADD I, Vx
        Set I = I + Vx.

        The values of I and Vx are added, and the results are stored in I.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.I += self.V[x]
        self.pc += 2


    # Fx29
    def LD_F(self):
        '''
        Fx29 - LD F, Vx
        Set I = location of sprite for digit Vx.

        The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.
        '''

        x = (self.instruction & 0x0F00) >> 8
        # self.I = ?
        self.pc += 2


    # Fx33
    def LD_B(self):
        '''
        Fx33 - LD B, Vx
        Store BCD representation of Vx in memory locations I, I+1, and I+2.

        The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        # How to do this?


    # Fx55
    def LD_I(self):
        '''
        Fx55 - LD [I], Vx
        Store registers V0 through Vx in memory starting at location I.

        The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
        '''

        # How to do this?


    # Fx65
    def LD_I_2(self):
        '''
        Fx65 - LD Vx, [I]
        Read registers V0 through Vx from memory starting at location I.

        The interpreter reads values from memory starting at location I into registers V0 through Vx.
        '''

        # How to do this?
