from sardana.pool.controller import MotorController, Type, Description, \
    DefaultValue
from sardana import State
import logging

from sardana.ctrl.pihexapod import PIHexapod

class PIHexapodMotCtrl(MotorController):

    _map_axis = {
        1: 'X',
        2: 'Y',
        3: 'Z',
        4: 'U',
        5: 'V',
        6: 'W',
    }

    # The properties used to connect to the IcePAP motor controller
    ctrl_properties = {
        'Host': {Type: str, Description: 'The host name', DefaultValue: "dlaelcthex01"},
        'Port': {Type: int, Description: 'The port number', DefaultValue: 50000}
    }
    

    def __init__(self, inst, props, *args, **kwargs):
        super().__init__(inst, props, *args, **kwargs)

        self.hexapod = None
        self._motors = {}

    def AddDevice(self, axis):
        if not self._motors:
            self.hexapod = PIHexapod(host=self.Host, port=self.Port)
        
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
            return State.Alarm, f"Error in axis {axis}, {self.hexapod.move_error_msg}\n{self.hexapod.get_axis_status(axis)}", 0
        else:
            if self.hexapod.on_target({self._map_axis[axis]}):
                return State.On, "Hexapod is stopped", 0
            else:
                return State.Moving, "Hexapod is moving", 0
    
    def GetAxisPar(self, axis: int, name: str):
        hexapod = self.hexapod
        name = name.lower()
        if name == "velocity":
            return hexapod.velocity
        elif name == "step_per_unit":
            return self._motor[self._map_axis[axis]]["step_per_unit"]
        else:
            logging.warning(f"HexapodController - GetAxisPar not defined: {self._map_axis[axis]}, {name}")    

    def SetAxisPar(self, axis: int, name: str, value):
        hexapod = self.hexapod
        name = name.lower()
        if name == "velocity":
            hexapod.velocity = value
        else:
            logging.warning(f"HexapodController - SetAxisPar not supported: {self._map_axis[axis]}, {name}, {value}")

    def print_to_cmd(self, p):
        print(f"cosa cosa: {p}")

    def SendToCtrl(self, stream):
        print(f"RECV Command: {stream}")
        r = eval(stream)
        return str(r)