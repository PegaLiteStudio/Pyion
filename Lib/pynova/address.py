"""
PyNova Smart Data Types: Address
Represents structured physical postal addresses with formatting and validation.
"""

from typing import Optional


class Address:
    """
    Represents a structured postal address.
    
    Prefers explicit geographic attributes (street, city, state, country,
    postal code) over fragile free-text parsing.
    """
    
    def __init__(
        self,
        *,
        city: str,
        state: str,
        country: str,
        postal_code: str,
        street: Optional[str] = None,
        building: Optional[str] = None
    ) -> None:
        if not city or not isinstance(city, str):
            raise ValueError("Address requires a non-empty string for 'city'.")
        if not state or not isinstance(state, str):
            raise ValueError("Address requires a non-empty string for 'state'.")
        if not country or not isinstance(country, str):
            raise ValueError("Address requires a non-empty string for 'country'.")
        if not postal_code or not isinstance(postal_code, str):
            raise ValueError("Address requires a non-empty string for 'postal_code'.")
            
        self._city: str = city.strip()
        self._state: str = state.strip()
        self._country: str = country.strip()
        self._postal_code: str = str(postal_code).strip()
        self._street: Optional[str] = street.strip() if street else None
        self._building: Optional[str] = building.strip() if building else None
        
    @property
    def city(self) -> str:
        """The city, municipality, or district."""
        return self._city
        
    @property
    def state(self) -> str:
        """The province, state, or administrative region."""
        return self._state
        
    @property
    def country(self) -> str:
        """The country or sovereign state name."""
        return self._country
        
    @property
    def postal_code(self) -> str:
        """The postal code, ZIP code, or PIN code."""
        return self._postal_code
        
    @property
    def street(self) -> Optional[str]:
        """The street name or road line, if provided."""
        return self._street
        
    @property
    def building(self) -> Optional[str]:
        """Building, estate, or apartment identifier, if provided."""
        return self._building
        
    @property
    def formatted(self) -> str:
        """
        Formatted single-line postal address string.
        """
        parts = []
        if self._building:
            parts.append(self._building)
        if self._street:
            parts.append(self._street)
        parts.append(self._city)
        parts.append(f"{self._state} - {self._postal_code}")
        parts.append(self._country)
        return ", ".join(parts)
        
    def to_multiline(self) -> str:
        """
        Formatted multi-line postal address string suitable for mail labels.
        """
        lines = []
        if self._building:
            lines.append(self._building)
        if self._street:
            lines.append(self._street)
        lines.append(f"{self._city}, {self._state} {self._postal_code}")
        lines.append(self._country)
        return "\n".join(lines)
        
    def __str__(self) -> str:
        return self.formatted
        
    def __repr__(self) -> str:
        return (
            f"Address(city={self.city!r}, state={self.state!r}, "
            f"country={self.country!r}, postal_code={self.postal_code!r})"
        )
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return False
        return (
            self.city.lower() == other.city.lower() and
            self.state.lower() == other.state.lower() and
            self.country.lower() == other.country.lower() and
            self.postal_code == other.postal_code and
            self.street == other.street and
            self.building == other.building
        )
