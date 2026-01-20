"""MCP Accessibility Models - Shared data models and helpers for accessible travel planning."""

from .models import (
    FlightAccessibility,
    HotelAccessibility,
    AccessibilityRequest,
)

from .helpers import (
    extract_hotel_accessibility,
    extract_amadeus_hotel_accessibility,
    extract_flight_accessibility_from_amadeus,
    validate_ssr_codes,
    get_ssr_code_description,
)

__version__ = "1.0.0"
__all__ = [
    "FlightAccessibility",
    "HotelAccessibility",
    "AccessibilityRequest",
    "extract_hotel_accessibility",
    "extract_amadeus_hotel_accessibility",
    "extract_flight_accessibility_from_amadeus",
    "validate_ssr_codes",
    "get_ssr_code_description",
]
