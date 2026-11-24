"""
Unit tests for PyNova Smart Data Type: EmailAddress
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Lib")))
from pynova.email import EmailAddress


class TestEmailAddress(unittest.TestCase):

    def test_valid_standard_email(self):
        em = EmailAddress("sahil@example.com")
        self.assertEqual(em.address, "sahil@example.com")
        self.assertEqual(em.username, "sahil")
        self.assertEqual(em.domain, "example.com")
        self.assertEqual(em.extension, "com")
        self.assertTrue(em.is_valid)

    def test_domain_normalization(self):
        em = EmailAddress("User@EXAMPLE.COM")
        self.assertEqual(em.domain, "example.com")
        self.assertEqual(em.address, "User@example.com")

    def test_multi_level_tld(self):
        em = EmailAddress("info@university.ac.in")
        self.assertEqual(em.username, "info")
        self.assertEqual(em.domain, "university.ac.in")
        self.assertEqual(em.extension, "ac.in")
        self.assertTrue(em.is_valid)

    def test_invalid_email_format(self):
        em = EmailAddress("not-an-email")
        self.assertFalse(em.is_valid)
        self.assertEqual(em.username, "not-an-email")

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            EmailAddress("")

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            EmailAddress(12345)  # type: ignore


if __name__ == "__main__":
    unittest.main()
