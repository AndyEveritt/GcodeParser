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