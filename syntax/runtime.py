"""
PyNova Runtime Support Utilities
Injected runtime validation helpers for PyNova custom syntax features.
"""

import sys
import time
from typing import Any, Iterator


def _pynova_validate_repeat(count: Any, line_num: int) -> range:
    """
    Validates the count expression for a 'repeat' block.
    
    Ensures that count is an integer >= 0, raising clear errors if invalid.
    """
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError(
            f"PyNova repeat count at line {line_num} must be an integer, "
            f"got {type(count).__name__} ({count!r})."
        )
    if count < 0:
        raise ValueError(
            f"PyNova repeat count at line {line_num} cannot be negative (got {count})."
        )
    return range(count)


def _pynova_runtime_wait(duration: Any, line_num: int) -> None:
    """
    Validates and executes a 'wait' delay statement.
    """
    if isinstance(duration, bool) or not isinstance(duration, (int, float)):
        raise TypeError(
            f"PyNova wait duration at line {line_num} must be a number (int or float), "
            f"got {type(duration).__name__} ({duration!r})."
        )
    if duration < 0:
        raise ValueError(
            f"PyNova wait duration at line {line_num} cannot be negative (got {duration})."
        )
    time.sleep(duration)


def _pynova_handle_safe_error(exc: Exception, line_num: int) -> None:
    """
    Outputs a readable error message for caught exceptions in a 'safe:' block.
    Does not swallow SystemExit or KeyboardInterrupt (ensured by catching Exception).
    """
    sys.stderr.write(
        f"[PyNova Safe Block Caught Error at line {line_num}]: "
        f"{type(exc).__name__}: {exc}\n"
    )
