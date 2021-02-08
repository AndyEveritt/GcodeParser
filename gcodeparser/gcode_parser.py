from typing import List, Dict, Tuple
from dataclasses import dataclass
import re
from .commands import Commands


@dataclass
class GcodeLine:
    command: Tuple[str, int]
    params: Dict[str, float]
    comment: str

    def __post_init__(self):
        if self.command[0] == 'G' and self.command[1] in (0, 1, 2, 3):
            self.type = Commands.MOVE
        elif self.command[0] == ';':
            self.type = Commands.COMMENT
        elif self.command[0] == 'T':
            self.type = Commands.TOOLCHANGE
        else:
            self.type = Commands.OTHER

    def get_param(self, param, return_type=None, default=None):
        try:
            if return_type is None:
                return self.params[param]
            else:
                return return_type(self.params[param])
        except KeyError:
            return default


class GcodeParser:
    def __init__(self, gcode: str, include_comments=False):
        self.gcode = gcode
        self.lines: List[GcodeLine] = get_lines(self.gcode, include_comments)
        self.include_comments = include_comments


def get_lines(gcode, include_comments=False):
    regex = r'(?!; *.+)(G|M|T|g|m|t)(\d+)(( *(?!G|M|g|m)\w-?\d+\.?\d*)*) *\t*(; *(.*))?|; *(.+)'
    regex_lines = re.findall(regex, gcode)
    lines = []
    for line in regex_lines:
        if line[0]:
            command = (line[0].upper(), int(line[1]))
            comment = line[5]
            params = split_params(line[2])

        elif include_comments:
            command = (';', None)
            comment = line[6]
            params = {}

        else:
            continue

        lines.append(
            GcodeLine(
                command=command,
                params=params,
                comment=comment,
            ))

    return lines


def split_params(line):
    regex = r'((?!\d)\w+?)(-?\d+\.?\d*)'
    elements = re.findall(regex, line)
    params = {}
    for element in elements:
        params[element[0].upper()] = float(element[1])

    return params


if __name__ == '__main__':
    with open('3DBenchy.gcode', 'r') as f:
        gcode = f.read()
    parsed_gcode = GcodeParser(gcode)
    pass
