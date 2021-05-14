from cmath import log
from typing import Dict, List, Set
from pipython import GCSDevice, pitools
import os
import logging

def bit_enabled(code: int, pos: int) -> bool:
    return code & (0x01 << pos) != 0

class Hexapod(GCSDevice):

    CONTROLLERNAME = 'C-887'
    REFMODES = 'FRF'

    _map_axis = {
        'X': 1,
        'Y': 2,
        'Z': 3,
        'U': 4,
        'V': 5,
        'W': 6,
    }

    class AxisStatus:
        def __init__(self, code) -> None:
            self.neg_limit_switch = bit_enabled(code, 0)
            self.reference_point_switch = bit_enabled(code, 1)
            self.pos_limit_switch = bit_enabled(code, 2)

            self.error_flag = bit_enabled(code, 8)
            self.servo_mode_on = bit_enabled(code, 12)
            self.in_motion = bit_enabled(code, 13)
            self.det_ref_value = bit_enabled(code, 14)
            self.on_target = bit_enabled(code, 15)

        def __repr__(self) -> str:
            return """{{
                "neg_limit_switch": {},
                "reference_point_switch": {},
                "pos_limit_switch": {},
                "error_flag": {},
                "servo_mode_on": {},
                "in_motion": {},
                "det_ref_value": {},
                "on_target": {},
            }}""".format(self.neg_limit_switch, self.reference_point_switch, self.pos_limit_switch,
                        self.error_flag, self.servo_mode_on, self.in_motion,
                        self.det_ref_value, self.on_target)


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

        self.move_error = False
        self.move_error_msg = None

        logging.info(f"Status: {self.qSRG()}")



    def new_coordinate_system(self, name: str, coords: Dict[str, float]):
        self.KSD(name, coords)

    def set_parent_coordinate_system(self, childs: List[str], parent: str):
        self.KLN(childs, parent)
    
    def enable_coordinate_system(self, name: str):
        self.KEN(name)

    def disable_coordinate_system(self):
        self.KEN(0)

    def move_to(self, pos: Dict[str, float]):
        try:
            self.move_error = False
            self.move_error_msg = None
            self.MOV(pos)
        except Exception as e:
            logging.error(f"Exception ocurred during move_to: {e}")
            self.move_error = True
            self.move_error_msg = e

    def move_relative(self, inc: Dict[str, float]):
        try:
            self.move_error = False
            self.move_error_msg = None
            self.MVR(inc)
        except Exception as e:
            logging.error(f"Exception ocurred during move_relative: {e}")
            self.move_error = True
            self.move_error_msg = e

    def on_target(self, axes: Set[str] = {'X', 'Y', 'Z', 'U', 'V', 'W'}):
        axes_on_target = self.qONT()

        result = True
        for axis in axes:
            result &= axes_on_target[axis]
            if result == False:
                return False
        
        return True

    def set_pivot(self, coords: Dict[str, float]):
        self.SPI(coords)

    def halt(self, axes: Set[str] = {'X', 'Y', 'Z', 'U', 'V', 'W'}):
        self.HLT(axes, noraise=True)

    def stop(self):
        self.STP(noraise=True)

    @property
    def velocity(self):
        return self.qVLS()

    @property.setter
    def set_velocity(self, v: float):
        self.VLS(v)

    @property
    def current_position(self):
        return self.qPOS()

    @property
    def version(self):
        return self.qVER().strip()

    def get_axis_status(self, axis: str):
        return Hexapod.AxisStatus(self.qSRG(axes=axis, registers=1)[axis][1])


def main():

    hexapod = Hexapod()
    pos = {'X': -10, 'Y':-10, 'Z':-3}
    hexapod.move_to(pos)

    while not hexapod.on_target():
        print('current position is: ', hexapod.GetPosStatus())
        print('status:', hexapod.get_axis_status('X'))

    print("done")

    for i in range(1,10):
        hexapod.move_relative({'X': 0.3})
        print('current position is: ', hexapod.GetPosStatus())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    print("PID: {}".format(os.getpid()))
    main()
