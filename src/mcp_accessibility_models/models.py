"""Pydantic models for accessibility features across MCP travel services."""

from typing import List, Optional
from pydantic import BaseModel, Field


class FlightAccessibility(BaseModel):
    """Accessibility features and accommodations for flights."""

    wheelchair_available: bool = Field(
        False,
        description="Wheelchair seating/accommodation available",
    )
    wheelchair_stowage: bool = Field(
        False,
        description="Wheelchair can be stowed in cargo hold",
    )
    accessible_lavatory: bool = Field(
        False,
        description="Aircraft has accessible lavatory",
    )
    extra_legroom_available: bool = Field(
        False,
        description="Extra legroom seating available for mobility impaired",
    )
    special_service_codes: Optional[List[str]] = Field(
        None,
        description="Amadeus SSR codes: WCHR (wheelchair), WCHS (wheelchair with stowage), STCR (stretcher), DEAF (deaf passenger), BLND (blind passenger), PRMK (passenger with mobility disability)",
    )
    companion_required: Optional[bool] = Field(
        None,
        description="Companion/escort passenger required for assistance",
    )
    special_meals_available: bool = Field(
        False,
        description="Special meal options (diabetic, low sodium, etc.)",
    )
    notes: Optional[str] = Field(
        None,
        description="Additional accessibility information from airline",
    )


class HotelAccessibility(BaseModel):
    """Accessibility features and accommodations for hotels."""

    wheelchair_accessible: bool = Field(
        False,
        description="Hotel has wheelchair accessible rooms available",
    )
    accessible_room_available: bool = Field(
        False,
        description="Accessible rooms currently in stock",
    )
    wheelchair_amenity_id: int = Field(
        53,
        description="SerpAPI amenity ID for wheelchair accessible (static reference)",
    )
    accessible_bathroom_types: Optional[List[str]] = Field(
        None,
        description="Types of accessible bathrooms (roll-in shower, grab bars, accessible toilet, etc.)",
    )
    accessible_parking: bool = Field(
        False,
        description="Accessible/handicap parking spaces available",
    )
    accessible_entrance: bool = Field(
        False,
        description="Level or ramped entrance for wheelchair access",
    )
    accessible_elevator: bool = Field(
        False,
        description="Accessible elevator serving all guest floors",
    )
    service_animals_allowed: bool = Field(
        False,
        description="Service animals/guide dogs allowed in accessible rooms",
    )
    lowest_accessible_price: Optional[float] = Field(
        None,
        description="Price of least expensive accessible room (Amadeus data)",
    )
    facility_list: Optional[List[str]] = Field(
        None,
        description="Complete list of accessibility features/facilities",
    )


class AccessibilityRequest(BaseModel):
    """Accessibility requirements for personalized trip planning."""

    wheelchair_user: bool = Field(
        False,
        description="Traveler uses wheelchair (may require stowage)",
    )
    reduced_mobility: bool = Field(
        False,
        description="General reduced mobility requiring assistance",
    )
    deaf: bool = Field(
        False,
        description="Deaf traveler (needs visual alerts on flights)",
    )
    blind: bool = Field(
        False,
        description="Blind traveler (needs audio assistance on flights)",
    )
    stretcher_case: bool = Field(
        False,
        description="Medical condition requiring stretcher/medical equipment",
    )
    companion_required: bool = Field(
        False,
        description="Companion/escort passenger traveling with accessible passenger",
    )
    special_requirements: Optional[str] = Field(
        None,
        description="Additional mobility or medical needs (allergies, equipment, etc.)",
    )
