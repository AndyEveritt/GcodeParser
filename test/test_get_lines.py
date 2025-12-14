from gcodeparser import GcodeLine, parse_gcode_lines


def test_no_params():
    line = GcodeLine(
        command=("G", 21),
        params={},
        comment="",
        line_index=0,
    )
    assert next(parse_gcode_lines("G21")) == line


def test_params():
    line = GcodeLine(
        command=("G", 1),
        params={"X": 10, "Y": 20},
        comment="",
        line_index=0,
    )
    assert next(parse_gcode_lines("G1 X10 Y20")) == line


def test_params_with_explicit_positive_values():
    line = GcodeLine(
        command=("G", 1),
        params={"X": 10, "Y": 20},
        comment="",
        line_index=0,
    )
    assert next(parse_gcode_lines("G1 X+10 Y+20")) == line


def test_2_commands_line():
    line1 = GcodeLine(
        command=("G", 91),
        params={},
        comment="",
        line_index=0,
    )
    line2 = GcodeLine(
        command=("G", 1),
        params={"X": 10, "Y": 20},
        comment="",
        line_index=0,
    )
    lines = list(parse_gcode_lines("G91 G1 X10 Y20"))
    assert len(lines) == 2
    assert lines[0] == line1
    assert lines[1] == line2


def test_string_params():
    line = GcodeLine(
        command=("M", 550),
        params={"P": '"hostname"'},
        comment="",
        line_index=0,
    )
    assert next(parse_gcode_lines('M550 P"hostname"')) == line


def test_ip_address_params():
    line = GcodeLine(
        command=("M", 552),
        params={"P": "192.168.0.1", "S": 1},
        comment="",
        line_index=0,
    )
    assert next(parse_gcode_lines("M552 P192.168.0.1 S1")) == line


def test_inline_comment():
    line = GcodeLine(
        command=("G", 1),
        params={"X": 10, "Y": 20},
        comment="this is a comment",
        line_index=0,
    )
    assert next(parse_gcode_lines("G1 X10 Y20 ; this is a comment")) == line
    assert next(parse_gcode_lines("G1 X10 Y20 ;      this is a comment")) == line
    assert next(parse_gcode_lines("G1 X10 Y20 \t;     \t this is a comment")) == line
    assert next(parse_gcode_lines("G1 X10 Y20 \t;     \t this is a comment")) == line


def test_inline_comment2():
    line = GcodeLine(
        command=("G", 1),
        params={"X": 10, "Y": 20},
        comment="this is a comment ; with a dummy comment for bants",
        line_index=0,
    )
    assert next(parse_gcode_lines("G1 X10 Y20 ; this is a comment ; with a dummy comment for bants")) == line


def test_include_comment_true():
    line = GcodeLine(
        command=(";", None),
        params={},
        comment="this is a comment",
        line_index=0,
    )
    assert next(parse_gcode_lines("; this is a comment", include_comments=True)) == line


def test_include_comment_false():
    assert next(parse_gcode_lines("; this is a comment", include_comments=False), None) is None


def test_multi_line():
    lines = [
        GcodeLine(
            command=("G", 91),
            params={},
            comment="",
            line_index=0,
        ),
        GcodeLine(
            command=("G", 1),
            params={"X": -10, "Y": 20},
            comment="inline comment",
            line_index=1,
        ),
        GcodeLine(
            command=("G", 1),
            params={"Z": 0.5},
            comment="",
            line_index=2,
        ),
        GcodeLine(
            command=("T", 1),
            params={},
            comment="",
            line_index=3,
        ),
        GcodeLine(
            command=("M", 350),
            params={"T": 100},
            comment="",
            line_index=4,
        ),
    ]

    def compare_without_line_index(lines1: list[GcodeLine], lines2: list[GcodeLine]) -> bool:
        if len(lines1) != len(lines2):
            return False
        for line1, line2 in zip(lines1, lines2):
            if line1.command != line2.command:
                return False
            if line1.params != line2.params:
                return False
            if line1.comment != line2.comment:
                return False
        return True

    assert compare_without_line_index(
        list(parse_gcode_lines("G91\nG1 X-10 Y20 ; inline comment\nG1 Z0.5\nT1\nM350 T100")), lines
    )
    assert compare_without_line_index(
        list(parse_gcode_lines("G91G1 X-10 Y20;inline comment\nG1 Z0.5\nT1M350 T100")), lines
    )
    assert compare_without_line_index(
        list(parse_gcode_lines(" \tG91\n\tG1\t  X-10 Y20 \t ;\t inline comment\nG1 Z0.5\nT1\nM350 T100")), lines
    )
    assert compare_without_line_index(
        list(
            parse_gcode_lines(
                "G91\nG1 X-10 Y20 ; inline comment\n; comment to be excluded\nG1 Z0.5\nT1\nM350 T100",
                include_comments=False,
            )
        ),
        lines,
    )
    assert compare_without_line_index(
        list(
            parse_gcode_lines(
                "G91 G1 X-10 Y20 ; inline comment\n; comment to be excluded\nG1 Z0.5\nT1\nM350 T100",
                include_comments=False,
            )
        ),
        lines,
    )
    assert compare_without_line_index(
        list(parse_gcode_lines(" \tG91\n\tG1\t  X-10 Y20 \t ;\t inline comment\nG1 Z0.5\nT1\nM350 T100")), lines
    )
    assert compare_without_line_index(
        list(
            parse_gcode_lines(
                "G91\nG1 X-10 Y20 ; inline comment\n; comment to be excluded\nG1 Z0.5\nT1\nM350 T100",
                include_comments=False,
            )
        ),
        lines,
    )
    assert compare_without_line_index(
        list(
            parse_gcode_lines(
                "G91 G1 X-10 Y20 ; inline comment\n; comment to be excluded\nG1 Z0.5\nT1\nM350 T100",
                include_comments=False,
            )
        ),
        lines,
    )


def test_multi_line2():
    """We want to ignore things that look like gcode in the comments"""
    lines = [
        GcodeLine(
            command=("G", 91),
            params={},
            comment="",
            line_index=0,
        ),
        GcodeLine(
            command=("G", 1),
            params={"X": 100},
            comment="comment G90",
            line_index=0,
        ),
    ]
    assert list(parse_gcode_lines("G91 G1 X100 ; comment G90")) == lines
