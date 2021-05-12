from cmath import log
from typing import Dict, List, Set
from pipython import GCSDevice, pitools
import os
import logging


def on_target(pidevice, axes: List[str]):
    axes_on_target = pidevice.qONT()

    result = True
    for axis in axes:
        result &= axes_on_target[axis]
        if result == False:
            return False
    
    return True

class Hexapod(GCSDevice):
    CONTROLLERNAME = 'C-887'
    REFMODES = 'FRF'

    def __init__(self, gcsdll='', gateway=None, host="localhost", port=50000):
        super().__init__(self.CONTROLLERNAME, gcsdll=gcsdll, gateway=gateway)
        self.ConnectTCPIP(ipaddress=host, ipport=port)

        logging.info(f"Connected {self.qIDN().strip()}")
        logging.info(f"Version:\n{self.version}")

        logging.info("Initializing connected stages...")
        pitools.startup(self, stages=None, refmodes=self.REFMODES)

        logging.info(f"Connected axes: {self.axes}")

        self.rangemin = self.qTMN()
        self.rangemax = self.qTMX()

        logging.info(f"Min axes range: {self.rangemin}")
        logging.info(f"Max axes range: {self.rangemax}")

    def move_to(self, pos: Dict[str, float]):
        self.MOV(pos)

    def move_relative(self, inc: Dict[str, float]):
        self.MVR(inc)

    def on_target(self, axes: Set[str] = {'X', 'Y', 'Z', 'U', 'V', 'W'}):
        axes_on_target = self.qONT()

        result = True
        for axis in axes:
            result &= axes_on_target[axis]
            if result == False:
                return False
        
        return True


    @property
    def current_position(self):
        return self.qPOS()

    @property
    def version(self):
        return self.qVER().strip()

def main():

    hexapod = Hexapod(host="localhost", port=50000)
    pos = {'X': -10, 'Y':-10, 'Z':-3}
    hexapod.move_to(pos)

    while not hexapod.on_target():
        print('current position is: ', hexapod.GetPosStatus())

    print("done")

    for i in range(1,10):
        hexapod.move_relative({'X': 0.3})
        print('current position is: ', hexapod.GetPosStatus())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("PID: {}".format(os.getpid()))
    main()
