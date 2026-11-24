"""
PyNova Smart Data Types: EmailAddress
Represents, parses, normalizes, and validates email address structures.
"""

from typing import Optional
import re


# Practical RFC 5322-compliant email syntax pattern
_EMAIL_REGEX = re.compile(
    r"^(?P<local>[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+)@"
    r"(?P<domain>[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+)$"
)


class EmailAddress:
    """
    Represents an electronic mail address.
    
    Provides access to username, domain, top-level/secondary domain extensions,
    and syntactic validity.
    
    Note: Validity indicates proper formatting according to internet standards;
    it does NOT verify mailbox existence or deliverability.
    """
    
    def __init__(self, address: str) -> None:
        if not isinstance(address, str):
            raise TypeError(f"EmailAddress requires a string, got {type(address).__name__}.")
            
        clean_addr = address.strip()
        if not clean_addr:
            raise ValueError("Email address string cannot be empty.")
            
        self._raw_input: str = clean_addr
        self._username: str = ""
        self._domain: str = ""
        self._extension: str = ""
        self._is_valid: bool = False
        
        self._parse()
        
    def _parse(self) -> None:
        match = _EMAIL_REGEX.match(self._raw_input)
        if match:
            self._username = match.group("local")
            self._domain = match.group("domain").lower()
            self._is_valid = True
            
            # Extract domain extension (e.g. "com" in "example.com", or "co.uk" in "example.co.uk")
            parts = self._domain.split(".")
            if len(parts) >= 3 and parts[-2] in {"co", "com", "edu", "gov", "ac", "org", "net"}:
                self._extension = f"{parts[-2]}.{parts[-1]}"
            elif parts:
                self._extension = parts[-1]
            else:
                self._extension = ""
        else:
            self._is_valid = False
            if "@" in self._raw_input:
                parts = self._raw_input.split("@", 1)
                self._username = parts[0]
                self._domain = parts[1].lower()
                domain_parts = self._domain.split(".")
                self._extension = domain_parts[-1] if len(domain_parts) > 1 else ""
            else:
                self._username = self._raw_input
                self._domain = ""
                self._extension = ""
                
    @property
    def address(self) -> str:
        """The normalized email address (with lowercase domain)."""
        if self._domain:
            return f"{self._username}@{self._domain}"
        return self._raw_input
        
    @property
    def username(self) -> str:
        """The local part (username) preceding the @ symbol."""
        return self._username
        
    @property
    def domain(self) -> str:
        """The host domain following the @ symbol."""
        return self._domain
        
    @property
    def extension(self) -> str:
        """The domain extension or suffix (e.g., 'com', 'org', 'edu.in')."""
        return self._extension
        
    @property
    def is_valid(self) -> bool:
        """
        True if the email matches valid RFC 5322 address syntax.
        Does NOT guarantee mailbox activity.
        """
        return self._is_valid
        
    def __str__(self) -> str:
        return self.address
        
    def __repr__(self) -> str:
        return f"EmailAddress({self.address!r}, valid={self._is_valid})"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EmailAddress):
            return False
        return self.address.lower() == other.address.lower()
