# Sample3: Test the position property system

from minerva_hexapode import Hexapod
import logging
import os
import time

def main():

    hexapod = Hexapod(host="dlaelcthex01")
    
    hexapod.move_to({'X': 0, 'Y':0, 'Z':0, 'U': 0, 'V':0, 'W':0})

    while not hexapod.on_target():
        print('current position is: ', hexapod.position)
        #for axis in hexapod.axes:
        #    print('status:', hexapod.get_axis_status(axis))

    print("done")

    t0 = time.time()
    hexapod.y = 1
    while not hexapod.on_target():
        print('current position is: ', hexapod.y)
    t1 = time.time()
    
    print(f"Done in {t1 - t0}s")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("PID: {}".format(os.getpid()))
    main()
