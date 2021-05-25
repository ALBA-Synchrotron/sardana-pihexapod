from sardana.macroserver.macro import macro
from sardana.macroserver.msparameter import Type


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["command", Type.String, None, "Command to send to the hexapod"]
])
def send_to_hexapode(self, hexapod, command):

    pool = self.getPools()[0]
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["x", Type.Float, None, "X coordinate of pivot"],
    ["y", Type.Float, None, "y coordinate of pivot"],
    ["z", Type.Float, None, "z coordinate of pivot"],
    
])
def set_pivot(self, hexapod, x, y, z):

    pool = self.getPools()[0]
    command = f'self.hexapod.set_pivot({{ "X":{x}, "Y":{y}, "Z":{z} }})'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")
