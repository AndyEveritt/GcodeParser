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

## Converting to DataFrames

If for whatever reason you want to convert your list of `GcodeLine` objects into a pandas dataframe, simply use `pd.DataFrame(GcodeParser(gcode).lines)`
