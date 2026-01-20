# MCP Accessibility Models

Shared accessibility data models and helper functions for Model Context Protocol (MCP) servers providing travel services.

## Overview

This package provides reusable, battle-tested accessibility models and helpers used across the MCP travel ecosystem:

- **Travel Assistant MCP** - Global flight, hotel, event, and weather services
- **Swiss Tourism MCP** - Swiss attractions, resorts, RailAway combos, and packages
- **Future MCPs** - Any travel-related MCP that needs accessibility support

## Features

### 📊 Pydantic Models

Three comprehensive accessibility models with full type safety and validation:

#### FlightAccessibility
Accessibility features for airline flights:
- `wheelchair_available` - Wheelchair seating/accommodation
- `wheelchair_stowage` - Wheelchair can be stowed in cargo
- `accessible_lavatory` - Accessible onboard restroom
- `extra_legroom_available` - Extra legroom seating
- `special_service_codes` - IATA SSR codes (WCHR, WCHS, STCR, DEAF, BLND, PRMK)
- `companion_required` - Companion/escort needed
- `special_meals_available` - Dietary accommodations
- `notes` - Additional accessibility info

#### HotelAccessibility
Accessibility features for accommodation:
- `wheelchair_accessible` - Wheelchair accessible rooms
- `accessible_room_available` - Rooms in stock
- `wheelchair_amenity_id` - SerpAPI amenity reference (53)
- `accessible_bathroom_types` - Roll-in shower, grab bars, etc.
- `accessible_parking` - Handicap parking
- `accessible_entrance` - Level or ramped entrance
- `accessible_elevator` - Accessible elevator access
- `service_animals_allowed` - Service animal policy
- `lowest_accessible_price` - Price of most affordable accessible room
- `facility_list` - Complete facility list

#### AccessibilityRequest
Traveler accessibility needs and requirements:
- `wheelchair_user` - Wheelchair usage
- `reduced_mobility` - General mobility limitations
- `deaf` - Deaf traveler (visual alert requirements)
- `blind` - Blind traveler (audio assistance)
- `stretcher_case` - Medical requirements
- `companion_required` - Traveling with companion
- `special_requirements` - Additional needs

### 🔧 Helper Functions

#### Extraction Helpers
- `extract_hotel_accessibility()` - Extract from SerpAPI hotel data (amenity ID 53)
- `extract_amadeus_hotel_accessibility()` - Extract from Amadeus hotel data (keyword matching)
- `extract_flight_accessibility_from_amadeus()` - Extract from Amadeus flight data

#### Validation Helpers
- `validate_ssr_codes()` - Validate IATA SSR codes
- `get_ssr_code_description()` - Get human-readable description
- `get_all_ssr_codes()` - Get all valid codes and descriptions

## Installation

### From PyPI
```bash
pip install mcp-accessibility-models
```

### From Source
```bash
git clone <repository>
cd mcp-accessibility-models
pip install -e ".[dev]"
```

## Usage

### Import Models

```python
from mcp_accessibility_models import (
    FlightAccessibility,
    HotelAccessibility,
    AccessibilityRequest,
)

# Create flight accessibility
flight = FlightAccessibility(
    wheelchair_available=True,
    wheelchair_stowage=True,
    special_service_codes=["WCHR", "WCHS"],
)

# Create hotel accessibility
hotel = HotelAccessibility(
    wheelchair_accessible=True,
    accessible_parking=True,
    facility_list=["Accessible rooms", "Accessible parking"],
)

# Create accessibility request
request = AccessibilityRequest(
    wheelchair_user=True,
    companion_required=True,
    special_requirements="Manual wheelchair, needs stowage",
)
```

### Use Extraction Helpers

