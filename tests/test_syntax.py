"""
Unit tests for PyNova Syntax Additions: repeat, safe, wait, between
"""

import sys
import os
import unittest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from syntax.translator import translate_pynova
from syntax.runtime import _pynova_validate_repeat, _pynova_runtime_wait, _pynova_handle_safe_error


class TestPyNovaSyntax(unittest.TestCase):

    def _execute(self, source: str) -> dict:
        translated = translate_pynova(source)
        scope = {
            "__builtins__": __builtins__,
            "_pynova_validate_repeat": _pynova_validate_repeat,
            "_pynova_runtime_wait": _pynova_runtime_wait,
            "_pynova_handle_safe_error": _pynova_handle_safe_error,
        }
        exec(translated, scope)
        return scope

    # 1. Repeat tests
    def test_repeat_loop_count(self):
        code = """
count = 0
repeat 5:
    count += 1
"""
        scope = self._execute(code)
        self.assertEqual(scope["count"], 5)

    def test_repeat_nested(self):
        code = """
inner_ticks = 0
repeat 3:
    repeat 4:
        inner_ticks += 1
"""
        scope = self._execute(code)
        self.assertEqual(scope["inner_ticks"], 12)

    def test_repeat_invalid_negative(self):
        code = """
repeat -3:
    pass
"""
        with self.assertRaises(ValueError):
            self._execute(code)

    def test_repeat_invalid_type(self):
        code = """
repeat "three":
    pass
"""
        with self.assertRaises(TypeError):
            self._execute(code)

    # 2. Safe tests
    def test_safe_handles_exception_and_continues(self):
        code = """
checkpoint_1 = True
safe:
    bad = 10 / 0
checkpoint_2 = True
"""
        scope = self._execute(code)
        self.assertTrue(scope["checkpoint_1"])
        self.assertTrue(scope["checkpoint_2"])

    def test_safe_does_not_swallow_system_exit(self):
        code = """
safe:
    raise SystemExit("Exit program")
"""
        with self.assertRaises(SystemExit):
            self._execute(code)

    # 3. Wait tests
    def test_wait_duration(self):
        code = """
import time
t0 = time.time()
wait 0.1
elapsed = time.time() - t0
"""
        scope = self._execute(code)
        self.assertGreaterEqual(scope["elapsed"], 0.08)

    def test_wait_negative_duration(self):
        code = """
wait -1
"""
        with self.assertRaises(ValueError):
            self._execute(code)

    # 4. Between tests
    def test_between_inclusive_bounds(self):
        code = """
res_mid = (25 between 18 and 60)
res_low = (18 between 18 and 60)
res_high = (60 between 18 and 60)
res_below = (17 between 18 and 60)
res_above = (61 between 18 and 60)
"""
        scope = self._execute(code)
        self.assertTrue(scope["res_mid"])
        self.assertTrue(scope["res_low"])
        self.assertTrue(scope["res_high"])
        self.assertFalse(scope["res_below"])
        self.assertFalse(scope["res_above"])

    def test_between_in_if_statement(self):
        code = """
age = 30
status = "unknown"
if age between 18 and 60:
    status = "eligible"
"""
        scope = self._execute(code)
        self.assertEqual(scope["status"], "eligible")

    # 5. Normal Python compatibility
    def test_standard_python_syntax_unaffected(self):
        code = """
def add(a, b):
    return a + b

nums = [add(i, 1) for i in range(5)]
"""
        scope = self._execute(code)
        self.assertEqual(scope["nums"], [1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
