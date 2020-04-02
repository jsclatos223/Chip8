# This is the class blueprint for our CPU Object.
import sys      # Functions specific to Python.
import random   # Imports the random package.
import time     # Imports the time package.


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
        self.pc = 0x0200                # Program Counter - Point to the current self.instruction to execute in memory.
        self.stack = []                 # CPU Stack
        self.sp = -1                    # Stack Point - Initiates as -1 since the stack itself is empty.  ********** CHANGE 4/1/2020.
        self.I = 0                      # Index Register - Holds memory addresses
        self.dt = 0                     # Delay Timer Register.  ********** CHANGE 4/1/2020.
        self.st = 0                     # Sound Timer Register.  ********** CHANGE 4/1/2020.
        self.keys = [0] * 16            # Flags for each of the 16 keyboard keys.  ********** CHANGE 4/1/2020.
        self.t_last - time.time()       # Timing control.  ********** CHANGE 4/1/2020.

        # Component Connections
        self.system_memory = 0          # Connection to system memory.
        self.gpu_memory = 0             # Connection to GPU memory.

        # Draw Flag
        self.instruction = 0x0000       # Track the current CPU instruction.
        self.previous_instruction = 0   # Previously executed CPU instruction.
        self.draw_flag = False          # Draw to screen if instructed.


    # Functions
    def tick(self):
        # Fetch
        self.instruction = (self.system_memory.read(self.pc) << 8) | self.system_memory.read(self.pc + 1)
        self.previous_instruction = self.instruction

        # Decode and Execute
        if (self.instruction & 0xF000) == 0x0000:
            if (self.instruction & 0x00FF) == 0x00E0:
                self.CLS()
            elif (self.instruction & 0x00FF) == 0x00EE::
                self.RET()

        elif (self.instruction & 0xF000) == 0x1000:
            self.JMP()

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
                self.LDXY()
            elif (self.instruction & 0x000F) == 1:
                self.ORXY()
            elif (self.instruction & 0x000F) == 2:
                self.ANDXY()
            elif (self.instruction & 0x000F) == 3:
                self.XORXY()
            elif (self.instruction & 0x000F) == 4:
                self.ADDXY()
            elif (self.instruction & 0x000F) == 5:
                self.SUBXY()
            elif (self.instruction & 0x000F) == 6:
                self.SHR()
            elif (self.instruction & 0x000F) == 7:
                self.SUBN()
            elif (self.instruction & 0x000F) == E:
                self.SHL()

        elif (self.instruction & 0xF000) == 0x9000:
            self.SNER()

        elif (self.instruction & 0xF000) == 0xA000:
            self.LOAD_I()

        elif (self.instruction & 0xF000) == 0xB000:
            self.JMPA()

        elif (self.instruction & 0xF000) == 0xC000:
            self.RND()

        elif (self.instruction & 0xF000) == 0xD000:
            self.DRW()

        elif (self.instruction & 0xF000) == 0xE000:
            if (self.instruction & 0xF0FF) == 0xE09E:
                self.SKP()
            elif (self.instruction & 0xF0FF) == 0xE0A1:
                self.SKNP()

        elif (self.instruction & 0xF000) == 0xF000:
            if (self.instruction & 0xF0FF) == 0xF007:
                self.DTVX()
            elif (self.instruction & 0xF0FF) == 0xF00A:
                self.notDefined()
            elif (self.instruction & 0xF0FF) == 0xF015:
                self.SETDLY()
            elif (self.instruction & 0xF0FF) == 0xF018:
                self.SETST()
            elif (self.instruction & 0xF0FF) == 0xF01E:
                self.ADDIX()
            elif (self.instruction & 0xF0FF) == 0xF029:
                self.LDFONT()
            elif (self.instruction & 0xF0FF) == 0xF033:
                self.BCD()
            elif (self.instruction & 0xF0FF) == 0xF055:
                self.LDIX()
            elif (self.instruction & 0xF0FF) == 0xF065:
                self.READREG()

    # Timing Code
    pytime = time.time()
    if pytime - self.t_last >= 1.0/60:
        if self.dt > 0:
            self.dt -= 1

        if self.st > 0:
            self.st -= 1

        self.t_last = pytime

    # Insert Event Check Code Here


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

        vx = (self.instruction & 0x0F00) >> 8						# The CPU Register that is currently holding the x coordinates.
		vy = (self.instruction & 0x00F0) >> 4						# The CPU Register that is currently holding the y coordinates.
		xcord = self.V[vx] 											# Extract the x value from the CPU instruction.
		ycord = self.V[vy]											# Extract the y value from the CPU instruction.
		height = self.instruction & 0x000F							# The number of bytes that make up the sprite.
		pixel = 0
		self.V[0xF] = 0

		for scanline in range(height):
			pixel = self.system_memory.memory[self.I + scanline]	# Register I holds the memory location of where the sprites exists in memory.
			for column in range(8):									# Check all 8 pixels that make up a single scanline of a sprite.
				gpuMemX = xcord + column							# Get the number of bytes horizontally in GPU memory.
				gpuMemY = (scanline + ycord) * 64					# Get the number of bytes vertically in GPU memory.
				gpuByte = gpuMemX + gpuMemY							# GPU Byte to draw to.
				if pixel & (128 >> column) != 0 and not (scanline + ycord >= 32 or column + xcord >= 64):	# Make sure drawing is completely within boundries.
					if self.gpu_memory.graphics_memory[gpuByte] == 1:
						self.V[0xf] = 1
					self.gpu_memory.graphics_memory[gpuByte] ^= 1	# XOR the byte to update the pixel.

		self.draw_flag = True										# Enable the draw flag to instruct the system to draw the above data to screen.
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
    def JMP(self):
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
    def LDXY(self):
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
    def ORXY(self):
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
    def ANDXY(self):
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
    def XORXY(self):
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
    def ADDXY(self):
        '''
        8xy4 - ADD Vx, Vy
        Set Vx = Vx + Vy, set VF = carry.

        The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] + self.V[y] > 255:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0

        self.V[x] = (self.V[x] + self.V[y]) & 0x00FF
        self.pc += 2


    # 8xy5
    def SUBXY(self):
        '''
        8xy5 - SUB Vx, Vy
        Set Vx = Vx - Vy, set VF = NOT borrow.

        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] > self.V[y]:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0

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

        if (self.V[x] & 0x0F) == 1:                     # If this value is 1, then we are working with an odd number.
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0

        self.V[x] >> 1                                  # Shifting right by 1, divides any number by 2.
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
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0

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

        if (self.V[x] & 0xF0) >> 4 == 1:                # If this value is 1, then we must carry this 1 to the carry register.
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0

        self.V[x] << 1                                  # Shifting left by 1, multiplies any number by 2.
        self.pc += 2


    # 9xy0
    def SNER(self):
        '''
        9xy0 - SNE Vx, Vy
        Skip next instruction if Vx != Vy.

        The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        y = (self.instruction & 0x00F0) >> 4

        if self.V[x] != self.V[y]:
            self.pc += 2
        self.pc += 2


    # Bnnn
    def JMPA(self):
        '''
        Bnnn - JP V0, addr
        Jump to location nnn + V0.

        The program counter is set to nnn plus the value of V0.
        '''

        nnn = self.instruction & 0x0FFF
        self.pc = self.V[0] + nnn


    # Cxkk
    def RND(self):
        '''
        Cxkk - RND Vx, byte
        Set Vx = random byte AND kk.

        The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx. See instruction 8xy2 for more information on AND.
        '''

        kk = self.instruction & 0x00FF
        x = (self.instruction & 0x0F00) >> 8
        rand = random.radiant(0, 255)                             # Generates a random number between 0 and 255.

        self.V[x] = rand & kk
        self.pc += 2


    # Ex9E
    def SKP(self):
        '''
        Ex9E - SKP Vx
        Skip next instruction if key with the value of Vx is pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position, PC is increased by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8

        if self.keys[self.V[x]] == 1:
            self.pc += 2
        self.pc += 2


    # ExA1
    def SKNP(self):
        '''
        ExA1 - SKNP Vx
        Skip next instruction if key with the value of Vx is not pressed.

        Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
        '''

        x = (self.instruction & 0x0F00) >> 8

        if self.keys[self.V[x]] == 0:
            self.pc += 2
        self.pc += 2


    # Fx07
    def DTVX(self):
        '''
        Fx07 - LD Vx, DT
        Set Vx = delay timer value.

        The value of DT is placed into Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.V[x] = self.dt
        self.pc += 2


    # Fx15
    def SETDLY(self):
        '''
        Fx15 - LD DT, Vx
        Set delay timer = Vx.

        DT is set equal to the value of Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.dt -= self.V[x]
        self.pc += 2


    # Fx18
    def SETST(self):
        '''
        Fx18 - LD ST, Vx
        Set sound timer = Vx.

        ST is set equal to the value of Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.st -= self.V[x]
        self.pc += 2


    # Fx1E
    def ADDIX(self):
        '''
        Fx1E - ADD I, Vx
        Set I = I + Vx.

        The values of I and Vx are added, and the results are stored in I.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.I = self.I + self.V[x]
        self.pc += 2


    # Fx29
    def LDFONT(self):
        '''
        Fx29 - LD F, Vx
        Set I = location of sprite for digit Vx.

        The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.I = self.V[x] * 5
        self.pc += 2


    # Fx33
    def BCD(self):
        '''
        Fx33 - LD B, Vx
        Store BCD representation of Vx in memory locations I, I+1, and I+2.

        The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2.
        '''

        x = (self.instruction & 0x0F00) >> 8
        self.system_memory.memory[self.I] = self.V[x] // 100
        self.system_memory.memory[self.I + 1] = (self.V[x] // 10) % 10
        self.system_memory.memory[self.I + 2] = (self.V[x] % 100) % 10
        self.pc += 2


    # Fx55
    def LDIX(self):
        '''
        Fx55 - LD [I], Vx
        Store registers V0 through Vx in memory starting at location I.

        The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
        '''

        x = (self.instruction & 0x0F00) >> 8
        for reg in range(x + 1):
            self.system_memory.memory[self.I + reg] = self.V[reg]
            self.pc += 2


    # Fx65
    def READREG(self):
        '''
        Fx65 - LD Vx, [I]
        Read registers V0 through Vx from memory starting at location I.

        The interpreter reads values from memory starting at location I into registers V0 through Vx.
        '''

        x = (self.instruction & 0x0F00) >> 8
        for reg in range(x + 1):
            self.V[reg] = self.system_memory.memory[self.I + reg]

        self.pc += 2
