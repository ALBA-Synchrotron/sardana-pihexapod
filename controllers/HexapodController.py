from hexapod import Hexapod

from sardana.pool.controller import MotorController
from sardana import State
import logging

class HexapodController(MotorController):

    _map_axis = {
        1: 'X',
        2: 'Y',
        3: 'Z',
        4: 'U',
        5: 'V',
        6: 'W',
    }

    def __init__(self, inst, props, *args, **kwargs):
        super().__init__(inst, props, *args, **kwargs)

        self.hexapod = None
        self._motors = {}

    def AddDevice(self, axis):
        if not self._motors:
            self.hexapod = Hexapod()
        
        self._motors[self._map_axis[axis]] = dict(step_per_unit=1.0)

    def DeleteDevice(self, axis):
        del self._motors[self._map_axis[axis]]

        if not self._motors:
            self.hexapod.close()
            self.hexapod = None

    def ReadOne(self, axis):
        print(f"ReadOne {self._map_axis[axis]}")
        return self.hexapod.current_position[self._map_axis[axis]]

    def PreStartAll(self):
        # clear the local motion information dictionary
        self._moveable_info = {}

    def StartOne(self, axis, position):
        # store information about this axis motion
        self._moveable_info[self._map_axis[axis]] = position

    def StartAll(self):
        print(f"StartAll: {self._moveable_info}")
        return self.hexapod.move_to(self._moveable_info)

    def PreStopAll(self):
        # clear the local motion information dictionary
        self._moveable_info = set()

    def StopOne(self, axis):
        # store information about this axis motion
        self._moveable_info.add(self._map_axis[axis])

    def StopAll(self):
        self.hexapod.halt(self._moveable_info)

    def StateOne(self, axis):
        if self.hexapod.move_error:
            return State.Alarm, "Hexapod has an error", 0
        else:
            if self.hexapod.on_target({self._map_axis[axis]}):
                return State.On, "Hexapod is stopped", 0
            else:
                return State.Moving, "Hexapod is moving", 0
    


    def GetAxisPar(self, axis, name):
        hexapod = self.hexapod
        name = name.lower()
        if name == "acceleration":
            return 7.5
        elif name == "deceleration":
            return 7.5
        elif name == "base_rate":
            return 1
        elif name == "velocity":
            return 10
        elif name == "step_per_unit":
            return self._motor[self._map_axis[axis]]["step_per_unit"]

    def SetAxisPar(self, axis, name, value):
        logging.warning(f"HexapodController - SetAxisPar not supported: {self._map_axis[axis]}, {name}, {value}")