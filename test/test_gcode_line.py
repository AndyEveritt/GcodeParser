from gcodeparser.gcode_parser import (
    GcodeLine,
    GcodeParser,
    get_lines,
    element_type,
    split_params,
)
from gcodeparser.commands import Commands


def test_post_init_move():
    line = GcodeLine(
        command=('G', 1),
        params={'X': 10, 'Y': 20},
        comment='this is a comment',
    )
    assert line.type == Commands.MOVE


def test_post_init_toolchange():
    line = GcodeLine(
        command=('T', 1),
        params={},
        comment='this is a comment',
    )
    assert line.type == Commands.TOOLCHANGE


def test_post_init_other():
    line = GcodeLine(
        command=('G', 91),
        params={'X': 10, 'Y': 20},
        comment='this is a comment',
    )
    assert line.type == Commands.OTHER


def test_command_str():
    line = GcodeLine(
        command=('G', 91),
        params={'X': 10, 'Y': 20},
        comment='this is a comment',
    )
    assert line.command_str == 'G91'


def test_to_gcode():
    line = GcodeLine(
        command=('G', 91),
        params={'X': 10, 'Y': 20},
        comment='this is a comment',
    )
    assert line.gcode_str == 'G91 X10 Y20 ; this is a comment'


def test_flag_parameter_to_gcode():
    line = GcodeLine(
        command=('G', 28),
        params={'X': True},
        comment='',
    )
    assert line.gcode_str == 'G28 X'


def test_flag_parameter_2_to_gcode():
    line = GcodeLine(
        command=('G', 28),
        params={'X': True, 'Y': 1},
        comment='',
    )
    assert line.gcode_str == 'G28 X Y1'
