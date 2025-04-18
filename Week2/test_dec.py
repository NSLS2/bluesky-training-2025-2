# test_dec.py

import pytest

# Function to test
def dec(x):
    return x - 1

# Test cases
def test_dec_positive():
    assert dec(5) == 4

def test_dec_zero():
    assert dec(0) == -1

def test_dec_negative():
    assert dec(-3) == -4

def test_dec_float():
    assert dec(2.5) == 1.5

def test_dec_false():
    assert dec(3) == 1