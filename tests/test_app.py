from fastapi.testclient import TestClient

def test_root_redirect(client: TestClient):
    """Test that root endpoint redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client: TestClient):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Check some known activities exist
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    
    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert all(key in chess_club for key in ["description", "schedule", "max_participants", "participants"])

def test_signup_success(client: TestClient):
    """Test successful activity signup"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify student was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_full_activity(client: TestClient):
    """Test signup for a full activity"""
    activity_name = "Chess Club"
    
    # Fill up the activity
    activities = client.get("/activities").json()
    max_participants = activities[activity_name]["max_participants"]
    current_participants = activities[activity_name]["participants"]
    
    # Add participants until full
    for i in range(max_participants - len(current_participants)):
        email = f"filler{i}@mergington.edu"
        client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Try to add one more
    response = client.post(f"/activities/{activity_name}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]

def test_unregister_success(client: TestClient):
    """Test successful unregistration from activity"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Known participant
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify student was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_registered(client: TestClient):
    """Test unregistering a student who isn't registered"""
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 404
    assert "Student not registered" in response.json()["detail"]

def test_activity_not_found(client: TestClient):
    """Test accessing non-existent activity"""
    activity_name = "Non Existent Club"
    email = "student@mergington.edu"
    
    # Test both endpoints
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 404
    
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 404