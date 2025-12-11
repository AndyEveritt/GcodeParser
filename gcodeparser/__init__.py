__version__ = "0.3.0"
__all__ = ["parse_gcode_lines", "GcodeParser", "GcodeLine", "Commands", "infer_element_type", "parse_parameters"]

import io
import re
import warnings
from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Type


class GcodeParser:
    """
    .. deprecated:: 0.3.0
        GcodeParser is deprecated and not recommended for use.
        Use :func:`parse_gcode_lines` instead, which provides a more efficient iterator-based approach.

    Parse gcode into a list of GcodeLine objects.

    .. warning::
        This class is deprecated. Use :func:`parse_gcode_lines` instead.
    """

    gcode: str
    include_comments: bool
    lines: list["GcodeLine"]

    def __init__(self, gcode: str, include_comments=False):
        warnings.warn(
            "GcodeParser is deprecated and not recommended. Use parse_gcode_lines() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.gcode = gcode
        self.include_comments = include_comments
        self.lines = list(parse_gcode_lines(self.gcode, self.include_comments))


class Commands(Enum):
    COMMENT = 0
    MOVE = 1
    OTHER = 2
    TOOLCHANGE = 3


@dataclass
class GcodeLine:
    command: tuple[str, int] | tuple[str, None]
    params: dict[str, float | str]
    comment: str
    line_index: int
    type: Commands = field(init=False)

    def __post_init__(self):
        if self.command[0] == "G" and self.command[1] in (0, 1, 2, 3):
            self.type = Commands.MOVE
        elif self.command[0] == ";":
            self.type = Commands.COMMENT
        elif self.command[0] == "T":
            self.type = Commands.TOOLCHANGE
        else:
            self.type = Commands.OTHER

    @property
    def command_str(self) -> str:
        return f"{self.command[0]}{self.command[1] if self.command[1] is not None else ''}"

    def get_param(
        self,
        param: str,
        return_type: Type[Any] | None = None,
        default: float | str | bool | None = None,
    ) -> float | str | bool | None:
        """
        Returns the value of the param if it exists, otherwise it will the default value.
        If `return_type` is set, the return value will be type cast.
        """
        try:
            if return_type is None:
                return self.params[param]
            else:
                return return_type(self.params[param])
        except KeyError:
            return default

    def update_param(self, param: str, value: int | float) -> float | str | bool | None:
        if self.get_param(param) is None:
            return None
        if type(value) not in (int, float):
            raise TypeError(f"Type {type(value)} is not a valid parameter type")
        self.params[param] = value
        return self.get_param(param)

    def delete_param(self, param: str) -> None:
        if self.get_param(param) is None:
            return
        self.params.pop(param)

    @property
    def gcode_str(self) -> str:
        command = self.command_str

        def param_value(param: str) -> str:
            value = self.get_param(param)
            is_flag_parameter = value is True
            if is_flag_parameter:
                return ""
            return str(value)

        params = " ".join(f"{param}{param_value(param)}" for param in self.params.keys())
        comment = f"; {self.comment}" if self.comment != "" else ""
        if command == ";":
            return comment
        return f"{command} {params} {comment}".strip()


GCODE_LINE_PATTERN = re.compile(
    r'(?!; *.+)(G|M|T|g|m|t)(\d+)(([ \t]*(?!G|M|g|m)\w(".*"|([-+\d\.]*)))*)[ \t]*(;[ \t]*(.*))?|;[ \t]*(.+)'
)
PARAMS_PATTERN = re.compile(r'((?!\d)\w+?)\s*(".*"|(\d+\.?)+|[-+]?\d*\.?\d*)')
DOUBLE_DOT_PATTERN = re.compile(r"\..*\.")
FLOAT_PATTERN = re.compile(r"[+-]?\d*\.\d+")


def parse_gcode_lines(gcode: io.TextIOBase | io.StringIO | str, include_comments: bool = False) -> Iterator[GcodeLine]:
    """
    Parse gcode from a file-like object, StringIO object, or string and yield GcodeLine objects one at a time.

    Args:
        gcode: The gcode content as a file-like object, StringIO object, or string
        include_comments: Whether to include comment-only lines

    Yields:
        GcodeLine objects representing parsed gcode commands
    """
    if isinstance(gcode, str):
        gcode = io.StringIO(gcode)

    for line_index, gcode_line in enumerate(gcode):
        # Find all matches on this line
        matches = list(GCODE_LINE_PATTERN.finditer(gcode_line))
        if not matches:
            continue

        # Separate command matches from comment-only matches
        command_matches = []
        comment_match = None

        for match in matches:
            groups = match.groups()
            if groups[0]:  # Has a command (G/M/T)
                command_matches.append(match)
            elif include_comments:  # Comment-only line
                comment_match = match

        # Handle comment-only lines
        if comment_match and not command_matches:
            groups = comment_match.groups()
            yield GcodeLine(
                command=(";", None),
                params={},
                comment=(groups[-1] or "").strip(),
                line_index=line_index,
            )
            continue

        # Process all commands on this line
        for i, match in enumerate(command_matches):
            groups = match.groups()
            command: tuple[str, int] | tuple[str, None] = (groups[0].upper(), int(groups[1]))
            params = parse_parameters(groups[2] or "")

            # Comments are attached to the last command on the line
            comment = ""
            if i == len(command_matches) - 1:
                # Get comment from the match's groups (group index -2 is the inline comment)
                comment = (groups[-2] or "").strip()
                # If no inline comment in this match, check if there's a comment match after
                if not comment and comment_match:
                    comment_pos = comment_match.start()
                    if comment_pos > match.end():
                        comment = (comment_match.groups()[-1] or "").strip()

            yield GcodeLine(
                command=command,
                params=params,
                comment=comment,
                line_index=line_index,
            )


def infer_element_type(element: str) -> type[int] | type[float] | type[str]:
    """
    Infer the Python type of a gcode parameter element.

    Args:
        element: The parameter value string

    Returns:
        The inferred type (int, float, or str)
    """
    if '"' in element or DOUBLE_DOT_PATTERN.search(element):
        return str
    if FLOAT_PATTERN.search(element):
        return float
    return int


def parse_parameters(line: str) -> dict[str, float | str | bool]:
    """
    Parse parameter string from a gcode line into a dictionary.

    Args:
        line: The parameter portion of a gcode line

    Returns:
        Dictionary mapping parameter names to their values
    """
    elements = PARAMS_PATTERN.findall(line)
    params: dict[str, float | str | bool] = {}
    for element in elements:
        if element[1] == "":
            params[element[0].upper()] = True
            continue
        element_type = infer_element_type(element[1])
        params[element[0].upper()] = element_type(element[1])

    return params
