from gcodeparser import infer_element_type


def test_element_type_int():
    assert infer_element_type("109321") is int


def test_element_type_neg_int():
    assert infer_element_type("-109321") is int


def test_element_type_float():
    assert infer_element_type("109321.0") is float


def test_element_type_float2():
    assert infer_element_type("109321.012345") is float


def test_element_type_neg_float():
    assert infer_element_type("-1.0") is float


def test_element_type_neg_float2():
    assert infer_element_type("-1.013456") is float


def test_element_type_str():
    assert infer_element_type("192.168.0.1") is str


def test_element_type_str2():
    assert infer_element_type('"test string"') is str
