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
def hexapod_set_pivot(self, hexapod, x, y, z):

    pool = self.getPools()[0]
    command = f'self.hexapod.set_pivot({{ "X":{x}, "Y":{y}, "Z":{z} }})'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["name", Type.String, None, "Name of the new coordinate system"],
    ["x", Type.Float, None, "X coordinate of the new coordinate system"],
    ["y", Type.Float, None, "y coordinate of the new coordinate system"],
    ["z", Type.Float, None, "z coordinate of the new coordinate system"],
    ["u", Type.Float, None, "u angle of the new coordinate system"],
    ["v", Type.Float, None, "v angle of the new coordinate system"],
    ["w", Type.Float, None, "w angle of the new coordinate system"],
])
def hexapod_new_coordinate_system(self, hexapod, name, x, y, z, u, v, w):

    pool = self.getPools()[0]
    command = f'self.hexapod.new_coordinate_system("{name}", {{ "X":{x}, "Y":{y}, "Z":{z}, "U":{u}, "V":{v}, "W":{w} }})'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["name", Type.String, None, "Name of the new coordinate system"],
])
def hexapod_enable_coordinate_system(self, hexapod, name):

    pool = self.getPools()[0]
    command = f'self.hexapod.enable_coordinate_system("{name}")'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
])
def hexapod_disable_coordinate_system(self, hexapod):

    pool = self.getPools()[0]
    command = f'self.hexapod.disable_coordinate_system()'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["child1", Type.String, None, "Name of the child1 coordinate system"],
    ["parent", Type.String, None, "Name of the parent coordinate system"],
])
def hexapod_set_1_parent_coordinate_system(self, hexapod, child1, parent):

    pool = self.getPools()[0]
    command = f'self.hexapod.set_parent_coordinate_system(["{child1}"], "{parent}")'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["child1", Type.String, None, "Name of the child1 coordinate system"],
    ["child2", Type.String, None, "Name of the child2 coordinate system"],
    ["parent", Type.String, None, "Name of the parent coordinate system"],
])
def hexapod_set_2_parent_coordinate_system(self, hexapod, child1, child2, parent):

    pool = self.getPools()[0]
    command = f'self.hexapod.set_parent_coordinate_system(["{child1}", "{child2}"], "{parent}")'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")


@macro(interactive=True, param_def = [
    ["hexapod", Type.String, None, "Command receiver hexapod"],
    ["child1", Type.String, None, "Name of the child1 coordinate system"],
    ["child2", Type.String, None, "Name of the child2 coordinate system"],
    ["child3", Type.String, None, "Name of the child3 coordinate system"],
    ["parent", Type.String, None, "Name of the parent coordinate system"],
])
def hexapod_set_3_parent_coordinate_system(self, hexapod, child1, child2, child3, parent):

    pool = self.getPools()[0]
    command = f'self.hexapod.set_parent_coordinate_system(["{child1}", "{child2}", "{child3}"], "{parent}")'
    controller_anser = pool.SendToController([hexapod, command])
    self.output(f"{pool} controller answer: {controller_anser}")