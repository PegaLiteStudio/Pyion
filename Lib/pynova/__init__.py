"""
PyNova: A Customized Python Distribution and Runtime
Provides smart data types and language enhancements.
"""

from pynova.person import Person
from pynova.phone import PhoneNumber
from pynova.email import EmailAddress
from pynova.url import URL
from pynova.address import Address

__version__ = "1.0.0"
__all__ = [
    "Person",
    "PhoneNumber",
    "EmailAddress",
    "URL",
    "Address",
    "__version__",
]
