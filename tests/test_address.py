"""
Unit tests for PyNova Smart Data Type: Address
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Lib")))
from pynova.address import Address


class TestAddress(unittest.TestCase):

    def test_structured_address(self):
        addr = Address(
            city="Agartala",
            state="Tripura",
            country="India",
            postal_code="799001"
        )
        self.assertEqual(addr.city, "Agartala")
        self.assertEqual(addr.state, "Tripura")
        self.assertEqual(addr.country, "India")
        self.assertEqual(addr.postal_code, "799001")
        self.assertIn("Agartala", addr.formatted)
        self.assertIn("799001", addr.formatted)

    def test_street_and_building_support(self):
        addr = Address(
            building="Tech Park 4",
            street="Main Boulevard",
            city="Bengaluru",
            state="Karnataka",
            country="India",
            postal_code="560100"
        )
        self.assertEqual(addr.street, "Main Boulevard")
        self.assertEqual(addr.building, "Tech Park 4")
        self.assertIn("Tech Park 4", addr.to_multiline())

    def test_missing_required_fields(self):
        with self.assertRaises(ValueError):
            Address(city="", state="Tripura", country="India", postal_code="799001")
        with self.assertRaises(ValueError):
            Address(city="Agartala", state="", country="India", postal_code="799001")


if __name__ == "__main__":
    unittest.main()
