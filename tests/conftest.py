import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before and after each test"""
    # Store original state
    original_activities = {
        "Basketball": {
            "description": "Team sport and basketball skills development",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis": {
            "description": "Learn tennis techniques and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media art",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["grace@mergington.edu", "jacob@mergington.edu"]
        }
    }
    
    # Clear and reset before test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client(reset_activities):
    """Provide TestClient instance with reset database"""
    return TestClient(app)
