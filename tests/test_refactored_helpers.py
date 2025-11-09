"""
Tests for refactored helper functions to verify duplication elimination
"""
import pytest
from src.app import (
    build_activities_context,
    get_participation_data,
    activities
)


def test_build_activities_context_includes_all_activities():
    """Verify build_activities_context returns formatted string with all activities"""
    context = build_activities_context()
    
    # Check that all activities are included
    for activity_name in activities.keys():
        assert activity_name in context
    
    # Check that key fields are included
    assert "Description:" in context
    assert "Schedule:" in context
    assert "Capacity:" in context


def test_get_participation_data_returns_correct_structure():
    """Verify get_participation_data returns proper structure for all activities"""
    data = get_participation_data()
    
    # Should have one entry per activity
    assert len(data) == len(activities)
    
    # Check structure of each entry
    for entry in data:
        assert "activity" in entry
        assert "participants" in entry
        assert "capacity" in entry
        assert "fill_rate" in entry
        assert entry["activity"] in activities
        assert isinstance(entry["participants"], int)
        assert isinstance(entry["capacity"], int)
        assert "%" in entry["fill_rate"]


def test_get_participation_data_calculates_fill_rate_correctly():
    """Verify fill rate calculation is accurate"""
    data = get_participation_data()
    
    for entry in data:
        activity_name = entry["activity"]
        activity = activities[activity_name]
        
        expected_count = len(activity["participants"])
        expected_capacity = activity["max_participants"]
        expected_percentage = (expected_count / expected_capacity) * 100
        expected_fill_rate = f"{expected_percentage:.1f}%"
        
        assert entry["participants"] == expected_count
        assert entry["capacity"] == expected_capacity
        assert entry["fill_rate"] == expected_fill_rate
