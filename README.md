# Python Hexapode library for PI C-887 Controller

## Requirements

Install GSCD Library for your operating system and install the PIPython library that supports it. This library was tested with `PIPython==1.5`

## Sardana Installation

Locate the path where this package have been installed. Usually in site-pakcages and add the path to the macros to the MacroServer macro path configuration. Do the same with the pool and the controllers.

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

