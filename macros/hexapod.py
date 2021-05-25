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