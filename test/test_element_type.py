from gcodeparser.gcode_parser import (
    element_type,
)


def test_element_type_int():
    assert element_type('109321') == int


def test_element_type_neg_int():
    assert element_type('-109321') == int


def test_element_type_float():
    assert element_type('109321.0') == float


def test_element_type_float2():
    assert element_type('109321.012345') == float


def test_element_type_neg_float():
    assert element_type('-1.0') == float


def test_element_type_neg_float2():
    assert element_type('-1.013456') == float


def test_element_type_str():
    assert element_type('192.168.0.1') == str


def test_element_type_str2():
    assert element_type('"test string"') == str
