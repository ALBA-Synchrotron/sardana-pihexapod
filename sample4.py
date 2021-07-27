# Sample4: Test reconnection

from minerva_hexapod import Hexapod
import logging
import os

def main():

    hexapod = Hexapod(host="dlaelcthex01")
    hexapod.move_to({'X': 0, 'Y':0, 'Z':0, 'U': 0, 'V':0, 'W':0})

    while not hexapod.on_target():
        print('current position is: ', hexapod.position)
    print("done")

    # Test Reconnection to the hexapod
    hexapod = None
    hexapod = Hexapod(host="dlaelcthex01")

    hexapod.y = 1
    while not hexapod.on_target():
        print('current position is: ', hexapod.y)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("PID: {}".format(os.getpid()))
    main()
