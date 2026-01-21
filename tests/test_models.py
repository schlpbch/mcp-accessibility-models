"""Tests for accessibility Pydantic models."""

from mcp_accessibility_models import (
    FlightAccessibility,
    HotelAccessibility,
    AccessibilityRequest,
)


class TestFlightAccessibility:
    """Test FlightAccessibility Pydantic model."""

    def test_valid_flight_accessibility_minimal(self):
        """Test creating FlightAccessibility with default values."""
        accessibility = FlightAccessibility()
        assert accessibility.wheelchair_available is False
        assert accessibility.wheelchair_stowage is False
        assert accessibility.accessible_lavatory is False
        assert accessibility.extra_legroom_available is False
        assert accessibility.special_meals_available is False
        assert accessibility.special_service_codes is None
        assert accessibility.companion_required is None
        assert accessibility.notes is None

    def test_valid_flight_accessibility_wheelchair(self):
        """Test FlightAccessibility for wheelchair user."""
        accessibility = FlightAccessibility(
            wheelchair_available=True,
            wheelchair_stowage=True,
            accessible_lavatory=True,
            special_service_codes=["WCHR", "WCHS"],
        )
        assert accessibility.wheelchair_available is True
        assert accessibility.wheelchair_stowage is True
        assert accessibility.accessible_lavatory is True
        assert "WCHR" in accessibility.special_service_codes

    def test_flight_accessibility_with_ssr_codes(self):
        """Test FlightAccessibility with various SSR codes."""
        accessibility = FlightAccessibility(
            special_service_codes=["WCHR", "STCR", "DEAF", "BLND", "PRMK"],
        )
        assert len(accessibility.special_service_codes) == 5
        assert "WCHR" in accessibility.special_service_codes
        assert "DEAF" in accessibility.special_service_codes
        assert "BLND" in accessibility.special_service_codes

    def test_flight_accessibility_companion_required(self):
        """Test FlightAccessibility with companion requirement."""
        accessibility = FlightAccessibility(
            wheelchair_available=True,
            companion_required=True,
            notes="Traveler requires assistance with mobility",
        )
        assert accessibility.companion_required is True
        assert accessibility.notes is not None

    def test_flight_accessibility_special_meals(self):
        """Test FlightAccessibility with special meal requirements."""
        accessibility = FlightAccessibility(
            special_meals_available=True,
        )
        assert accessibility.special_meals_available is True

    def test_flight_accessibility_all_features(self):
        """Test FlightAccessibility with all accessibility features."""
        accessibility = FlightAccessibility(
            wheelchair_available=True,
            wheelchair_stowage=True,
            accessible_lavatory=True,
            extra_legroom_available=True,
            special_service_codes=["WCHR", "WCHS", "STCR"],
            companion_required=False,
            special_meals_available=True,
            notes="Fully accessible economy seat with aisle chair",
        )
        assert accessibility.wheelchair_available is True
        assert accessibility.extra_legroom_available is True
        assert accessibility.special_meals_available is True
        assert accessibility.notes is not None

    def test_flight_accessibility_schema(self):
        """Test that FlightAccessibility has proper field descriptions."""
        schema = FlightAccessibility.model_json_schema()
        assert "properties" in schema
        assert "wheelchair_available" in schema["properties"]
        assert "special_service_codes" in schema["properties"]


