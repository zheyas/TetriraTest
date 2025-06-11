import pytest
from solution import strict

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def hello(name: str) -> str:
    return f"Hello, {name}"

@strict
def with_default(a: int, b: int = 10) -> int:
    return a + b

def test_sum_two_ok():
    assert sum_two(1, 2) == 3
    assert sum_two(a=10, b=5) == 15

def test_sum_two_bad_type():
    with pytest.raises(TypeError):
        sum_two(1, 2.5)
    with pytest.raises(TypeError):
        sum_two('1', 2)
    with pytest.raises(TypeError):
        sum_two(a=1, b='2')

def test_hello_ok():
    assert hello("Python") == "Hello, Python"

def test_hello_bad_type():
    with pytest.raises(TypeError):
        hello(123)

def test_with_default_ok():
    assert with_default(5) == 15
    assert with_default(2, 3) == 5

def test_with_default_bad():
    with pytest.raises(TypeError):
        with_default("oops")
    with pytest.raises(TypeError):
        with_default(3, "oops")
