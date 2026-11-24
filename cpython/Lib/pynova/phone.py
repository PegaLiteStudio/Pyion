"""
PyNova Smart Data Types: PhoneNumber
Represents, parses, formats, and validates international telephone numbers
using official ITU-T numbering-plan metadata.
"""

from typing import Optional
import re

try:
    import phonenumbers
    from phonenumbers import geocoder
    _HAS_PHONENUMBERS = True
except ImportError:
    _HAS_PHONENUMBERS = False


class PhoneNumber:
    """
    Represents an international telephone number.
    
    Extracts country calling code, national number, formatted representation,
    validity flag, and geographic region.
    
    Note: Validity indicates conformance with international numbering plans;
    it does NOT verify whether a line is currently active or in service.
    """
    
    def __init__(self, number: str, default_region: Optional[str] = None) -> None:
        if not isinstance(number, str):
            raise TypeError(f"PhoneNumber requires a string argument, got {type(number).__name__}.")
            
        clean_input = number.strip()
        if not clean_input:
            raise ValueError("Phone number string cannot be empty.")
            
        self._raw_input: str = clean_input
        self._country_code: Optional[int] = None
        self._national_number: Optional[int] = None
        self._is_valid: bool = False
        self._country_name: str = "Unknown"
        self._formatted: str = clean_input
        
        self._parse(default_region)
        
    def _parse(self, default_region: Optional[str]) -> None:
        if _HAS_PHONENUMBERS:
            try:
                parsed = phonenumbers.parse(self._raw_input, default_region)
                self._country_code = parsed.country_code
                self._national_number = parsed.national_number
                self._is_valid = phonenumbers.is_valid_number(parsed)
                
                # Format to standard E.164 and international
                self._formatted = phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
                
                # Geographic country resolution
                country_desc = geocoder.description_for_number(parsed, "en")
                if country_desc:
                    self._country_name = country_desc
                elif self._country_code:
                    region = phonenumbers.region_code_for_country_code(self._country_code)
                    self._country_name = region or "Unknown"
                return
            except phonenumbers.NumberParseException:
                pass
                
        # Fallback rudimentary parser if phonenumbers library is unavailable or parse fails
        normalized = re.sub(r"[^\d+]", "", self._raw_input)
        if normalized.startswith("+"):
            digits = normalized[1:]
            if len(digits) >= 10:
                # Common country calling code heuristics
                if digits.startswith("1"):
                    self._country_code = 1
                    self._national_number = int(digits[1:])
                    self._country_name = "US/CA"
                elif digits.startswith("91"):
                    self._country_code = 91
                    self._national_number = int(digits[2:])
                    self._country_name = "India"
                elif digits.startswith("44"):
                    self._country_code = 44
                    self._national_number = int(digits[2:])
                    self._country_name = "United Kingdom"
                else:
                    self._country_code = int(digits[:3])
                    self._national_number = int(digits[3:])
                self._is_valid = (7 <= len(digits) <= 15)
                self._formatted = f"+{self._country_code} {self._national_number}"
                return
                
        self._is_valid = False
        self._formatted = self._raw_input
        
    @property
    def number(self) -> str:
        """The normalized or raw telephone number string."""
        return self._raw_input
        
    @property
    def country_code(self) -> Optional[int]:
        """The international calling country code (e.g., 91 for India, 1 for US)."""
        return self._country_code
        
    @property
    def national_number(self) -> Optional[int]:
        """The subscriber / national phone number digits."""
        return self._national_number
        
    @property
    def country(self) -> str:
        """The country or territory name associated with this numbering plan."""
        return self._country_name
        
    @property
    def is_valid(self) -> bool:
        """
        True if the number conforms to standard international dialing format.
        Does NOT guarantee active subscription.
        """
        return self._is_valid
        
    @property
    def formatted(self) -> str:
        """The phone number formatted for readability."""
        return self._formatted
        
    def __str__(self) -> str:
        return self.formatted
        
    def __repr__(self) -> str:
        return f"PhoneNumber({self._raw_input!r}, valid={self._is_valid}, country={self._country_name!r})"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhoneNumber):
            return False
        return (
            self.country_code == other.country_code and
            self.national_number == other.national_number and
            self.is_valid == other.is_valid
        )
