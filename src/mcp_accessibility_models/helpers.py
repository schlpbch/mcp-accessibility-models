"""Helper functions for accessibility data extraction and validation."""

from typing import Any, Dict, List, Optional


# =====================================================================
# IATA SSR CODE REFERENCE
# =====================================================================

SSR_CODE_DESCRIPTIONS = {
    "WCHR": "Wheelchair assistance (passenger provides own wheelchair)",
    "WCHS": "Wheelchair with stowage (wheelchair stowed in cargo hold)",
    "STCR": "Stretcher case (medical requirement for stretcher accommodation)",
    "DEAF": "Deaf passenger (visual alerts, no audio announcements)",
    "BLND": "Blind passenger (audio assistance, guide dog accommodation)",
    "PRMK": "Passenger with mobility disability (priority seating, extra assistance)",
}

VALID_SSR_CODES = set(SSR_CODE_DESCRIPTIONS.keys())


# =====================================================================
# HOTEL ACCESSIBILITY EXTRACTION
# =====================================================================


def extract_hotel_accessibility(hotel_property: Dict[str, Any]) -> Dict[str, Any]:
    """Extract accessibility information from SerpAPI hotel property.

    SerpAPI includes amenities with IDs. Amenity ID 53 = wheelchair accessible.

    Args:
        hotel_property: Hotel property dict from SerpAPI response

    Returns:
        Dictionary with accessibility information
    """
    amenities = hotel_property.get("amenities", [])
    amenity_ids = [a.get("id") for a in amenities if isinstance(a, dict) and "id" in a]

    wheelchair_accessible = 53 in amenity_ids

    return {
        "wheelchair_accessible": wheelchair_accessible,
        "accessible_room_available": wheelchair_accessible,
        "wheelchair_amenity_id": 53,
        "amenities": amenities,
    }


def extract_amadeus_hotel_accessibility(hotel_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract accessibility information from Amadeus hotel offer.

    Amadeus returns facility and description data that may contain accessibility info.

    Args:
        hotel_data: Hotel data dict from Amadeus API response

    Returns:
        Dictionary with accessibility information
    """
    facilities = hotel_data.get("facilities", [])
    descriptions = hotel_data.get("descriptions", {})

    # Build facility list from facilities array
    facility_list = []
    if facilities:
        for facility in facilities:
            if isinstance(facility, dict):
                facility_list.append(facility.get("description", str(facility)))
            else:
                facility_list.append(str(facility))

    # Check for accessibility-related facilities
    accessibility_keywords = [
        "wheelchair",
        "accessible",
        "mobility",
        "elevator",
        "ramp",
        "parking",
        "bathroom",
    ]

    has_accessibility = any(
        keyword.lower() in str(facility).lower() for facility in facility_list
        for keyword in accessibility_keywords
    )

    return {
        "wheelchair_accessible": has_accessibility,
        "accessible_room_available": has_accessibility,
        "facility_list": facility_list,
    }


# =====================================================================
# FLIGHT ACCESSIBILITY EXTRACTION
# =====================================================================


def extract_flight_accessibility_from_amadeus(flight_offer: Dict[str, Any]) -> Dict[str, Any]:
    """Extract accessibility information from Amadeus flight offer.

    Amadeus returns traveler pricing which may include special service requests (SSR).

    Args:
        flight_offer: Flight offer dict from Amadeus API response

    Returns:
        Dictionary with accessibility information and SSR codes
    """
    ssr_codes = []

    # Extract SSR codes from traveler pricing if available
    traveler_pricings = flight_offer.get("travelerPricings", [])
    for pricing in traveler_pricings:
        fare_details = pricing.get("fareDetailsBySegment", [])
        for detail in fare_details:
            included_checks = detail.get("includedCheckedBags", {})
            # SSR codes are not typically in the response, but could be passed by user
            # This is a placeholder for extracting them if available in extended response
            pass

    return {
        "wheelchair_available": False,
        "wheelchair_stowage": False,
        "accessible_lavatory": False,
        "extra_legroom_available": False,
        "special_service_codes": ssr_codes if ssr_codes else None,
        "companion_required": None,
        "special_meals_available": False,
        "notes": "Check with airline for specific accessibility accommodations",
    }


# =====================================================================
# IATA SSR CODE VALIDATION
# =====================================================================


def validate_ssr_codes(codes: Optional[List[str]]) -> Optional[List[str]]:
    """Validate IATA Special Service Request (SSR) codes.

    Args:
        codes: List of SSR codes to validate

    Returns:
        List of valid codes, or None if input is None

    Raises:
        ValueError: If any code is invalid
    """
    if codes is None:
        return None

    if not isinstance(codes, list):
        raise ValueError(f"SSR codes must be a list, got {type(codes)}")

    validated = []
    for code in codes:
        if not isinstance(code, str):
            raise ValueError(f"SSR code must be string, got {type(code)}")

        code_upper = code.upper()
        if code_upper not in VALID_SSR_CODES:
            raise ValueError(
                f"Invalid SSR code '{code}'. Valid codes: {', '.join(sorted(VALID_SSR_CODES))}"
            )

        validated.append(code_upper)

    return validated


def get_ssr_code_description(code: str) -> str:
    """Get human-readable description of an IATA SSR code.

    Args:
        code: IATA SSR code (e.g., 'WCHR', 'DEAF')

    Returns:
        Description of the code

    Raises:
        ValueError: If code is not valid
    """
    code_upper = code.upper()
    if code_upper not in VALID_SSR_CODES:
        raise ValueError(
            f"Invalid SSR code '{code}'. Valid codes: {', '.join(sorted(VALID_SSR_CODES))}"
        )

    return SSR_CODE_DESCRIPTIONS[code_upper]


def get_all_ssr_codes() -> Dict[str, str]:
    """Get all valid IATA SSR codes and their descriptions.

    Returns:
        Dictionary mapping code to description
    """
    return SSR_CODE_DESCRIPTIONS.copy()
