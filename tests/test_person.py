"""
Unit tests for PyNova Smart Data Type: Person
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Lib")))
from pynova.person import Person


class TestPerson(unittest.TestCase):

    def test_basic_two_word_name(self):
        p = Person("Sahil Hossain")
        self.assertEqual(p.first_name, "Sahil")
        self.assertEqual(p.last_name, "Hossain")
        self.assertEqual(p.middle_name, "")
        self.assertEqual(p.full_name, "Sahil Hossain")
        self.assertEqual(p.initials, "S.H.")
        self.assertEqual(str(p), "Sahil Hossain")

    def test_three_word_name(self):
        p = Person("Mohammad Sahil Hossain")
        self.assertEqual(p.first_name, "Mohammad")
        self.assertEqual(p.middle_name, "Sahil")
        self.assertEqual(p.last_name, "Hossain")
        self.assertEqual(p.full_name, "Mohammad Sahil Hossain")
        self.assertEqual(p.initials, "M.S.H.")

    def test_single_word_name(self):
        p = Person("Plato")
        self.assertEqual(p.first_name, "Plato")
        self.assertEqual(p.last_name, "")
        self.assertEqual(p.middle_name, "")
        self.assertEqual(p.initials, "P.")

    def test_explicit_overrides(self):
        p = Person(first_name="Ada", last_name="Lovelace")
        self.assertEqual(p.first_name, "Ada")
        self.assertEqual(p.last_name, "Lovelace")
        self.assertEqual(p.full_name, "Ada Lovelace")
        self.assertEqual(p.initials, "A.L.")

    def test_whitespace_handling(self):
        p = Person("   Alan    Turing   ")
        self.assertEqual(p.first_name, "Alan")
        self.assertEqual(p.last_name, "Turing")
        self.assertEqual(p.full_name, "Alan Turing")
        self.assertEqual(p.initials, "A.T.")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            Person("")
        with self.assertRaises(TypeError):
            Person(123)  # type: ignore


if __name__ == "__main__":
    unittest.main()
