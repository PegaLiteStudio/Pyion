"""
PyNova Smart Data Types: URL
Represents, parses, validates, and inspects web Uniform Resource Locators.
"""

from typing import Optional
from urllib.parse import urlparse, urlunparse


class URL:
    """
    Represents a Web Uniform Resource Locator (URL).
    
    Provides access to protocol/scheme, domain/hostname, port, path,
    query parameters, fragment, and security status.
    
    Note: is_secure indicates that the URL uses TLS/HTTPS transport;
    it does NOT guarantee the content or safety of the target destination.
    """
    
    def __init__(self, url: str) -> None:
        if not isinstance(url, str):
            raise TypeError(f"URL requires a string, got {type(url).__name__}.")
            
        clean_url = url.strip()
        if not clean_url:
            raise ValueError("URL string cannot be empty.")
            
        self._raw_input: str = clean_url
        self._scheme: str = ""
        self._domain: str = ""
        self._port: Optional[int] = None
        self._path: str = ""
        self._query: str = ""
        self._fragment: str = ""
        self._is_valid: bool = False
        
        self._parse()
        
    def _parse(self) -> None:
        # Default scheme assumption if not provided
        target = self._raw_input
        if "://" not in target and not target.startswith("//"):
            # Could be domain-first such as 'example.com/docs'
            parsed = urlparse(f"http://{target}")
            has_explicit_scheme = False
        else:
            parsed = urlparse(target)
            has_explicit_scheme = True
            
        if has_explicit_scheme:
            self._scheme = parsed.scheme.lower()
            self._domain = parsed.hostname.lower() if parsed.hostname else ""
            self._port = parsed.port
            self._path = parsed.path or "/"
            self._query = parsed.query
            self._fragment = parsed.fragment
            self._is_valid = bool(self._scheme and self._domain)
        else:
            self._scheme = ""
            self._domain = parsed.hostname.lower() if parsed.hostname else ""
            self._port = parsed.port
            self._path = parsed.path or "/"
            self._query = parsed.query
            self._fragment = parsed.fragment
            self._is_valid = bool(self._domain and "." in self._domain)
            
    @property
    def url(self) -> str:
        """The normalized URL string."""
        if self._scheme and self._domain:
            netloc = self._domain
            if self._port:
                netloc += f":{self._port}"
            return urlunparse((self._scheme, netloc, self._path, "", self._query, self._fragment))
        return self._raw_input
        
    @property
    def protocol(self) -> str:
        """The network protocol/scheme (e.g., 'http', 'https', 'ftp')."""
        return self._scheme
        
    @property
    def domain(self) -> str:
        """The fully qualified domain name or hostname."""
        return self._domain
        
    @property
    def port(self) -> Optional[int]:
        """The port number if specified, or None."""
        return self._port
        
    @property
    def path(self) -> str:
        """The hierarchical path component of the URL."""
        return self._path
        
    @property
    def query(self) -> str:
        """The query parameter string."""
        return self._query
        
    @property
    def fragment(self) -> str:
        """The anchor fragment identifier."""
        return self._fragment
        
    @property
    def is_secure(self) -> bool:
        """
        True if the URL uses encrypted HTTPS transport.
        Does NOT guarantee that the remote server or content is trustworthy.
        """
        return self._scheme == "https"
        
    @property
    def is_valid(self) -> bool:
        """True if the URL conforms to valid URL syntax."""
        return self._is_valid
        
    def __str__(self) -> str:
        return self.url
        
    def __repr__(self) -> str:
        return f"URL({self.url!r}, secure={self.is_secure}, valid={self.is_valid})"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, URL):
            return False
        return self.url == other.url
