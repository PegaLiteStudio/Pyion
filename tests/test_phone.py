"""
Unit tests for PyNova Smart Data Type: PhoneNumber
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Lib")))
from pynova.phone import PhoneNumber


class TestPhoneNumber(unittest.TestCase):

    def test_valid_indian_number(self):
        ph = PhoneNumber("+919876543210")
        self.assertEqual(ph.country_code, 91)
        self.assertEqual(ph.national_number, 9876543210)
        self.assertTrue(ph.is_valid)
        self.assertIn("98765", ph.formatted)
        self.assertIn("India", ph.country)

    def test_valid_us_number(self):
        ph = PhoneNumber("+16502530000")
        self.assertEqual(ph.country_code, 1)
        self.assertTrue(ph.is_valid)
        self.assertIn("CA", ph.country)

    def test_invalid_syntax_number(self):
        ph = PhoneNumber("+9999999999999999999")
        self.assertFalse(ph.is_valid)

    def test_empty_number(self):
        with self.assertRaises(ValueError):
            PhoneNumber("")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            PhoneNumber(9876543210)  # type: ignore


if __name__ == "__main__":
    unittest.main()
