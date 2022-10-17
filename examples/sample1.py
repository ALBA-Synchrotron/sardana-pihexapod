# Sample 1: Example of how to use the main features of the library
from minerva_hexapod import Hexapod
import logging
import os

def main():

    hexapod = Hexapod(host="dlaelcthex01")
    hexapod.move_to({'X': 1, 'Y':0, 'Z':0})

    while not hexapod.on_target():
        print('current position is: ', hexapod.position)
        for axis in hexapod.axes:
            print('status:', hexapod.get_axis_status(axis))
    print("done")

    hexapod.move_relative({'X': 0.5})

    while not hexapod.on_target():
        print('current position is: ', hexapod.position)
    print("done")

    hexapod.new_coordinate_system(
        "pepe", {'X': 0, 'Y': 0, 'Z': 1, 'U': 0, 'V': 0, 'W': 0})
    
    hexapod.new_coordinate_system(
        "maria", {'X': 0, 'Y': 0, 'Z': 0, 'U': 1, 'V': 0, 'W': 0})
 
    hexapod.set_parent_coordinate_system("pepe", "maria")
 
    hexapod.enable_coordinate_system("pepe")
 
    hexapod.move_to({'X': 0, 'Y':1, 'Z':0})
    while not hexapod.on_target():
        print('current position is: ', hexapod.position)
    
    hexapod.disable_coordinate_system()
    hexapod.remove_coordinate_system("pepe")
    hexapod.remove_coordinate_system("maria")
    
    hexapod.move_to({'X': 0, 'Y':0, 'Z':0, 'U': 0, 'V': 0, 'W': 0})

    while not hexapod.on_target():
        print('current position is: ', hexapod.position)
    print("\nAll commands succeded!")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("PID: {}".format(os.getpid()))
    main()
