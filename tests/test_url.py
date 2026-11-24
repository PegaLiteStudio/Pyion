"""
Unit tests for PyNova Smart Data Type: URL
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Lib")))
from pynova.url import URL


class TestURL(unittest.TestCase):

    def test_https_url(self):
        u = URL("https://example.com/docs/index.html")
        self.assertEqual(u.protocol, "https")
        self.assertEqual(u.domain, "example.com")
        self.assertEqual(u.path, "/docs/index.html")
        self.assertTrue(u.is_secure)
        self.assertTrue(u.is_valid)

    def test_http_url(self):
        u = URL("http://insecure-site.org/home")
        self.assertEqual(u.protocol, "http")
        self.assertFalse(u.is_secure)
        self.assertTrue(u.is_valid)

    def test_query_and_fragment(self):
        u = URL("https://search.engine.com/search?q=pynova#results")
        self.assertEqual(u.query, "q=pynova")
        self.assertEqual(u.fragment, "results")

    def test_empty_url(self):
        with self.assertRaises(ValueError):
            URL("")

    def test_non_string_url(self):
        with self.assertRaises(TypeError):
            URL(["https://invalid"])  # type: ignore


if __name__ == "__main__":
    unittest.main()
