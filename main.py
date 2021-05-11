from typing import List
from pipython import GCSDevice, pitools
import os


CONTROLLERNAME = 'C-887'
STAGES = None  # this controller does not need a 'stages' setting
REFMODES = 'FRF'

def on_target(pidevice, axis: List[str]):
    axis_on_target = pidevice.qONT()

    result = True
    for axe in axis:
        result &= axis_on_target[axe]
        if result == False:
            return False
    
    return True


def main():

    pidevice = GCSDevice(CONTROLLERNAME)
    pidevice.ConnectTCPIP(ipaddress='localhost')

    print('connected: {}'.format(pidevice.qIDN().strip()))

    if pidevice.HasqVER():
        print('version info:\n{}'.format(pidevice.qVER().strip()))

    print('initialize connected stages...')
    pitools.startup(pidevice, stages=STAGES, refmodes=REFMODES)

    rangemin = pidevice.qTMN()
    rangemax = pidevice.qTMX()
    curpos = pidevice.qPOS()

    print(f"Rangemin: {rangemin}")
    print(f"Rangemax: {rangemax}")
    print(f"curpos: {curpos}")

    min = {'X': -10, 'Y':-10, 'Z':-3}
    pidevice.MOV(min)
    print("Y on target:", pidevice.qONT())

    while not on_target(pidevice, ['X', 'Y', 'Z']):
        position = pidevice.GetPosStatus()  # query single axis
        print('current position is: ', position)

    pidevice.close()
    print('done')

if __name__ == '__main__':
    # To see what is going on in the background you can remove the following
    # two hashtags. Then debug messages are shown. This can be helpful if
    # there are any issues.

    # import logging
    # logging.basicConfig(level=logging.DEBUG)

    print("PID: {}".format(os.getpid()))
    main()
