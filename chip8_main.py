# imports
import os		        # Provides OS level control to Python.
import sys		        # Functions specific to Python.
import chip8_cpu        # Imports the CPU Object class file.
import chip8_memory     # Imports the Memory Object class file.
import chip8_gpu        # Imports the GPU Object class file.
import chip8_events     # Imports the Events Object class file.


os.system('cls')	# Sends the clear command to the command line.


def main(rom, debug):
    # Create main system componenet Objects
    cpu_part = chip8_cpu.CPU()              # Creates a CPU Object from chip8_cpu.py class file.
    memory_part = chip8_memory.MMU()        # Creates a Memory Object from chip*_memory.py class file.
    gpu_part = chip8_gpu.GPU()              # Creates a GPU Object from chip8_gpu.py class file.
    events_part = chip8_events.EVENTS()     # Creates an Events Object from chip8_events.py class file.

    # Connect Chip8 Components
    cpu_part.system_memory = memory_part    # Conenct the CPU to the system memory.

    # Load ROM into memory
    memory_part.loadROM(rom)

    # CPU Execution Loop
    while True:
        cpu_part.tick()                 # 1 Hertz (Hz) of a cpu clock cycle
        # INSERT EVENT CHECK CODE HERE
        # INSERT DRAW GRAPHICS CODE HERE
        # End CPU loop

if __name__ == "__main__":
    if len(sys.argv) == 3:              # Check to see if 3 arguments were entered on the command line.
        main(sys.argv[1], sys.argv[2])
    else:
        print( 'Usage: py chip8_main.py [program file] [Debug: 0 (off), 1 (on)]' )
