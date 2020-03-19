# imports
import os		        # Provides OS level control to Python.
import sys		        # Functions specific to Python.
import chip8_cpu        # Imports the CPU Object class file.
import chip8_memory     # Imports the Memory Object class file.
import chip8_gpu        # Imports the GPU Object class file.
import chip8_events     # Imports the Events Object class file.


os.system('cls')	# Sends the "cls" command to the command line.  On a Mac, "clear" sends the clear command.


def main(rom, debug):
    # Create main system componenet Objects
    cpu_part = chip8_cpu.CPU()              # Creates a CPU Object from chip8_cpu.py class file.
    memory_part = chip8_memory.MMU()        # Creates a Memory Object from chip*_memory.py class file.
    gpu_part = chip8_gpu.GPU()              # Creates a GPU Object from chip8_gpu.py class file.
    events_part = chip8_events.EVENTS()     # Creates an Events Object from chip8_events.py class file.

    # Connect Chip8 Components
    cpu_part.system_memory = memory_part    # Connect the CPU to the system memory.
    cpu_part.gpu_memory = gpu_part          # Connect the CPU to the GPU.
    gpu_part.cpu = cpu_part                 # Connect the GPU to the CPU.

    # Load ROM into memory
    memory_part.loadROM(rom)

    #Turn on the screen
    if debug == '0':# QUESTION:
        gpu_part.screen()

    # CPU Main loop
    # Run an infinite loop of calling the CPU tick() function, returning any results after each "tick",
    # check for any outside events that happened during the "tick", and then draw ay graphics to the screen.
    while True:
        if debug == '1':
            while True:
                # Debug mode initial output
                step = input("\nPress the Enter Key to step to the next Instruction. Press 'q' to quit: ")
                os.system('cls')

                if step == 'q':
                    sys.exit()              # Stops the program

                elif step == '':
                    # Outputs General Purpose Register Data during one individual "tick"
                    cpu_part.tick()
                    print("****************************** CPU Debug Data ******************************")
                    print("General Purpose Register Data")
                    print("V00:", format(cpu_part.V[0], '02x'),"\t", end = "", flush = True)    # flush --> clears the register
                    print("V08:", format(cpu_part.V[8], '02x'))
                    print("V01:", format(cpu_part.V[1], '02x'),"\t", end = "", flush = True)
                    print("V09:", format(cpu_part.V[9], '02x'))
                    print("V02:", format(cpu_part.V[2], '02x'),"\t", end = "", flush = True)
                    print("V10:", format(cpu_part.V[10], '02x'))
                    print("V03:", format(cpu_part.V[3], '02x'),"\t", end = "", flush = True)
                    print("V11:", format(cpu_part.V[11], '02x'))
                    print("V04:", format(cpu_part.V[4], '02x'),"\t", end = "", flush = True)
                    print("V12:", format(cpu_part.V[12], '02x'))
                    print("V05:", format(cpu_part.V[5], '02x'),"\t", end = "", flush = True)
                    print("V13:", format(cpu_part.V[13], '02x'))
                    print("V06:", format(cpu_part.V[6], '02x'),"\t", end = "", flush = True)
                    print("V14:", format(cpu_part.V[14], '02x'))
                    print("V07:", format(cpu_part.V[7], '02x'),"\t", end = "", flush = True)
                    print("V15:", format(cpu_part.V[15], '02x'))

                    # Prints Special Purpose Register Data during one individual "tick"
                    print("\nSpecial Purpose Register Data")

                    # Prints the Program Counter during one individual "tick"
                    print("Program Counter:", format(cpu_part.pc, '04x'))

                    # Prints the Stack Pointer during one individual "tick"
                    print("Stack Pointer:", format(cpu_part.sp, '04x'))

                    # Prints the CPU Stack during one individual "tick"
                    print("CPU Stack:")
                    for i, j in enumerate(cpu_part.stack):      # Remember you can name i, j anything (Cain used k, v).
                        print(i, '\t', format(j, '04x'))

                    # Prints the Current Instruction during one individual "tick"
                    print("\nCurrent Instruction:", format(cpu_part.instruction, '04x'))

                    # Prints data stored in the System Memory during one individual "tick"
                    print("\nSystem Memory: ")
                    # Outputs the Memory Address
                    for i in range(0, 10, 2):                   # Remember you can name i, j anything (Cain used k, v).
                        print("\n", format(cpu_part.pc + i, '04x') + ":", "\t", end = "", flush = True)
                        # Outputs the data stored in Memory Address and Memory Address + 1
                        for j in range(0, 2):
                            if j < 2:
                                print(format(memory_part.read((cpu_part.pc + i) + j), '02x'), "\t", end = "", flush = True)
        else:
            cpu_part.tick()                                     # 1 Hertz (Hz) of a cpu clock cycle
            # INSERT EVENT CHECK CODE HERE

            # INSERT DRAW GRAPHICS CODE HERE
            if cpu_part.draw_flag == True:
                gpu_part.draw_graphics()

            # End CPU loop



if __name__ == "__main__":
    if len(sys.argv) == 3:              # Check to see if 3 arguments were entered on the command line.
        main(sys.argv[1], sys.argv[2])
    else:
        print( 'Usage: py chip8_main.py [program file] [Debug: 0 (off), 1 (on)]' )
