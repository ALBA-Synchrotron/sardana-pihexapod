# Sample3: Test the position property system

from minerva_hexapode import Hexapod
import logging
import os
import time

def main():

    hexapod = Hexapod(host="dlaelcthex01")

    hexapod.x = 1
    time.sleep(0.1)
    hexapod.y = -1
    time.sleep(0.1)
    hexapod.z = 1
    time.sleep(0.1)
    hexapod.u = -1
    time.sleep(0.1)
    hexapod.v = 1
    time.sleep(0.1)
    hexapod.w = -1

    while not hexapod.on_target():
        x = hexapod.x
        time.sleep(0.1)
        y = hexapod.y
        time.sleep(0.1)
        z = hexapod.z
        time.sleep(0.1)
        u = hexapod.u
        time.sleep(0.1)
        v = hexapod.v
        time.sleep(0.1)
        w = hexapod.w
        print('current position is: ', x, y, z, u, v, w)
        time.sleep(1)

    hexapod.x = -1
    hexapod.y = 1
    hexapod.z = -1
    hexapod.u = 1
    hexapod.v = -1
    hexapod.w = 1

    while not hexapod.on_target():
        print('current position is: ', hexapod.x, hexapod.y, hexapod.z, hexapod.u, hexapod.v, hexapod.w)
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("PID: {}".format(os.getpid()))
    main()
