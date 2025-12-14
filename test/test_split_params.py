from gcodeparser import parse_parameters


def test_split_int_params():
    assert parse_parameters(" P0 S1 X10") == {"P": 0, "S": 1, "X": 10}


def test_split_float_params():
    assert parse_parameters(" P0.1 S1.1345 X10.0") == {"P": 0.1, "S": 1.1345, "X": 10.0}


def test_split_sub1_params():
    assert parse_parameters(" P0.00001 S-0.00021 X.0001 Y-.003213") == {
        "P": 0.00001,
        "S": -0.00021,
        "X": 0.0001,
        "Y": -0.003213,
    }


def test_split_string_params():
    assert parse_parameters(' P"string"') == {"P": '"string"'}


def test_split_string_with_semicolon_params():
    assert parse_parameters(' P"string ; semicolon"') == {"P": '"string ; semicolon"'}


def test_split_neg_int_params():
    assert parse_parameters(" P-0 S-1 X-10") == {"P": 0, "S": -1, "X": -10}


def test_split_positive_int_params():
    assert parse_parameters(" P+0 S+1 X+10") == {"P": 0, "S": 1, "X": 10}


def test_split_neg_float_params():
    assert parse_parameters(" P-0.1 S-1.1345 X-10.0") == {"P": -0.1, "S": -1.1345, "X": -10.0}


def test_split_positive_float_params():
    assert parse_parameters(" P+0.1 S+1.1345 X+10.0") == {"P": 0.1, "S": 1.1345, "X": 10.0}


def test_split_ip_params():
    assert parse_parameters("P192.168.0.1 S1") == {"P": "192.168.0.1", "S": 1}


def test_split_no_space_params():
    assert parse_parameters('P0.1S1.1345X10.0A"string"') == {"P": 0.1, "S": 1.1345, "X": 10.0, "A": '"string"'}


def test_split_no_value_params():
    assert parse_parameters(" X") == {"X": True}


def test_split_multi_no_value_params():
    assert parse_parameters(" XYZ") == {"X": True, "Y": True, "Z": True}


def test_split_multi_no_value_spaced_params():
    assert parse_parameters(" X Y Z") == {"X": True, "Y": True, "Z": True}
