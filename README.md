# Python hexapod library for PI C-887 Controller

## Requirements

Install PI GSCD Library for your operating system and install the PIPython library that supports it. This library was tested with `PIPython==1.5`

## Installation

Clone this repository:
```
https://git.cells.es/controls/minerva/python_hexapod_core.git
```

Install with pip
```
pip install .
```

### Test

```python
>>> from minerva_hexapod import Hexapod
>>> h = Hexapod(host="dlaelcthex01")
>>> h.axes
['X', 'Y', 'Z', 'U', 'V', 'W']
>>> h.move_to({"X": 1})
>>> h.position
{"X": 0.999997220867mm, "Y": 1.22225325645e-06mm, "Z": 3.03443967969e-08mm, "U": -1.42516686632e-07deg, "V": 8.01359844144e-08deg, "W": 1.2431950165e-07deg }
```

## Add to Sardana
Locate the path where this package have been installed. Usually in site-pakcages and add the path to the macros to the MacroServer macro path configuration. Do the same with the pool and the controllers.

### Controller

For instance:
```
Pool_<ServerName>_<ServerNumber>.put_property({"PoolPath":["<Your controller dir path>"]})

Example:
Pool_lab01_1.put_property({'PoolPath': [r'C:\Users\sunlo\miniconda3\envs\sardana\Lib\site-packages\python_hexapod_core\controllers']})
```

Then create a controller:

```
defctrl HexapodController hexCtrl Host dlaelcthex01
```

Then define the axes:

```
defelem hex_x hexCtrl 1
defelem hex_y hexCtrl 2
defelem hex_z hexCtrl 3
defelem hex_u hexCtrl 4
defelem hex_v hexCtrl 5
defelem hex_w hexCtrl 6
```

For more information look at [Sardana: Adding elements](https://sardana-controls.org/users/adding_elements.html?highlight=poolpath)

### Macros

To install the macros the same procedure have to be done:

```
_MACRO_SERVER.put_property({"MacroPath":["<Your macro dir path>"]})

Example:
_MACRO_SERVER.put_property({'MacroPath': [r'C:\Users\sunlo\miniconda3\envs\sardana\Lib\site-packages\python_hexapod_core\macros']})
```

## Known Issues

The position properties `x, y, z, u, v, w` may provoke a timeout exception if are called too often in a very short period of time like:
```
hexapod.x
hexapod.y
```
or
```
hexapod.x = 1
hexapod.y = -1
```

