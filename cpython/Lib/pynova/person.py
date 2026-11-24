"""
PyNova Smart Data Types: Person
Represents and manipulates a person's name with parsing, formatting, and initials extraction.
"""

from typing import Optional


class Person:
    """
    Represents an individual person's name.
    
    Supports automatic extraction of first, middle, and last names,
    as well as explicit override when automatic splitting is ambiguous.
    """
    
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        middle_name: Optional[str] = None
    ) -> None:
        if not name and not first_name:
            raise ValueError("Person requires a non-empty name string or first_name.")
        
        if name is not None and not isinstance(name, str):
            raise TypeError(f"Expected name to be a string, got {type(name).__name__}.")
        
        raw_name = (name or "").strip()
        if not raw_name and not first_name:
            raise ValueError("Person name cannot be empty or whitespace.")

        parts = [p for p in raw_name.split() if p]
        
        # Priority: explicit overrides take precedence over parsed values
        if first_name is not None:
            self._first_name = first_name.strip()
        elif parts:
            self._first_name = parts[0]
        else:
            self._first_name = ""
            
        if middle_name is not None:
            self._middle_name = middle_name.strip()
        elif len(parts) > 2 and last_name is None:
            self._middle_name = " ".join(parts[1:-1])
        else:
            self._middle_name = ""
            
        if last_name is not None:
            self._last_name = last_name.strip()
        elif len(parts) >= 2:
            self._last_name = parts[-1]
        else:
            self._last_name = ""
            
    @property
    def first_name(self) -> str:
        """The person's first name."""
        return self._first_name
        
    @property
    def middle_name(self) -> str:
        """The person's middle name(s), if available."""
        return self._middle_name
        
    @property
    def last_name(self) -> str:
        """The person's last name or surname."""
        return self._last_name
        
    @property
    def full_name(self) -> str:
        """The complete full name formatted cleanly."""
        components = [c for c in (self._first_name, self._middle_name, self._last_name) if c]
        return " ".join(components)
        
    @property
    def initials(self) -> str:
        """
        Initials in standard uppercase notation (e.g., 'S.H.').
        """
        parts = [c for c in (self._first_name, self._middle_name, self._last_name) if c]
        if not parts:
            return ""
        return ".".join(part[0].upper() for part in parts) + "."
        
    def __str__(self) -> str:
        return self.full_name
        
    def __repr__(self) -> str:
        return f"Person(full_name={self.full_name!r}, initials={self.initials!r})"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return False
        return (
            self.first_name == other.first_name and
            self.middle_name == other.middle_name and
            self.last_name == other.last_name
        )
