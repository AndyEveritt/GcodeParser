from gcodeparser.gcode_parser import (
    GcodeLine,
    GcodeParser,
    get_lines,
    element_type,
    split_params,
)
from gcodeparser.commands import Commands


def test_no_params():
    line = GcodeLine(
        command=('G', 21),
        params={},
        comment='',
    )
    assert get_lines('G21')[0] == line


def test_params():
    line = GcodeLine(
        command=('G', 1),
        params={'X': 10, 'Y': 20},
        comment='',
    )
    assert get_lines('G1 X10 Y20')[0] == line


def test_params_with_explicit_positive_values():
    line = GcodeLine(
        command=('G', 1),
        params={'X': 10, 'Y': 20},
        comment='',
    )
    assert get_lines('G1 X+10 Y+20')[0] == line


def test_2_commands_line():
    line1 = GcodeLine(
        command=('G', 91),
        params={},
        comment='',
    )
    line2 = GcodeLine(
        command=('G', 1),
        params={'X': 10, 'Y': 20},
        comment='',
    )
    lines = get_lines('G91 G1 X10 Y20')
    assert lines[0] == line1
    assert lines[1] == line2


def test_string_params():
    line = GcodeLine(
        command=('M', 550),
        params={'P': '"hostname"'},
        comment='',
    )
    assert get_lines('M550 P"hostname"')[0] == line


def test_ip_address_params():
    line = GcodeLine(
        command=('M', 552),
        params={'P': '192.168.0.1', 'S': 1},
        comment='',
    )
    assert get_lines('M552 P192.168.0.1 S1')[0] == line


def test_inline_comment():
    line = GcodeLine(
        command=('G', 1),
        params={'X': 10, 'Y': 20},
        comment='this is a comment',
    )
    assert get_lines('G1 X10 Y20 ; this is a comment')[0] == line
    assert get_lines('G1 X10 Y20 ;      this is a comment')[0] == line
    assert get_lines('G1 X10 Y20 \t;     \t this is a comment')[0] == line
    assert get_lines('G1 X10 Y20 \t;     \t this is a comment')[0] == line


def test_inline_comment2():
    line = GcodeLine(
        command=('G', 1),
        params={'X': 10, 'Y': 20},
        comment='this is a comment ; with a dummy comment for bants',
    )
    assert get_lines('G1 X10 Y20 ; this is a comment ; with a dummy comment for bants')[0] == line


def test_include_comment_true():
    line = GcodeLine(
        command=(';', None),
        params={},
        comment='this is a comment',
    )
    assert get_lines('; this is a comment', include_comments=True)[0] == line


def test_include_comment_false():
    assert len(get_lines('; this is a comment', include_comments=False)) == 0


def test_multi_line():
    lines = [
        GcodeLine(
            command=('G', 91),
            params={},
            comment='',
        ), GcodeLine(
            command=('G', 1),
            params={'X': -10, 'Y': 20},
            comment='inline comment',
        ), GcodeLine(
            command=('G', 1),
            params={'Z': 0.5},
            comment='',
        ), GcodeLine(
            command=('T', 1),
            params={},
            comment='',
        ), GcodeLine(
            command=('M', 350),
            params={'T': 100},
            comment='',
        )]
    assert get_lines('G91\nG1 X-10 Y20 ; inline comment\nG1 Z0.5\nT1\nM350 T100') == lines
    assert get_lines('G91G1 X-10 Y20;inline comment\nG1 Z0.5\nT1M350 T100') == lines
    assert get_lines(' \tG91\n\tG1\t  X-10 Y20 \t ;\t inline comment\nG1 Z0.5\nT1\nM350 T100') == lines
    assert get_lines('G91\nG1 X-10 Y20 ; inline comment\n; comment to be excluded\nG1 Z0.5\nT1\nM350 T100',
                     include_comments=False) == lines
    assert get_lines('G91 G1 X-10 Y20 ; inline comment\n; comment to be excluded\nG1 Z0.5\nT1\nM350 T100',
                     include_comments=False) == lines


def test_multi_line2():
    """ We want to ignore things that look like gcode in the comments
    """
    lines = [
        GcodeLine(
            command=('G', 91),
            params={},
            comment='',
        ),
        GcodeLine(
            command=('G', 1),
            params={'X': 100},
            comment='comment G90'
        )
    ]
    assert get_lines('G91 G1 X100 ; comment G90') == lines
