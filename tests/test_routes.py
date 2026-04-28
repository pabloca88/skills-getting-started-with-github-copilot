import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_200(self, client):
        # Arrange - no setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
    
    def test_get_activities_contains_expected_keys(self, client):
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_details in activities.values():
            assert set(activity_details.keys()) == expected_keys
    
    def test_get_activities_has_Basketball(self, client):
        # Arrange - Basketball is in our test database
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert "Basketball" in activities
        assert activities["Basketball"]["max_participants"] == 15


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_success(self, client):
        # Arrange
        activity_name = "Basketball"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "NonexistentActivity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_activity_returns_400(self, client):
        # Arrange
        activity_name = "Basketball"
        email = "alex@mergington.edu"  # Already signed up for Basketball
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_unregister_participant_success(self, client):
        # Arrange
        activity_name = "Basketball"
        email = "alex@mergington.edu"  # Already a participant
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity_name]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "NonexistentActivity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_nonexistent_participant_returns_404(self, client):
        # Arrange
        activity_name = "Basketball"
        email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
