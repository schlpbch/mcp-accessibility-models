"""Tests for accessibility helper functions."""

import pytest
from mcp_accessibility_models import (
    extract_hotel_accessibility,
    extract_amadeus_hotel_accessibility,
    extract_flight_accessibility_from_amadeus,
    validate_ssr_codes,
    get_ssr_code_description,
)


class TestHotelAccessibilityExtraction:
    """Test extraction of accessibility data from hotel properties."""

    def test_extract_wheelchair_accessible_hotel(self):
        """Test extracting wheelchair accessible amenity from hotel."""
        hotel_property = {
            "name": "Accessible Hotel",
            "amenities": [
                {"id": 1, "name": "WiFi"},
                {"id": 53, "name": "Wheelchair accessible"},
                {"id": 5, "name": "Parking"},
            ],
        }
        accessibility = extract_hotel_accessibility(hotel_property)
        assert accessibility["wheelchair_accessible"] is True
        assert accessibility["accessible_room_available"] is True
        assert accessibility["wheelchair_amenity_id"] == 53

    def test_extract_non_wheelchair_hotel(self):
        """Test hotel without wheelchair accessibility."""
        hotel_property = {
            "name": "Standard Hotel",
            "amenities": [
                {"id": 1, "name": "WiFi"},
                {"id": 5, "name": "Parking"},
            ],
        }
        accessibility = extract_hotel_accessibility(hotel_property)
        assert accessibility["wheelchair_accessible"] is False
        assert accessibility["accessible_room_available"] is False

    def test_extract_hotel_without_amenities(self):
        """Test hotel with no amenities field."""
        hotel_property = {"name": "Simple Hotel"}
        accessibility = extract_hotel_accessibility(hotel_property)
        assert accessibility["wheelchair_accessible"] is False
        assert accessibility["wheelchair_amenity_id"] == 53

    def test_extract_hotel_empty_amenities(self):
        """Test hotel with empty amenities list."""
        hotel_property = {
            "name": "Empty Hotel",
            "amenities": [],
        }
        accessibility = extract_hotel_accessibility(hotel_property)
        assert accessibility["wheelchair_accessible"] is False


class TestAmadeusHotelAccessibilityExtraction:
    """Test extraction of accessibility data from Amadeus hotels."""

    def test_extract_amadeus_accessible_facilities(self):
        """Test extracting accessibility from Amadeus facilities."""
        hotel_data = {
            "name": "Accessible Hotel",
            "facilities": [
                {"description": "Wheelchair accessible rooms"},
                {"description": "Accessible bathroom with grab bars"},
                {"description": "Elevator"},
            ],
        }
        accessibility = extract_amadeus_hotel_accessibility(hotel_data)
        assert accessibility["wheelchair_accessible"] is True
        assert accessibility["accessible_room_available"] is True
        assert len(accessibility["facility_list"]) == 3

    def test_extract_amadeus_no_accessibility(self):
        """Test Amadeus hotel without accessibility features."""
        hotel_data = {
            "name": "Standard Hotel",
            "facilities": [
                {"description": "WiFi"},
                {"description": "Restaurant"},
            ],
        }
        accessibility = extract_amadeus_hotel_accessibility(hotel_data)
        assert accessibility["wheelchair_accessible"] is False

    def test_extract_amadeus_no_facilities(self):
        """Test Amadeus hotel with no facilities."""
        hotel_data = {"name": "Simple Hotel"}
        accessibility = extract_amadeus_hotel_accessibility(hotel_data)
        assert accessibility["wheelchair_accessible"] is False
        assert accessibility["facility_list"] == []

    def test_extract_amadeus_accessibility_keywords(self):
        """Test detection of various accessibility keywords."""
        keywords = [
            "wheelchair",
            "accessible",
            "mobility",
            "elevator",
            "ramp",
            "parking",
            "bathroom",
        ]

        for keyword in keywords:
            hotel_data = {
                "facilities": [{"description": f"Feature with {keyword} available"}]
            }
            accessibility = extract_amadeus_hotel_accessibility(hotel_data)
            assert accessibility["wheelchair_accessible"] is True, (
                f"Failed for keyword: {keyword}"
            )

    def test_extract_amadeus_case_insensitive(self):
        """Test that accessibility keyword matching is case-insensitive."""
        hotel_data = {
            "facilities": [
                {"description": "WHEELCHAIR ACCESSIBLE ROOMS"},
                {"description": "Accessible BATHROOM"},
            ]
        }
        accessibility = extract_amadeus_hotel_accessibility(hotel_data)
        assert accessibility["wheelchair_accessible"] is True


