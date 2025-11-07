from fastapi.testclient import TestClient
from src.app import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_get_weather_success():
    """Test successful weather data fetch"""
    # Mock the geocoding response
    mock_geocode_response = MagicMock()
    mock_geocode_response.json.return_value = {
        "results": [{
            "name": "New York",
            "country": "United States",
            "latitude": 40.7128,
            "longitude": -74.0060
        }]
    }
    mock_geocode_response.raise_for_status = MagicMock()
    
    # Mock the weather response
    mock_weather_response = MagicMock()
    mock_weather_response.json.return_value = {
        "current": {
            "temperature_2m": 68.5,
            "apparent_temperature": 66.2,
            "relative_humidity_2m": 65,
            "weather_code": 0,
            "wind_speed_10m": 8.5,
            "precipitation": 0.0,
            "time": "2025-11-07T15:00"
        }
    }
    mock_weather_response.raise_for_status = MagicMock()
    
    with patch('src.app.requests.get') as mock_get:
        mock_get.side_effect = [mock_geocode_response, mock_weather_response]
        
        resp = client.get("/weather?location=New York")
        assert resp.status_code == 200
        data = resp.json()
        
        # Check response structure
        assert "location" in data
        assert "temperature" in data
        assert "humidity" in data
        assert "conditions" in data
        assert "wind_speed" in data
        
        # Check values
        assert data["temperature"] == 68.5
        assert data["humidity"] == 65
        assert data["conditions"] == "Clear sky"
        assert data["wind_speed"] == 8.5


def test_get_weather_default_location():
    """Test weather endpoint with default location"""
    mock_geocode_response = MagicMock()
    mock_geocode_response.json.return_value = {
        "results": [{
            "name": "New York",
            "country": "United States",
            "latitude": 40.7128,
            "longitude": -74.0060
        }]
    }
    mock_geocode_response.raise_for_status = MagicMock()
    
    mock_weather_response = MagicMock()
    mock_weather_response.json.return_value = {
        "current": {
            "temperature_2m": 70.0,
            "apparent_temperature": 68.0,
            "relative_humidity_2m": 60,
            "weather_code": 1,
            "wind_speed_10m": 5.0,
            "precipitation": 0.0,
            "time": "2025-11-07T15:00"
        }
    }
    mock_weather_response.raise_for_status = MagicMock()
    
    with patch('src.app.requests.get') as mock_get:
        mock_get.side_effect = [mock_geocode_response, mock_weather_response]
        
        resp = client.get("/weather")
        assert resp.status_code == 200
        data = resp.json()
        assert "location" in data
        assert "temperature" in data


def test_get_weather_location_not_found():
    """Test weather endpoint with invalid location"""
    mock_geocode_response = MagicMock()
    mock_geocode_response.json.return_value = {
        "results": []
    }
    mock_geocode_response.raise_for_status = MagicMock()
    
    with patch('src.app.requests.get') as mock_get:
        mock_get.return_value = mock_geocode_response
        
        resp = client.get("/weather?location=InvalidLocationXYZ123")
        assert resp.status_code == 404
        data = resp.json()
        assert "detail" in data


def test_get_weather_service_unavailable():
    """Test weather endpoint when external service is down"""
    with patch('src.app.requests.get') as mock_get:
        import requests
        mock_get.side_effect = requests.RequestException("Service unavailable")
        
        resp = client.get("/weather?location=London")
        assert resp.status_code == 503
        data = resp.json()
        assert "detail" in data
        assert "Weather service unavailable" in data["detail"]
