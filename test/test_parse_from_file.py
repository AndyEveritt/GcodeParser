import io
import tempfile
from pathlib import Path

from gcodeparser import parse_gcode_lines


def test_parse_from_stringio():
    """Test parsing from StringIO object"""
    gcode_content = "G21\nG1 X10 Y20\nM104 S200"
    stringio = io.StringIO(gcode_content)
    
    lines = list(parse_gcode_lines(stringio))
    
    assert len(lines) == 3
    assert lines[0].command == ("G", 21)
    assert lines[1].command == ("G", 1)
    assert lines[1].params == {"X": 10, "Y": 20}
    assert lines[2].command == ("M", 104)
    assert lines[2].params == {"S": 200}


def test_parse_from_file_object():
    """Test parsing from a file-like object (TextIO)"""
    gcode_content = "G21\nG1 X10 Y20 ; move to position\nM104 S200"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines = list(parse_gcode_lines(f))
        
        assert len(lines) == 3
        assert lines[0].command == ("G", 21)
        assert lines[1].command == ("G", 1)
        assert lines[1].params == {"X": 10, "Y": 20}
        assert lines[1].comment == "move to position"
        assert lines[2].command == ("M", 104)
        assert lines[2].params == {"S": 200}
    finally:
        temp_path.unlink()


def test_parse_from_file_with_comments():
    """Test parsing from file with include_comments=True"""
    gcode_content = "G21\n; this is a comment\nG1 X10 Y20"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines = list(parse_gcode_lines(f, include_comments=True))
        
        assert len(lines) == 3
        assert lines[0].command == ("G", 21)
        assert lines[1].command == (";", None)
        assert lines[1].comment == "this is a comment"
        assert lines[2].command == ("G", 1)
    finally:
        temp_path.unlink()


def test_parse_from_file_without_comments():
    """Test parsing from file with include_comments=False"""
    gcode_content = "G21\n; this is a comment\nG1 X10 Y20"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines = list(parse_gcode_lines(f, include_comments=False))
        
        assert len(lines) == 2
        assert lines[0].command == ("G", 21)
        assert lines[1].command == ("G", 1)
    finally:
        temp_path.unlink()


def test_parse_from_file_iteration():
    """Test that we can iterate over file lines one at a time"""
    gcode_content = "G21\nG1 X10 Y20\nM104 S200"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines = []
            for line in parse_gcode_lines(f, include_comments=False):
                lines.append(line)
        
        assert len(lines) == 3
        assert lines[0].command == ("G", 21)
        assert lines[1].command == ("G", 1)
        assert lines[2].command == ("M", 104)
    finally:
        temp_path.unlink()


def test_parse_from_string_vs_file():
    """Test that parsing from string and file gives same results"""
    gcode_content = "G21\nG1 X10 Y20 ; comment\nM104 S200"
    
    # Parse from string
    lines_from_string = list(parse_gcode_lines(gcode_content))
    
    # Parse from file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines_from_file = list(parse_gcode_lines(f))
        
        assert len(lines_from_string) == len(lines_from_file)
        for str_line, file_line in zip(lines_from_string, lines_from_file):
            assert str_line.command == file_line.command
            assert str_line.params == file_line.params
            assert str_line.comment == file_line.comment
    finally:
        temp_path.unlink()


def test_parse_from_file_multiline_commands():
    """Test parsing multiple commands on same line from file"""
    gcode_content = "G91 G1 X10 Y20\nM104 S200 M106 S50"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines = list(parse_gcode_lines(f))
        
        assert len(lines) == 4
        assert lines[0].command == ("G", 91)
        assert lines[1].command == ("G", 1)
        assert lines[1].params == {"X": 10, "Y": 20}
        assert lines[2].command == ("M", 104)
        assert lines[2].params == {"S": 200}
        assert lines[3].command == ("M", 106)
        assert lines[3].params == {"S": 50}
    finally:
        temp_path.unlink()


def test_parse_from_file_empty_lines():
    """Test parsing file with empty lines"""
    gcode_content = "G21\n\nG1 X10\n\nM104 S200\n"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.gcode') as f:
        f.write(gcode_content)
        temp_path = Path(f.name)
    
    try:
        with open(temp_path, 'r') as f:
            lines = list(parse_gcode_lines(f))
        
        assert len(lines) == 3
        assert lines[0].command == ("G", 21)
        assert lines[1].command == ("G", 1)
        assert lines[2].command == ("M", 104)
    finally:
        temp_path.unlink()