class TestFlightAccessibilityExtraction:
    """Test extraction of accessibility data from flight offers."""

    def test_extract_flight_basic(self):
        """Test basic flight accessibility extraction."""
        flight_offer = {
            "id": "1",
            "source": "GDS",
        }
        accessibility = extract_flight_accessibility_from_amadeus(flight_offer)
        assert accessibility["wheelchair_available"] is False
        assert accessibility["accessible_lavatory"] is False
        assert accessibility["notes"] is not None

    def test_extract_flight_default_values(self):
        """Test that all fields have default values."""
        flight_offer = {}
        accessibility = extract_flight_accessibility_from_amadeus(flight_offer)
        assert "wheelchair_available" in accessibility
        assert "wheelchair_stowage" in accessibility
        assert "accessible_lavatory" in accessibility
        assert "extra_legroom_available" in accessibility
        assert "special_service_codes" in accessibility


class TestSSRCodeValidation:
    """Test IATA SSR code validation."""

    def test_validate_valid_ssr_codes(self):
        """Test validation of valid SSR codes."""
        codes = ["WCHR", "WCHS", "STCR", "DEAF", "BLND", "PRMK"]
        validated = validate_ssr_codes(codes)
        assert validated == codes

    def test_validate_lowercase_ssr_codes(self):
        """Test that lowercase codes are converted to uppercase."""
        codes = ["wchr", "wchs"]
        validated = validate_ssr_codes(codes)
        assert validated == ["WCHR", "WCHS"]

    def test_validate_invalid_ssr_code(self):
        """Test that invalid codes raise ValueError."""
        codes = ["INVALID"]
        with pytest.raises(ValueError):
            validate_ssr_codes(codes)

    def test_validate_none_ssr_codes(self):
        """Test that None returns None."""
        validated = validate_ssr_codes(None)
        assert validated is None

    def test_validate_empty_list(self):
        """Test that empty list returns empty list."""
        validated = validate_ssr_codes([])
        assert validated == []

    def test_validate_non_list_raises_error(self):
        """Test that non-list input raises ValueError."""
        with pytest.raises(ValueError):
            validate_ssr_codes("WCHR")

    def test_validate_non_string_code_raises_error(self):
        """Test that non-string codes raise ValueError."""
        with pytest.raises(ValueError):
            validate_ssr_codes([123])


class TestSSRCodeDescription:
    """Test IATA SSR code descriptions."""

    def test_get_wchr_description(self):
        """Test WCHR code description."""
        desc = get_ssr_code_description("WCHR")
        assert "wheelchair" in desc.lower()
        assert "assistance" in desc.lower()

    def test_get_deaf_description(self):
        """Test DEAF code description."""
        desc = get_ssr_code_description("DEAF")
        assert "deaf" in desc.lower()
        assert "visual" in desc.lower()

    def test_get_blnd_description(self):
        """Test BLND code description."""
        desc = get_ssr_code_description("BLND")
        assert "blind" in desc.lower()
        assert "audio" in desc.lower()

    def test_get_stcr_description(self):
        """Test STCR code description."""
        desc = get_ssr_code_description("STCR")
        assert "stretcher" in desc.lower()

    def test_invalid_code_raises_error(self):
        """Test that invalid code raises ValueError."""
        with pytest.raises(ValueError):
            get_ssr_code_description("INVALID")

    def test_case_insensitive_lookup(self):
        """Test that code lookup is case-insensitive."""
        desc_upper = get_ssr_code_description("WCHR")
        desc_lower = get_ssr_code_description("wchr")
        assert desc_upper == desc_lower
