from hexapod import Hexapod

from sardana.pool.controller import MotorController
from sardana import State
import logging

class HexapodController(MotorController):
    def __init__(self, inst, props, *args, **kwargs):
        super(HexapodController, self).__init__(inst, props, *args, **kwargs)

        self.hexapod = Hexapod()

        self._motors = {}

    def AddDevice(self, axis):
        self._motors[axis] = dict(step_per_unit=1.0)

    def DeleteDevice(self, axis):
        del self._motors[axis]

    def ReadOne(self, axis):
        return self.hexapod.current_position[axis]

    def StateOne(self, axis):
        if self.hexapod.move_error:
            return State.Fault, "Hexapod has an error"
        else:
            if self.hexapod.on_target({axis}):
                return State.on, "Hexapod is stopped"
            else:
                return State.Moving, "Hexapod is moving"
    
    def StartOne(self, axis, position):
        self.hexapod.move_to({axis: position})

    def StopOne(self, axis):
        self.hexapod.halt({axis})

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
            return self._motor[axis]["step_per_unit"]

    def SetAxisPar(self, axis, name, value):
        logging.warning(f"HexapodController - SetAxisPar not supported: {axis}, {name}, {value}")