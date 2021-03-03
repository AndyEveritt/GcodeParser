from gcodeparser.gcode_parser import (
    GcodeLine,
    GcodeParser,
    get_lines,
    element_type,
    split_params,
)
from gcodeparser.commands import Commands


def test_split_int_params():
    assert split_params(' P0 S1 X10') == {'P': 0, 'S': 1, 'X': 10}


def test_split_float_params():
    assert split_params(' P0.1 S1.1345 X10.0') == {'P': 0.1, 'S': 1.1345, 'X': 10.0}


def test_split_string_params():
    assert split_params(' P"string"') == {'P': '"string"'}


def test_split_string_with_semicolon_params():
    assert split_params(' P"string ; semicolon"') == {'P': '"string ; semicolon"'}


def test_split_neg_int_params():
    assert split_params(' P-0 S-1 X-10') == {'P': 0, 'S': -1, 'X': -10}


def test_split_neg_float_params():
    assert split_params(' P-0.1 S-1.1345 X-10.0') == {'P': -0.1, 'S': -1.1345, 'X': -10.0}


def test_split_ip_params():
    assert split_params('P192.168.0.1 S1') == {'P': '192.168.0.1', 'S': 1}


def test_split_no_space_params():
    assert split_params('P0.1S1.1345X10.0A"string"') == {'P': 0.1, 'S': 1.1345, 'X': 10.0, 'A': '"string"'}
