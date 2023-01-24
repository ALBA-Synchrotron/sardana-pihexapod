from sardana.pool.controller import MotorController, Type, Description, \
    DefaultValue
from sardana import State
import logging

from sardana_pihexapod.ctrl.pihexapod import PIHexapod

import time

import argparse


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
        'Host': {
            Type: str,
            Description: 'The host name',
            DefaultValue: "dlaelcthex01"
        },
        'Port': {
            Type: int,
            Description: 'The port number',
            DefaultValue: 50000
        }
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
        return self.hexapod.current_position()[self._map_axis[axis]]

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
            message = f"Error in axis {axis}, {self.hexapod.move_error_msg}\n\
                {self.hexapod.get_axis_status(axis)}"
            return State.Alarm, message, 0
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
            message = f"HexapodController - GetAxisPar not defined: "\
                      f"{self._map_axis[axis]}, {name}"
            logging.warning(message)

    def SetAxisPar(self, axis: int, name: str, value):
        hexapod = self.hexapod
        name = name.lower()
        if name == "velocity":
            hexapod.velocity = value
        else:
            message = f"HexapodController - SetAxisPar not supported: "\
                      f"{self._map_axis[axis]}, {name}, {value}"
            logging.warning(message)

    def print_to_cmd(self, p):
        print(f"cosa cosa: {p}")

    def SendToCtrl(self, stream):
        print(f"RECV Command: {stream}")
        r = eval(stream)
        return str(r)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int, default=50000)
    args = parser.parse_args()

    ctrl = PIHexapodMotCtrl('test', {'Host': args.host, 'Port': args.port})
    ctrl.AddDevice(1)
    ctrl.AddDevice(2)
    ctrl.AddDevice(3)
    ctrl.AddDevice(4)
    ctrl.AddDevice(5)
    ctrl.AddDevice(6)

    axis1 = 3
    position1 = -3
    ctrl.PreStartAll()
    ctrl.StartOne(axis1, position1)
    axis2 = 4
    position2 = -1
    ctrl.StartOne(axis2, position2)
    ctrl.StartAll()

    t0 = time.time()
    print(ctrl.StateAll())
    while ctrl.StateOne(axis1)[0] != State.On:
        ctrl.StateAll()
        time.sleep(0.1)
    print(time.time() - t0)
    print(ctrl.ReadAll())
    print("Axis1: ", axis1, ctrl.ReadOne(axis1))
    print("Axis2: ", axis2, ctrl.ReadOne(axis2))
    return ctrl


if __name__ == '__main__':
    main()
