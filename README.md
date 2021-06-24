# GcodeParser

A simple gcode parser that takes a string of text and returns a list where each gcode command is seperated into a python object.

The structure of the python object is:

`G1 X10 Y-2.5 ; this is a comment`

```python
GcodeLine(
  command = ('G', 1),
  params = {'X': 10, 'Y': -2.5},
  comment = 'this is a comment',
)
```

# Install

```
pip install gcodeparser
```

Alternatively:

```
pip install -e "git+https://github.com/AndyEveritt/GcodeParser.git@master#egg=gcodeparser"
```

# Usage

```python
from gcodeparser import GcodeParser

# open gcode file and store contents as variable
with open('my_gcode.gcode', 'r') as f:
  gcode = f.read()

GcodeParser(gcode).lines    # get parsed gcode lines
```

## Include Comments

`GcodeParser` takes a second argument called `include_comments` which defaults to `False`. If this is set to `True` then any line from the gcode file which only contains a comment will also be included in the output.

```py
gcode = (
  'G1 X1 ; this comment is always included\n',
  '; this comment will only be included if `include_comments=True`',
)

GcodeParser(gcode, include_comments=True).lines
```

If `include_comments` is `True` then the comment line will be in the form of:

```python
GcodeLine(
  command = (';', None),
  params = {},
  comment = 'this comment will only be included if `include_comments=True`',
)
```

## Converting a File

```python
from gcodeparser import GcodeParser

with open('3DBenchy.gcode', 'r') as f:
    gcode = f.read()
parsed_gcode = GcodeParser(gcode)
parsed_gcode.lines
```

_output:_

```py
[GcodeLine(command=('G', 10), params={'P': 0, 'R': 0, 'S': 0}, comment='sets the standby temperature'),
 GcodeLine(command=('G', 29), params={'S': 1}, comment=''),
 GcodeLine(command=('T', 0), params={}, comment=''),
 GcodeLine(command=('G', 21), params={}, comment='set units to millimeters'),
 GcodeLine(command=('G', 90), params={}, comment='use absolute coordinates'),
 GcodeLine(command=('M', 83), params={}, comment='use relative distances for extrusion'),
 GcodeLine(command=('G', 1), params={'E': -0.6, 'F': 3600.0}, comment=''),
 GcodeLine(command=('G', 1), params={'Z': 0.45, 'F': 7800.0}, comment=''),
 GcodeLine(command=('G', 1), params={'Z': 2.35}, comment=''),
 GcodeLine(command=('G', 1), params={'X': 119.575, 'Y': 89.986}, comment=''),
 GcodeLine(command=('G', 1), params={'Z': 0.45}, comment=''),
 GcodeLine(command=('G', 1), params={'E': 0.6, 'F': 3600.0}, comment=''),
 GcodeLine(command=('G', 1), params={'F': 1800.0}, comment=''),
 GcodeLine(command=('G', 1), params={'X': 120.774, 'Y': 88.783, 'E': 0.17459}, comment=''),
 GcodeLine(command=('G', 1), params={'X': 121.692, 'Y': 88.145, 'E': 0.11492}, comment=''),
 GcodeLine(command=('G', 1), params={'X': 122.7, 'Y': 87.638, 'E': 0.11596}, comment=''),
 GcodeLine(command=('G', 1), params={'X': 123.742, 'Y': 87.285, 'E': 0.11317}, comment=''),
 ...
]
```

## Convert Command Tuple to String

The `GcodeLine`class has a property `command_str` which will return the command tuple as a string. ie `('G', 91)` -> `"G91"`.

## Changing back to Gcode String

The `GcodeLine` class has a property `gcode_str` which will return the equivalent gcode string.

> This was called `to_gcode()` in version 0.0.6 and before.

## Parameters

The `GcodeLine` class has a several helper methods to get and manipulate gcode parameters.

For an example `GcodeLine` `line`:

### Retrieving Params

To retrieve a param, use the method `get_param(param: str, return_type=None, default=None)` which
returns the value of the param if it exists, otherwise it will the `default` value.
If `return_type` is set, the return value will be type cast.

```python
line.get_param('X')
```

### Updating Params

To update a param, use the method `update_param(param: str, value: int | float)`

```python
line.update_param('X', 10)
```

If the param does not exist, it will return `None` else it will return the updated value.

### Deleting Params

To delete a param, use the method `delete_param(param: str)`

```python
line.delete_param('X')
```

## Converting to DataFrames

If for whatever reason you want to convert your list of `GcodeLine` objects into a pandas dataframe, simply use `pd.DataFrame(GcodeParser(gcode).lines)`
