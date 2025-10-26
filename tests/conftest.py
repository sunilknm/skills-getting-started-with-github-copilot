import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    """Create a test client for our FastAPI app"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_test_data():
    """Reset activities data before each test"""
    # Store original data
    original_data = activities.copy()
    
    # Reset after test
    yield
    activities.clear()
    activities.update(original_data)