```python
from mcp_accessibility_models import (
    extract_hotel_accessibility,
    extract_amadeus_hotel_accessibility,
)

# Extract from SerpAPI hotel data
hotel_property = {
    "name": "Accessible Hotel",
    "amenities": [
        {"id": 1, "name": "WiFi"},
        {"id": 53, "name": "Wheelchair accessible"},
    ],
}
accessibility = extract_hotel_accessibility(hotel_property)
# Result: {"wheelchair_accessible": True, "accessible_room_available": True, ...}

# Extract from Amadeus hotel data
amadeus_hotel = {
    "facilities": [
        {"description": "Wheelchair accessible rooms"},
        {"description": "Accessible parking"},
    ],
}
accessibility = extract_amadeus_hotel_accessibility(amadeus_hotel)
# Result: {"wheelchair_accessible": True, "facility_list": [...], ...}
```

### Validate SSR Codes

```python
from mcp_accessibility_models import (
    validate_ssr_codes,
    get_ssr_code_description,
)

# Validate codes
codes = validate_ssr_codes(["WCHR", "WCHS", "DEAF"])
# Returns: ["WCHR", "WCHS", "DEAF"]

# Get description
desc = get_ssr_code_description("WCHR")
# Returns: "Wheelchair assistance (passenger provides own wheelchair)"

# Invalid code raises ValueError
try:
    validate_ssr_codes(["INVALID"])
except ValueError as e:
    print(f"Error: {e}")
```

## IATA SSR Codes

Supported Special Service Request codes used by airlines:

| Code | Description |
|------|-------------|
| WCHR | Wheelchair assistance (passenger provides own wheelchair) |
| WCHS | Wheelchair with stowage (wheelchair stowed in cargo hold) |
| STCR | Stretcher case (medical requirement for stretcher accommodation) |
| DEAF | Deaf passenger (visual alerts, no audio announcements) |
| BLND | Blind passenger (audio assistance, guide dog accommodation) |
| PRMK | Passenger with mobility disability (priority seating, extra assistance) |

## Testing

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_models.py
pytest tests/test_helpers.py
```

Run with coverage:

```bash
pytest --cov=mcp_accessibility_models
```

## Architecture

### Single Source of Truth

This package provides shared models used across multiple MCP servers:

```
┌─────────────────────────────────────────┐
│  mcp-accessibility-models (v1.0.0)      │
├─────────────────────────────────────────┤
│ • FlightAccessibility                   │
│ • HotelAccessibility                    │
│ • AccessibilityRequest                  │
│ • Extraction Helpers                    │
│ • SSR Validators                        │
└─────────────────────────────────────────┘
        ▲                           ▲
        │                           │
    ┌───┴─────────────┐    ┌────────┴───┐
    │  Travel         │    │  Swiss     │
    │  Assistant      │    │  Tourism   │
    │  MCP (v2.4+)    │    │  MCP       │
    └─────────────────┘    └────────────┘
```

### No Circular Dependencies

Each MCP independently imports from this shared package without creating dependency cycles:

- Travel Assistant MCP → mcp-accessibility-models ✅
- Swiss Tourism MCP → mcp-accessibility-models ✅
- Future MCP → mcp-accessibility-models ✅

## Contributing

This package is part of the MCP travel ecosystem. Contributions should follow existing patterns:

1. Add model fields with clear descriptions
2. Add extraction helpers for new API sources
3. Add comprehensive tests (100% coverage)
4. Update documentation
5. Follow semantic versioning

## Version History

### v1.0.0 (January 20, 2026)
- Initial release
- 3 Pydantic models (FlightAccessibility, HotelAccessibility, AccessibilityRequest)
- 3 extraction helpers
- 6 validation helpers
- 25+ comprehensive tests
- 100% test coverage

## License

This package is part of the Anthropic Model Context Protocol ecosystem.

## Support

For issues or questions:
1. Check the main MCP documentation
2. Review test cases for usage examples
3. File issues on the repository

---

**Package Version:** 1.0.0
**Last Updated:** January 20, 2026
**Status:** Stable & Production Ready
