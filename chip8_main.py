# imports
import os		        # Provides OS level control to Python.
import sys		        # Functions specific to Python.
import chip8_cpu        # Imports the CPU Object class file.
import chip8_memory     # Imports the Memory Object class file.
import chip8_gpu        # Imports the GPU Object class file.
import chip8_events     # Imports the Events Object class file.


os.system('clear')	# Sends the clear command to the command line.


def main(rom_file, debug_stat):
    # Create main system componenet Objects
    cpu_part = chip8_cpu.CPU()              # Creates a CPU Object from chip8_cpu.py class file.
    memory_part = chip8_memory.MMU()        # Creates a Memory Object from chip*_memory.py class file.
    gpu_part = chip8_gpu.GPU()              # Creates a GPU Object from chip8_gpu.py class file.
    events_part = chip8_events.EVENTS()     # Creates an Events Object from chip8_events.py class file.

    # Loading ROM into Memory
    with open(rom_file, 'rb') as file:
        rom_data = file.read()

        # 2 main types of loops - for loop and while loop.
        for byte in rom_data:                       # For each byte in the rom_data list, do something.
            memory_part.write(cpu_part.PC, byte)
            cpu_part.PC += 1                        # Increment the PC register by 1.

    if debug == '1':
        for address, value in enumerate(memory_part.memory):
            print(format(address, '03x'), '\t', format(value, '02x'))
    else:
        print('Debug disabled')


if __name__ == "__main__":
    if len(sys.argv) == 3:              # Check to see if 3 arguments were entered on the command line.
        rom_file = sys.argv[1]          # File from the ROM
        debug = sys.argv[2]             # Debug argument
        main(rom_file, debug)
    else:
        print( 'Usage: py chip8_main.py [program file] [Debug: 0 (off), 1 (on)]' )