class TestHotelAccessibility:
    """Test HotelAccessibility Pydantic model."""

    def test_valid_hotel_accessibility_minimal(self):
        """Test creating HotelAccessibility with default values."""
        accessibility = HotelAccessibility()
        assert accessibility.wheelchair_accessible is False
        assert accessibility.accessible_room_available is False
        assert accessibility.wheelchair_amenity_id == 53
        assert accessibility.accessible_parking is False

    def test_hotel_accessibility_wheelchair_accessible(self):
        """Test HotelAccessibility for wheelchair users."""
        accessibility = HotelAccessibility(
            wheelchair_accessible=True,
            accessible_room_available=True,
            accessible_entrance=True,
            accessible_elevator=True,
            accessible_parking=True,
        )
        assert accessibility.wheelchair_accessible is True
        assert accessibility.accessible_entrance is True
        assert accessibility.accessible_parking is True

    def test_hotel_accessibility_bathroom_types(self):
        """Test HotelAccessibility with various bathroom types."""
        accessibility = HotelAccessibility(
            accessible_bathroom_types=[
                "roll-in shower",
                "grab bars",
                "accessible toilet",
            ],
        )
        assert len(accessibility.accessible_bathroom_types) == 3
        assert "roll-in shower" in accessibility.accessible_bathroom_types

    def test_hotel_accessibility_service_animals(self):
        """Test HotelAccessibility with service animal support."""
        accessibility = HotelAccessibility(
            service_animals_allowed=True,
        )
        assert accessibility.service_animals_allowed is True

    def test_hotel_accessibility_pricing(self):
        """Test HotelAccessibility with pricing information."""
        accessibility = HotelAccessibility(
            wheelchair_accessible=True,
            lowest_accessible_price=189.99,
        )
        assert accessibility.lowest_accessible_price == 189.99

    def test_hotel_accessibility_facility_list(self):
        """Test HotelAccessibility with comprehensive facility list."""
        facilities = [
            "Accessible rooms",
            "Wheelchair accessible bathrooms",
            "Accessible parking",
            "Service animal friendly",
        ]
        accessibility = HotelAccessibility(
            wheelchair_accessible=True,
            facility_list=facilities,
        )
        assert len(accessibility.facility_list) == 4
        assert "Accessible rooms" in accessibility.facility_list

    def test_hotel_accessibility_schema(self):
        """Test that HotelAccessibility has proper field descriptions."""
        schema = HotelAccessibility.model_json_schema()
        assert "properties" in schema
        assert "wheelchair_accessible" in schema["properties"]
        assert "accessible_parking" in schema["properties"]


class TestAccessibilityRequest:
    """Test AccessibilityRequest Pydantic model."""

    def test_valid_accessibility_request_minimal(self):
        """Test creating AccessibilityRequest with default values."""
        request = AccessibilityRequest()
        assert request.wheelchair_user is False
        assert request.reduced_mobility is False
        assert request.deaf is False
        assert request.blind is False
        assert request.stretcher_case is False
        assert request.companion_required is False
        assert request.special_requirements is None

    def test_accessibility_request_wheelchair_user(self):
        """Test AccessibilityRequest for wheelchair user."""
        request = AccessibilityRequest(
            wheelchair_user=True,
            special_requirements="Manual wheelchair, needs stowage",
        )
        assert request.wheelchair_user is True
        assert request.special_requirements is not None

    def test_accessibility_request_reduced_mobility(self):
        """Test AccessibilityRequest for reduced mobility."""
        request = AccessibilityRequest(
            reduced_mobility=True,
            companion_required=True,
        )
        assert request.reduced_mobility is True
        assert request.companion_required is True

    def test_accessibility_request_deaf_traveler(self):
        """Test AccessibilityRequest for deaf traveler."""
        request = AccessibilityRequest(
            deaf=True,
        )
        assert request.deaf is True
        assert request.blind is False

    def test_accessibility_request_blind_traveler(self):
        """Test AccessibilityRequest for blind traveler."""
        request = AccessibilityRequest(
            blind=True,
            special_requirements="Needs Braille materials",
        )
        assert request.blind is True
        assert "Braille" in request.special_requirements

    def test_accessibility_request_schema(self):
        """Test that AccessibilityRequest has proper field descriptions."""
        schema = AccessibilityRequest.model_json_schema()
        assert "properties" in schema
        assert "wheelchair_user" in schema["properties"]
        assert "deaf" in schema["properties"]
