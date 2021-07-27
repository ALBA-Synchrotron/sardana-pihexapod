from cmath import log
from typing import Dict, List, Set
from pipython import GCSDevice, pitools, gcserror
import os
import logging

def bit_enabled(code: int, pos: int) -> bool:
    return code & (0x01 << pos) != 0

class Hexapod(GCSDevice):
    """
    All the axis are printed in the specified system units. By default milimeters
    for X, Y, Z axis and degrees for U, V, W. 
    """

    CONTROLLERNAME = 'C-887'
    REFMODES = 'FRF'

    _map_axis = {
        'X': 1,
        'Y': 2,
        'Z': 3,
        'U': 4,
        'V': 5,
        'W': 6,
        1: 'X',
        2: 'Y',
        3: 'Z',
        4: 'U',
        5: 'V',
        6: 'W'
    }

    class Position:
        def __init__(self, position, units) -> None:
            self.x = position['X']
            self.y = position['Y']
            self.z = position['Z']
            self.u = position['U']
            self.v = position['V']
            self.w = position['W']

            self.units_x = units['X']
            self.units_y = units['Y']
            self.units_z = units['Z']
            self.units_u = units['U']
            self.units_v = units['V']
            self.units_w = units['W']
        
        def __repr__(self) -> str:
            return f"""{{"X": {self.x}{self.units_x}, "Y": {self.y}{self.units_y}, "Z": {self.z}{self.units_z}, "U": {self.u}{self.units_u}, "V": {self.v}{self.units_v}, "W": {self.w}{self.units_w} }}"""

            
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

        self.start_up()

        logging.info(f"Connected axes: {self.axes}")

        self.rangemin = self.qTMN()
        self.rangemax = self.qTMX()

        logging.info(f"Min axes range: {self.rangemin}")
        logging.info(f"Max axes range: {self.rangemax}")

        self.move_error = False
        self.move_error_msg = None

        logging.info(f"Status: {self.qSRG()}")

    def __del__(self):
        self.CloseConnection()

    def start_up(self):
        logging.info("Initializing connected stages...")
        
        initialized = False
        max_attemps = 5
        while not initialized and max_attemps > 0:
            try:
                pitools.startup(self, stages=None, refmodes=self.REFMODES)
                initialized = True
            except gcserror.GCSError as ex:
                max_attemps -= 1
                logging.warn(ex)
                if max_attemps == 0:
                    raise ex


    def new_coordinate_system(self, name: str, coords: Dict[str, float]):
        self.KSD(name, coords)

    def set_parent_coordinate_system(self, childs: str, parent: str):
        self.KLN(childs, parent)
    
    def enable_coordinate_system(self, name: str):
        self.KEN(name)

    def get_enabled_coordinate_system(self):
        return self.qKEN()

    def disable_coordinate_system(self):
        self.KEN(0)

    def remove_coordinate_system(self, name: str):
        self.KRM(name)

    def move_to(self, pos: Dict[str, float]):
        """
            Is not a blocking method.
        """
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

    def current_position(self):
        return self.qPOS()

    def current_units(self):
        return self.qPUN()

    @property
    def velocity(self):
        return self.qVLS()

    @velocity.setter
    def set_velocity(self, value: float):
        self.VLS(value)

    @property
    def version(self):
        return self.qVER().strip()

    def get_axis_status(self, axis: str):
        return Hexapod.AxisStatus(self.qSRG()[str(self._map_axis[axis])][1])

    def is_referenced(self, axes: Set[str] = {'X', 'Y', 'Z', 'U', 'V', 'W'}):
        return self.FRF(axes)

    @property
    def position(self):
        return self.Position(self.current_position(), self.current_units())

    @property
    def x(self):
        return self.current_position()['X']

    @x.setter
    def x(self, value):
        self.move_to({"X": value})

    @property
    def y(self):
        return self.current_position()['Y']

    @y.setter
    def y(self, value):
        self.move_to({"Y": value})

    @property
    def z(self):
        return self.current_position()['Z']

    @z.setter
    def z(self, value):
        self.move_to({"Z": value})

    @property
    def u(self):
        return self.current_position()['U']

    @u.setter
    def u(self, value):
        self.move_to({"U": value})

    @property
    def v(self):
        return self.current_position()['V']

    @v.setter
    def v(self, value):
        self.move_to({"V": value})

    @property
    def w(self):
        return self.current_position()['W']

    @w.setter
    def w(self, value):
        self.move_to({"W": value})
